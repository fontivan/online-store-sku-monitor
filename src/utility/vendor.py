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
This module encompasses functionalities related to the Vendor abstract class,
providing a foundation for implementing vendor-specific operations in online
commerce analysis.
"""

from abc import ABC, abstractmethod
import builtins
from concurrent.futures import as_completed
import time
import logging
import random

import requests
from requests_futures.sessions import FuturesSession

from src.utility.parse_exception import ParseException


class Vendor(ABC):
    """
    Abstract base class for vendor-specific operations in online commerce analysis.
    """

    alert = None
    logger = None
    in_stock_result = "IN_STOCK"
    items_json_path = None
    items_to_check = []
    max_timeout = 15  # seconds'
    out_of_stock_result = "OUT_OF_STOCK"
    session = None
    stores_to_check = []
    user_agent_headers = [
        # Android agents
        "Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
                Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36",
        "Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0",
        "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G960U) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
                SamsungBrowser/10.2 Chrome/71.0.3578.99 Mobile Safari/537.36",
        # iOS agents
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) \
            AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) \
            AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) \
            AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
        # Linux agents
        "Mozilla/5.0 (X11; Linux x86_64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) \
            Gecko/20100101 Firefox/65.0",
        "Mozilla/5.0 (SMART-TV; Linux; Tizen 2.4.0) \
            AppleWebkit/538.1 (KHTML, like Gecko) SamsungBrowser/1.1 TV Safari/538.1",
        # macOS agents
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) \
            AppleWebKit/605.1.15 (KHTML, like Gecko)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) \
            AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        # Windows agents
        "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; \
            Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
    ]
    vendor_name = None

    def __init__(self, vendor_data, logger, alert):
        self.logger = logger
        self.vendor_name = vendor_data['name']
        # Will be initialized in the function call
        self.items_to_check = []
        self._filter_items(vendor_data['skus'])
        self.stores_to_check = vendor_data['locations']
        self.alert = alert
        self.session = FuturesSession()

    def log_msg(self, msg, log_level):
        """
        Logs a message at the specified log level, prefixed with the vendor's name.

        Args:
            msg (str): The message to be logged.
            log_level (int): The log level at which the message should be logged.
        """
        log = f"[[ {self.vendor_name} ]] :: {msg}"

        match(log_level):
            case(logging.CRITICAL):
                self.logger.critical(log)
            case(logging.ERROR):
                self.logger.error(log)
            case(logging.WARNING):
                self.logger.warning(log)
            case(logging.INFO):
                self.logger.info(log)
            case(logging.DEBUG):
                self.logger.debug(log)

    def _filter_items(self, vendor_data):
        for item in vendor_data:
            if item['enabled'] is True:
                self.log_msg(
                    f"Item \'{item['name']}\' added to check list.",
                    logging.INFO)
                self.items_to_check.append(item)
            else:
                self.log_msg(
                    f"Item \'{item['name']}\' is not enabled.",
                    logging.INFO)

    def _initialize_futures(self):
        """
        TODO: Fill this in
        """

        # Initialize the list
        futures = []

        # Create the futures based on the items to be checked
        for item in self.items_to_check:
            try:
                future = self.session.get(item['url'], allow_redirects=False, headers={
                    'User-Agent': str(random.choice(self.user_agent_headers))
                }, timeout=self.max_timeout)
                future.item = item
                futures.append(future)
            except builtins.Exception as e:
                raise e
        return futures

    def _process_futures(self, futures):
        """
        TODO: Fill this in
        """

        # Loop over all the futures and process them
        for future in as_completed(futures):
            try:
                response = future.result()
                if response.status_code == 200:
                    self.logger.debug(f"Raw response text: \n ----- {response.text} \n -----")
                    stock_result, location = self.parse_item_page(response.text, self.stores_to_check)
                    if stock_result == self.in_stock_result:
                        self.alert.send_alert(future.item, self.vendor_name, location)
                    elif stock_result == self.out_of_stock_result:
                        self.log_msg(
                            f"\'{future.item['name']}\' not in stock.",
                            logging.INFO
                        )
                    else:
                        raise ParseException
                else:
                    self.log_msg(
                        f"Response code was \'{response.status_code}\' for \'{future.item['name']}\'",
                        logging.WARN
                    )
                    continue
            except ParseException:
                self.log_msg(
                    f"Failed to parse page contents for: \
                        \'{future.item['name']}\'. Will try again later.",
                        logging.ERROR
                )
                time.sleep(self.max_timeout)
            except requests.exceptions.Timeout:
                self.log_msg(
                    f"Timeout attempting to check stock for: \
                        \'{future.item['name']}\'. Will try again later.",
                        logging.WARN
                )
                time.sleep(self.max_timeout)
            except builtins.Exception as e:
                self.log_msg(
                    f"An error occurred attempting to check stock for: \
                        \'{future.item['name']}\'. Caught exception: \'{str(e)}\'.",
                    logging.ERROR
                )
                time.sleep(self.max_timeout)
                raise e from e

    def check_stock_for_items(self):
        """
        Checks the stock availability for items asynchronously.
        """
        futures = self._initialize_futures()
        self._process_futures(futures)

    @abstractmethod
    def parse_item_page(self, item_page_html, stores_to_check):
        """
        Parses the HTML content of an item page to determine the availability of the item.

        Args:
            item_page_html (str): The HTML content of the item page.
            stores_to_check (list): A list of stores to check for the item's availability.

        Returns:
            str: Result indicating the availability status of the item.
        """
        raise NotImplementedError("This method should be overridden!")
