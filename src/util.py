from colorama import init
init()

from colorama import Fore, Back, Style


def print_red(msg):
    print(Fore.RED + '' + msg)
    print(Fore.WHITE)


def print_green(msg):
    print(Fore.GREEN + '' + msg)
    print(Fore.WHITE)
