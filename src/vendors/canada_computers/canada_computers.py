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

import os

from bs4 import BeautifulSoup
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
                    self.logger.debug(s2.text)
                    if not '-' in s2.text:
                        return self.in_stock_result

        return self.out_of_stock_result
