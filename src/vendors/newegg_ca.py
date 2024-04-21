# MIT License
#
# Copyright (c) 2020-2024 fontivan
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

from bs4 import BeautifulSoup
from src.utility.vendor import Vendor

class NeweggCA(Vendor):
    """
    TODO: Add header
    """

    def parse_item_page(self, item_page_html, stores_to_check):
        """
        TODO: Add header
        """
        online_store = BeautifulSoup(item_page_html, features="html.parser") \
            .body \
            .find_all('div', attrs={'class': 'product-buy'})

        for div in online_store:
            self.logger.debug(div.text)
            if 'Add to cart' in div.text:
                return self.in_stock_result

        return self.out_of_stock_result
