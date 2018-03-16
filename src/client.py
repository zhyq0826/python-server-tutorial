import time
import socket
from threading import Thread


from util import print_red, print_green

THREAD_COUNT = 1
QS_P_THREAD = 1


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8000)
    print('connect to server {0}'.format(server_address))
    s.connect(server_address)
    msg = 'hello socket'
    print_green('sending data ==> ' + msg)
    s.send(msg)
    msg = s.recv(1024)
    print_red('recving data <== ' + msg)


def loop_n_times(n):
    for _ in range(n):
        main()
        time.sleep(3)


class ConcurrenceClient(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        loop_n_times(QS_P_THREAD)


if __name__ == '__main__':
    start = time.time()
    clients = []
    for _ in range(THREAD_COUNT):
        t = ConcurrenceClient()
        clients.append(t)
        t.start()

    for t in clients:
        t.join()

    print_green('time consume ==> ' + str(time.time() - start))
