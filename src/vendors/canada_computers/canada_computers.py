from bs4 import BeautifulSoup
import os
from vendor import Vendor

'''
TODO: Add header
'''
class CanadaComputers(Vendor):

    '''
    TODO: Add header
    '''
    def __init__(self, logger):
        super().__init__("Canada Computers", os.getcwd() + "/vendors/canada_computers", logger)

    '''
    TODO: Add header
    '''
    def parse_item_page(self, item_page_html, stores_to_check):

        stock_info_div = BeautifulSoup(item_page_html, features="html.parser") \
            .body \
            .find('div', attrs={'class': 'stocklevel-pop'})

        rejoined_html = "".join(str(v) for v in stock_info_div.contents)

        stores_with_stock_information = BeautifulSoup(rejoined_html, features="html.parser") \
            .find_all('div', attrs={'class': 'row'})

        for s1 in stores_to_check:
            for s2 in stores_with_stock_information:
                if s1 in s2.text:
                    if not '-' in s2.text:
                        return self.in_stock_result

        return self.out_of_stock_result
