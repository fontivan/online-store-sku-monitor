# MIT License
#
# Copyright (c) 2020-2025 fontivan
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
This module contains functionalities specific to CanadaComputersCA, a subclass 
of Vendor, focusing on operations related to parsing and analyzing Canada Computers'
online commerce data.
"""

from bs4 import BeautifulSoup
from src.utility.parse_exception import ParseException
from src.utility.vendor import Vendor


class CanadaComputersCA(Vendor):
    """
    Subclass of Vendor tailored for CanadaComputersCA operations, 
    providing methods for parsing and analyzing Canada Computers' online commerce data.
    """

    def parse_item_page(self, item_page_html, stores_to_check):
        """
        Parses the HTML content of an item page to determine the availability
        of the item on CanadaComputersCA.

        Args:
            item_page_html (str): The HTML content of the item page.
            stores_to_check (list): A list of online stores to check for the
                                    item's availability.

        Returns:
            str: Result indicating the availability status of the item.
        """

        try:
            # Use the store pickup modal info
            # their use the misspelled id 'checkothertores' instead of 'checkotherstores
            check_other_stores_div = BeautifulSoup(item_page_html, features='html.parser') \
                .find('div', attrs={'id': 'checkothertores'})

            rejoined_html = "".join(str(v) for v in check_other_stores_div.contents)

            # Always check the online store
            online_box = BeautifulSoup(rejoined_html, features='html.parser') \
                .find('div', attrs={'class': 'online-box'}) \
                .text

            online_in_stock_count = online_box.split("Online")[-1].strip()

            # Check for stock number
            if online_in_stock_count != '0':
                return self.in_stock_result, 'Web store'

            # Get store data
            store_divs = BeautifulSoup(rejoined_html, features='html.parser') \
                .findAll('div', attrs={'class': 'row'})

            # Loop over the stores
            for s1 in stores_to_check:
                for s2 in store_divs:
                    if s1 in s2.text:
                        in_store_count = s2.text.split(s1)[-1].strip().split(' ')[0].strip()
                        if in_store_count != '0':
                            return self.in_stock_result, s1
        except Exception as e:
            raise ParseException from e

        return self.out_of_stock_result, None
