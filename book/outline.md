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


## level trigger

被监控的文件描述符有读写事件发生时，如果一次没有把数据读写完毕，下次 epoll 会继续返回上次没有处理完成的文件描述符，极端情况下，如果某个文件描述符一直不处理 epoll 会一直返回，直到文件描述符的数据被读写完成。

## edge trigger

被监控的文件描述符有读写事件发生时，epoll 只会通知一次，处理程序必须一次处理完成和此次读写事件相关联的所有数据，直到出现 socket Error (在非阻塞模式下，没有数据可读时返回错误)，之后文件描述符又继续在下次读写事件发生时返回，重复这一过程。

## level trigger 和 edge trigger 的不同

二者的差别就在于 edge trigger 只有在有读写事件出现时才返回文件描述符，不论此次读写事件关联多少数据都必须一次性处理完成，而 level trigger 则是有读写事件时会返回，文件描述符关联的数据没有处理完成时也会返回，也就是 level-trigger 比 edge trigger 做了很多的关于数据是否处理完成的校验工作。

## select 的不足

- select的一个缺点在于单个进程能够监视的文件描述符的数量存在最大限制
- 另外，select()所维护的存储大量文件描述符的数据结构，随着文件描述符数量的增大，其复制的开销也线性增长。同时，由于网络响应时间的延迟使得大量TCP连接处于非活跃状态，但调用select()会对所有socket进行一次线性扫描，所以这也浪费了一定的开销。


## epoll 的优点

epoll可以同时支持水平触发和边缘触发（Edge Triggered，只告诉进程哪些文件描述符刚刚变为就绪状态，它只说一遍，如果我们没有采取行动，那么它将不会再次告知，这种方式称为边缘触发），理论上边缘触发的性能要更高一些，但是代码实现相当复杂。

epoll同样只告知那些就绪的文件描述符，而且当我们调用epoll_wait()获得就绪文件描述符时，返回的不是实际的描述符，而是一个代表就绪描述符数量的值，你只需要去epoll指定的一个数组中依次取得相应数量的文件描述符即可，这里也使用了内存映射（mmap）技术，这样便彻底省掉了这些文件描述符在系统调用时复制的开销。

另一个本质的改进在于epoll采用基于事件的就绪通知方式。在select/poll中，进程只有在调用一定的方法后，内核才对所有监视的文件描述符进行扫描，而epoll事先通过epoll_ctl()来注册一个文件描述符，一旦基于某个文件描述符就绪时，内核会采用类似callback的回调机制，迅速激活这个文件描述符，当进程调用epoll_wait()时便得到通知。


## 高性能服务器分析

- tornado
- gunicorn
- libevent
- libuv
- nginx
- java disruptor、false sharding、并发无锁、ring buffer
- tcp_nodelay,nio
- 内存池、对象池、数据结构
- 磁盘尾部追加、LSM

