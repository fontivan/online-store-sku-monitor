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
This module encompasses functionality specific to BestBuyCA, a subclass of Vendor, 
focusing on operations pertinent to BestBuy Canada's online commerce analysis.
"""

from bs4 import BeautifulSoup
from src.utility.vendor import Vendor

class BestBuyCA(Vendor):
    """
    Subclass of Vendor designed for BestBuyCA operations, providing methods 
    tailored for parsing and analyzing BestBuy Canada's online commerce data.
    """

    def parse_item_page(self, item_page_html, stores_to_check):
        """
        Parses the HTML content of an item page to determine the availability 
        of the item on BestBuyCA.

        Args:
            item_page_html (str): The HTML content of the item page.
            stores_to_check (list): A list of online stores to check for the 
                                    item's availability.

        Returns:
            str: Result indicating the availability status of the item.
        """
        online_store = BeautifulSoup(item_page_html, features="html.parser") \
            .body \
            .find_all('span', attrs={'class': 'availabilityMessage_1MO75'})

        for span in online_store:
            self.logger.debug(span.text)
            if 'Available online' in span.text:
                return self.in_stock_result

        return self.out_of_stock_result
