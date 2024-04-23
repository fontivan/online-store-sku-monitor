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
This module contains functionalities specific to MemoryExpressCA,
a subclass of Vendor, focusing on operations related to parsing and 
analyzing Memory Express' online commerce data.
"""

from bs4 import BeautifulSoup
from src.utility.vendor import Vendor


class MemoryExpressCA(Vendor):
    """
    Subclass of Vendor tailored for MemoryExpressCA operations, providing 
    methods for parsing and analyzing Memory Express' online commerce data.
    """

    def parse_item_page(self, item_page_html, stores_to_check):
        """
        Parses the HTML content of an item page to determine the availability
        of the item on MemoryExpressCA.

        Args:
            item_page_html (str): The HTML content of the item page.
            stores_to_check (list): A list of online stores to check for the
                                    item's availability.

        Returns:
            str: Result indicating the availability status of the item.
        """
        stores_with_stock_information = BeautifulSoup(item_page_html, features="html.parser") \
            .body \
            .find_all('div', attrs={'class': 'c-capr-inventory-store'})

        for s1 in stores_to_check:
            for s2 in stores_with_stock_information:
                if s1 in s2.text:
                    self.logger.debug(s2.text)
                    if 'Out of Stock' not in s2.text and 'Backorder' not in s2.text:
                        return self.in_stock_result

        return self.out_of_stock_result
