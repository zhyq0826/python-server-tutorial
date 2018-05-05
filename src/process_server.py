import socket
import os
import time
from datetime import datetime

from util import print_red, print_green


def main():
    # create tcp socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # enable reuse address port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind socket to the port
    server_address = ('localhost', 8000)
    s.bind(server_address)
    s.listen(10)
    while 1:
        print_green(' waitting to recevie message from client')
        connection, address = s.accept()
        if not os.fork():   # enter child process
            time.sleep(1)   # exec task in 3 seconds
            msg = connection.recv(1024)
            print_red("child process")
            connection.send(msg.capitalize())
            connection.close()      # close client socket
            s.close()       # child does not need this
            break           # break child while loop
        connection.close()      # parent does not need this


if __name__ == '__main__':
    main()
