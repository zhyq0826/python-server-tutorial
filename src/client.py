import time
import socket
from threading import Thread


from util import print_red, print_green


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8000)
    print('connect to server {0}'.format(server_address))
    s.connect(server_address)
    print_green('sending data ==> ')
    msg = 'hello socket'
    # print(msg)
    s.send(msg)
    print_red('recving data <== ')
    msg = s.recv(1024)
    # print(msg)


def loop_n_times(n):
    for _ in range(n):
        main()


class ConcurrenceClient(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        loop_n_times(100)


if __name__ == '__main__':
    start = time.time()
    clients = []
    for _ in range(4):
        t = ConcurrenceClient()
        clients.append(t)
        t.start()

    for t in clients:
        t.join()

    print_green('time consume ==> ' + str(time.time() - start))
