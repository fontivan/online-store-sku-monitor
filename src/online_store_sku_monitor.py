#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2020 fontivan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
TODO: Add header
"""

import logging
from datetime import datetime
import sys
from vendor_thread.vendor_thread import VendorThread
from vendors.amd import AMD
from vendors.best_buy import BestBuy
from vendors.canada_computers import CanadaComputers
from vendors.memory_express import MemoryExpress
# from vendors.newegg import Newegg


def configure_logger(log_to_file, log_to_stdout):
    """
    TODO: Add header
    """
    logger_name = "online-store-sku-monitor"
    logger = logging.getLogger(logger_name)
    # The global log level must be set lower then the level
    # of the messages going to /any/ output, hence DEBUG
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[[ %(asctime)s ]] :: [[ %(levelname)s ]] :: %(message)s')
    log_file_name = datetime.now().strftime('/tmp/online_store_sku_monitor_%H_%M_%d_%m_%Y.log')

    # Log to file
    if log_to_file:
        fh = logging.FileHandler(log_file_name, mode='w', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # Log to stdout
    if log_to_stdout:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def log_info(logger, msg):
    """
    TODO: Add header
    """
    logger.info(f"[[ Main ]] :: {msg}")


def main():
    """
    TODO: Add header
    """
    loop_forever = True
    log_to_stdout = True
    log_to_file = False

    logger = configure_logger(log_to_file, log_to_stdout)

    # Loop and do nothing since the threads will be running in the background
    try:
        # Save the thread data
        thread_list = []
        # Start a thread for each vendor
        log_info(logger, 'Starting threads for vendors...')
        thread_list.append(VendorThread(AMD(logger), logger, loop_forever, 75).start())
        thread_list.append(VendorThread(BestBuy(logger), logger, loop_forever, 45).start())
        thread_list.append(VendorThread(CanadaComputers(logger), logger, loop_forever, 45).start())
        # thread_list.append(VendorThread(Newegg(logger), logger, loop_forever, 75).start())
        thread_list.append(VendorThread(MemoryExpress(logger), logger, loop_forever, 75).start())
        log_info(logger, 'All threads started!')

        # Loop forever, just letting the threads run in the background
        while loop_forever:
            pass
    # Catch keyboard interrupt as the exit mechanism
    except KeyboardInterrupt:
        log_info(logger, 'Exiting on keyboard interrupt')
        sys.exit(0)


if __name__ == '__main__':
    main()
