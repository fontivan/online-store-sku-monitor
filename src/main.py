#!/usr/bin/env python3

from vendors.canada_computers import CanadaComputers
from vendors.memory_express import MemoryExpress
import threading

def thread_cc():
    canada_computers = CanadaComputers()
    canada_computers.check_stock_for_items()

def thread_me():
    memory_express = MemoryExpress()
    memory_express.check_stock_for_items()

'''
TODO: Add header
'''
def main():

    thread_pool = list()

    thread_pool.append(threading.Thread(target=thread_cc))
    thread_pool.append(threading.Thread(target=thread_me))

    for thread in thread_pool:
        thread.start()

if __name__ == '__main__':
    main()
