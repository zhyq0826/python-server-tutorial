import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8000)
    print('connect to server {0}'.format(server_address))
    s.connect(server_address)
    print('sending data')
    s.send('hello socket')


if __name__ == '__main__':
    main()
