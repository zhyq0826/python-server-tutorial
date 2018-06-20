# -*- coding:utf-8 -*-

import socket
import select
import sys
import Queue

from datetime import datetime


from util import print_red, print_green


def main():
    # create tcp socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # enable reuse address port
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind socket to the port
    server.setblocking(0)
    server_address = ('localhost', 8000)
    server.bind(server_address)
    server.listen(10)
    # Outgoing message queues (socket:Queue)
    message_queues = {}
    # 1 second
    TIMEOUT = 1

    """
    POLLIN  Input ready
    POLLPRI Priority input ready
    POLLOUT Able to receive output
    POLLERR Error
    POLLHUP Channel closed
    POLLNVAL    Channel not open
    """
    READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
    READ_WRITE = READ_ONLY | select.POLLOUT
    poller = select.epoll()
    poller.register(server.fileno(), READ_ONLY | select.EPOLLET)

    # Map file descriptors to socket objects
    fd_to_socket = {server.fileno(): server}
    while True:
        # Wait for at least one of the sockets to be ready for processing
        print_green(' waitting to recevie message from client')
        events = poller.poll(TIMEOUT)
        for fd, flag in events:
            # Retrieve the actual socket from its file descriptor
            s = fd_to_socket[fd]
            if flag & (select.POLLIN | select.POLLPRI):
                if s is server:
                    # A "readable" server socket is ready to accept a connection
                    try:
                        while True:
                            connection, client_address = s.accept()
                            connection.setblocking(0)
                            fd_to_socket[connection.fileno()] = connection
                            poller.register(connection.fileno(), READ_ONLY)

                            # Give the connection a queue for data we want to send
                            message_queues[connection] = Queue.Queue()
                            print_red(' connection {0} is comming ==> '.format(
                                connection.getpeername()))
                        pass
                    except socket.error:
                        pass
                else:
                    data = ''
                    try:
                        while True:
                            _data = s.recv(1024)
                            if not _data:
                                break
                            data += _data
                    except socket.error:
                        pass
                    if data:
                        print_red(' connection {0} is sending ==> '.format(
                            s.getpeername()))
                        message_queues[s].put(data.capitalize())
                        # Add output channel for response
                        poller.modify(s, READ_WRITE)
                    else:
                        # Interpret empty result as closed connection
                        print_red(' connection {0} is closed ==> '.format(
                            s.getpeername()))
                        # Stop listening for input on the connection
                        poller.unregister(s)
                        s.close()

                        # Remove message queue
                        del message_queues[s]
            elif flag & select.POLLHUP:
                # Client hung up
                print_red('connection {0} is closing ==> '.format(
                    s.getpeername()))
                # Stop listening for input on the connection
                poller.unregister(s)
                s.close()
            elif flag & select.POLLOUT:
                # Socket is ready to send data, if there is any to send.
                try:
                    next_msg = message_queues[s].get_nowait()
                except Queue.Empty:
                    # No messages waiting so stop checking for writability.
                    poller.modify(s, READ_ONLY)
                else:
                    print_red('connection {0} sending msg ==> '.format(
                        s.getpeername()))
                    try:
                        while next_msg:
                            bytelength = s.send(next_msg)
                            next_msg = next_msg[bytelength:]
                    except socket.error:
                        pass
            elif flag & select.POLLERR:
                print_red('connection {0} exceptional ==> '.format(
                    s.getpeername()))
                # Stop listening for input on the connection
                poller.unregister(s)
                s.close()

                # Remove message queue
                del message_queues[s]


if __name__ == '__main__':
    main()
