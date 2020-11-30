#!/usr/bin/env python3

from vendors.canada_computers import CanadaComputers
from vendors.memory_express import MemoryExpress
from vendors.best_buy import BestBuy
from vendor_thread.vendor_thread import VendorThread

'''
TODO: Add header
'''
def main():

    # Start a thread for each vendor
    VendorThread(CanadaComputers()).start()
    VendorThread(MemoryExpress()).start()
    VendorThread(BestBuy()).start()

    # Loop and do nothing since the threads will be running in the background
    try:
        while True:
            pass
    except KeyboardInterrupt:
        exit(0)

if __name__ == '__main__':
    main()
