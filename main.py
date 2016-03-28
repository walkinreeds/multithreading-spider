# coding: utf-8
# Author: RaPoSpectre
# Create: 2016-03-25


from __future__ import unicode_literals

from ProxyProducer import KuaiProducer, LiuLiuProducer, XiCiProducer
from ProxyConsumer import SpiderConsumer
from CheckConsumer import CheckConsumer, ProcessWorker

import Queue
import time


def main():
    ts = time.time()
    queue = Queue.Queue()
    ip_queue = Queue.Queue()
    number_queue = Queue.Queue()
    available_queue = Queue.Queue()
    # kuai = KuaiProducer(queue, pages=10)
    liu = LiuLiuProducer(queue, pages=1)
    xi = XiCiProducer(queue)

    # xi.start()
    liu.start()
    # xi.start()
    print '\n开始地址抓取:\n'
    time.sleep(3)
    worker = ProcessWorker(cq=queue, total=queue.qsize())
    worker.start()
    for i in range(1, 17):
        spider = SpiderConsumer(q=queue, cq=ip_queue, nq=number_queue, name='spider{0}'.format(i))
        spider.daemon = True
        spider.start()

    queue.join()
    # time.sleep(3)
    # print ip_queue.qsize()
    total_addr = 0
    total_addr = 0
    available_addr = 0
    while not number_queue.empty():
        total_addr += number_queue.get()
    check_list = []
    print '\n开始地址检查:\n'
    worker = ProcessWorker(cq=ip_queue, total=total_addr)
    worker.start()
    for c in range(1, 49):
        check = CheckConsumer(ip_queue, name='check{0}'.format(c))
        check_list.append(check)
        check.start()
    ip_queue.join()
    print '\n开始地址写入:\n'
    with open('proxy.txt', 'a+') as f1:
        for check in check_list:
            for itm in check.available_list:
                available_addr += 1
                f1.writelines('{0}\n'.format(itm))
            check.stop()
    print('\n共抓取 {0} 个地址, 可用 {1} 个地址, 耗时 {2}s'.format(total_addr, available_addr, round(time.time() - ts), 2))


if __name__ == '__main__':
    main()
