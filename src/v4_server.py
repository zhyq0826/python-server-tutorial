import socket
import time
from datetime import datetime
import threading

from util import print_red, print_green

lock = threading.Lock()
GLOBAL_REQUEST_STATE = {
    'count': 0
}


def process_client_request(client):
    time.sleep(1)   # exec task in 3 seconds
    msg = client.recv(1024)
    print_red("thread %s" % threading.current_thread().name)
    client.send(msg.capitalize())
    client.close()      # close client socket
    with lock:
        GLOBAL_REQUEST_STATE['count'] += 1


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
        print_green(
            str(datetime.now()) + ' waitting to recevie message from client')
        client, address = s.accept()
        t = threading.Thread(target=process_client_request, args=(client,))
        t.daemon = True
        t.start()


if __name__ == '__main__':
    main()
