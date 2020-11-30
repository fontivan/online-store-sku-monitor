#!/usr/bin/env python3

from datetime import datetime
import logging
from vendors.amd import AMD
from vendors.best_buy import BestBuy
from vendors.canada_computers import CanadaComputers
from vendors.newegg import Newegg
from vendors.memory_express import MemoryExpress
from vendor_thread.vendor_thread import VendorThread

'''
TODO: Add header
'''
def configure_logger(log_to_file, log_to_stdout):

    logger_name = "stockmonitor"
    logger = logging.getLogger(logger_name)
    # The global log level must be set lower then the level of the messages going to /any/ output, hence DEBUG
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[[ %(asctime)s ]] :: [[ %(levelname)s ]] :: %(message)s')
    log_file_name = datetime.now().strftime('/tmp/stockmonitor_%H_%M_%d_%m_%Y.log')

    # Log to file
    if log_to_file:
        fh = logging.FileHandler(log_file_name, mode = 'w', encoding = 'utf-8')
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

'''
TODO: Add header
'''
def main():

    logger = configure_logger(False, True)

    # Loop and do nothing since the threads will be running in the background
    try:
        # Start a thread for each vendor
        logger.info('Starting threads for vendors...')
        VendorThread(AMD(logger), logger).start()
        VendorThread(BestBuy(logger), logger).start(),
        VendorThread(CanadaComputers(logger), logger).start(),
        VendorThread(Newegg(logger), logger).start(),
        VendorThread(MemoryExpress(logger), logger).start()
        logger.info('All threads started!')

        # Loop forever, just letting the threads run in the background
        while True:
            pass
    # Catch keyboard interrupt as the exit mechanism
    except KeyboardInterrupt:
        logger.info('Exiting on keyboard interrupt')
        exit(0)

if __name__ == '__main__':
    main()
