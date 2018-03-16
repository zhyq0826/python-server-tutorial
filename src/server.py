import socket
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
        client, address = s.accept()
        time.sleep(1)
        msg = client.recv(1024)
        client.send(msg.capitalize())
        client.close()


if __name__ == '__main__':
    main()
