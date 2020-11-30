from bs4 import BeautifulSoup
import os
from vendor import Vendor

'''
TODO: Add header
'''
class AMD(Vendor):

    '''
    TODO: Add header
    '''
    def __init__(self, logger):
        super().__init__("AMD", os.getcwd() + "/vendors/amd", logger)

    '''
    TODO: Add header
    '''
    def parse_item_page(self, item_page_html, stores_to_check):

        online_store = BeautifulSoup(item_page_html, features="html.parser") \
            .body \
            .find_all('p', attrs={'class': 'product-out-of-stock'})

        if len(online_store) == 0:
            return self.in_stock_result

        return self.out_of_stock_result
