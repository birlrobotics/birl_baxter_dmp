#!/usr/bin/env python

import sys

import rospy

from multiprocessing import Queue
from traj_gen import TarjGen
from traj_exec import TarjExec

if __name__ == '__main__':
    com_queue = Queue()

    tg = TarjGen(com_queue)
    te = TarjExec(com_queue)

    te.start()
    import time
    time.sleep(5)
    tg.start()


    while not rospy.is_shutdown():
        pass

    tg.shutdown()
    te.shutdown()

