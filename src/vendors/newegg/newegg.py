from bs4 import BeautifulSoup
import os
from vendor import Vendor

'''
TODO: Add header
'''
class Newegg(Vendor):

    '''
    TODO: Add header
    '''
    def __init__(self, logger):
        super().__init__("Newegg", os.getcwd() + "/vendors/newegg", logger)

    '''
    TODO: Add header
    '''
    def parse_item_page(self, item_page_html, stores_to_check):

        online_store = BeautifulSoup(item_page_html, features="html.parser") \
            .body \
            .find_all('div', attrs={'class': 'product-buy'})

        for div in online_store:
            self.logger.debug(div.text)
            if 'Add to cart' in div.text:
                return self.in_stock_result

        return self.out_of_stock_result
