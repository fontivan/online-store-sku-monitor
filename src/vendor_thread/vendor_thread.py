import logging
import random
import threading
import time

'''
TODO: Add header
'''
class VendorThread (threading.Thread):

    sleep_time = None
    vendor = None
    logger = None
    loop_forever = True

    '''
    TODO: Add header
    '''
    def __init__(self, vendor, logger, loop_forever, sleep_time):
        self.logger = logger
        self.vendor = vendor
        self.loop_forever = loop_forever
        self.sleep_time = sleep_time
        super().__init__(daemon=loop_forever)

    '''
    TODO: Add header
    '''
    def run(self):
        self.vendor.log_msg('Daemon thread \'{}\' started for vendor'.format(self.getName()), logging.INFO)
        while True:
            self.vendor.check_stock_for_items()
            if not self.loop_forever:
                break
            generated_time = self.sleep_time + random.randrange(20)
            self.vendor.log_msg('Checked all items for vendor, sleeping for \'{}\' seconds'.format(generated_time), logging.INFO)
            time.sleep(generated_time)
