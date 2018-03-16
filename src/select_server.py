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

    # Sockets from which we expect to read
    inputs = [server]
    # Sockets to which we expect to write
    outputs = []
    # Outgoing message queues (socket:Queue)
    message_queues = {}

    while inputs:

        # Wait for at least one of the sockets to be ready for processing
        print_green(' waitting to recevie message from client')
        readable, writable, exceptional = select.select(inputs, outputs, inputs)  # noqa

        # Handle inputs
        for s in readable:
            if s is server:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                connection.setblocking(0)
                # 新 socket 加入读监听列表
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()
                print_red(' connection {0} is comming ==> '.format(connection.getpeername()))
            else:
                data = s.recv(1024)
                if data:
                    # 读取数据的 socket 加入输出列表
                    if s not in outputs:
                        outputs.append(s)
                    # 此 socket 数据积累
                    print_red(' connection {0} is sending ==> '.format(s.getpeername()))
                    message_queues[s].put(data.capitalize())
                else:
                    # client 关闭 socket
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    print_red(' connection {0} is closed ==> '.format(s.getpeername()))
                    s.close()

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                if s in outputs:
                    outputs.remove(s)
            else:
                s.send(next_msg)

        # Handle "exceptional conditions"
        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()


if __name__ == '__main__':
    main()