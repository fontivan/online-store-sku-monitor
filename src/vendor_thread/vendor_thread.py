import threading
import time

'''
TODO: Add header
'''
class VendorThread (threading.Thread):

    sleep_time = 60
    vendor = None

    '''
    TODO: Add header
    '''
    def __init__(self, vendor):
        self.vendor = vendor
        super().__init__()

    '''
    TODO: Add header
    '''
    def run(self):
        while True:
            self.vendor.check_stock_for_items()
            print('Checked all items for vendor \'{}\'... sleeping for \'{}\' seconds'.format(self.vendor.vendor_name, self.sleep_time))
            time.sleep(self.sleep_time)
