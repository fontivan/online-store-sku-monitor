import logging
import threading
import time

'''
TODO: Add header
'''
class VendorThread (threading.Thread):

    sleep_time = 60
    vendor = None
    logger = None
    loop_forever = True

    '''
    TODO: Add header
    '''
    def __init__(self, vendor, logger, loop_forever):
        self.logger = logger
        self.vendor = vendor
        self.loop_forever = loop_forever
        super().__init__(daemon=loop_forever)

    '''
    TODO: Add header
    '''
    def run(self):
        self.vendor.log_msg('Daemon thread started for vendor', logging.INFO)
        while True:
            self.vendor.check_stock_for_items()
            if not self.loop_forever:
                break
            self.vendor.log_msg('Checked all items for vendor, sleeping for \'{}\' seconds'.format(self.sleep_time), logging.INFO)
            time.sleep(self.sleep_time)
