from bs4 import BeautifulSoup
import os
from vendor import Vendor

'''
TODO: Add header
'''
class MemoryExpress(Vendor):

    '''
    TODO: Add header
    '''
    def __init__(self, logger):
        super().__init__("Memory Express", os.getcwd() + "/vendors/memory_express", logger)

    '''
    TODO: Add header
    '''
    def parse_item_page(self, item_page_html, stores_to_check):

        stores_with_stock_information = BeautifulSoup(item_page_html, features="html.parser") \
            .body \
            .find_all('div', attrs={'class':'c-capr-inventory-store'})

        for s1 in stores_to_check:
            for s2 in stores_with_stock_information:
                if s1 in s2.text:
                    self.logger.debug(s2.text)
                    if not 'Out of Stock' in s2.text and not 'Backorder' in s2.text:
                        return self.in_stock_result

        return self.out_of_stock_result
