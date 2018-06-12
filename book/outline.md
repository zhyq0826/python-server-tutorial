每种 web server 的缺点是什么，基于此缺点进行进化，进化的目的就是为了改掉缺点

实现一个 Python 通用线程池来模拟多线程模型

高性能的 web server 

c10k 问题 http://www.kegel.com/c10k.html 提供了很多资源从不同的角度提高 web server 的 性能

- 多线程
- 多进程
- 协成
- 上下文切换
- 数据 copy


https://docs.python.org/2/library/select.html#polling-objects
The poll() system call, supported on most Unix systems, provides better scalability for network servers that service many, many clients at the same time. poll() scales better because the system call only requires listing the file descriptors of interest, while select() builds a bitmap, turns on bits for the fds of interest, and then afterward the whole bitmap has to be linearly scanned again. select() is O(highest file descriptor), while poll() is O(number of file descriptors).