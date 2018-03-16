from datetime import datetime
from colorama import init
init()

from colorama import Fore, Back, Style


def print_red(msg):
    print(Fore.RED + str(datetime.now()) + ' ' + msg)
    print(Fore.WHITE)


def print_green(msg):
    print(Fore.GREEN + str(datetime.now()) + ' ' + msg)
    print(Fore.WHITE)
