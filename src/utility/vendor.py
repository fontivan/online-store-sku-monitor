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

from abc import ABC, abstractmethod
import builtins
from concurrent.futures import as_completed
import time
import logging
import random

import requests
from requests_futures.sessions import FuturesSession


class Vendor(ABC):
    """
    TODO: Add header
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

    """
    TODO: Add header
    """

    def __init__(self, vendor_data, logger, alert):
        self.logger = logger
        self.vendor_name = vendor_data['name']
        self.items_to_check = vendor_data['skus']
        self.stores_to_check = vendor_data['locations']
        self.alert = alert
        self.session = FuturesSession()

    def log_msg(self, msg, log_level):
        """
        TODO: Add header
        """
        log = f"[[ {self.vendor_name} ]] :: {msg}"
        if log_level == logging.CRITICAL:
            self.logger.critical(log)
        elif log_level == logging.ERROR:
            self.logger.error(log)
        elif log_level == logging.WARNING:
            self.logger.warning(log)
        elif log_level == logging.INFO:
            self.logger.info(log)
        elif log_level == logging.DEBUG:
            self.logger.debug(log)

    def check_stock_for_items(self):
        """
        TODO: Add header
        """
        futures = []

        for item in self.items_to_check:
            try:
                future = self.session.get(item['url'], headers={
                    'User-Agent': str(random.choice(self.user_agent_headers))
                }, timeout=self.max_timeout)
                future.item = item
                futures.append(future)
            except builtins.Exception as e:
                raise e

        for future in as_completed(futures):
            try:
                response = future.result()
                if response.status_code == 200:
                    self.logger.debug(f"Raw response text: \n ----- {response.text} \n -----")
                    stock_result = self.parse_item_page(response.text, self.stores_to_check)
                    if stock_result == self.in_stock_result:
                        self.alert.send_alert(future.item, self.vendor_name)
                    elif stock_result == self.out_of_stock_result:
                        self.log_msg(
                            f"\'{future.item['name']}\' not in stock.",
                            logging.INFO
                        )
                    else:
                        raise ValueError('Unable to parse stock from webpage')
                else:
                    raise requests.HTTPError(f"Response code was \'{response.status_code}\'f")
            except builtins.Exception as e:
                self.log_msg(
                    f"An error occurred attempting to check stock for: \
                        \'{future.item['name']}\'. Caught exception: \'{str(e)}\'.",
                    logging.ERROR
                )
                time.sleep(self.max_timeout)
                raise e

    @abstractmethod
    def parse_item_page(self, item_page_html, stores_to_check):
        """
        TODO: Add header
        """
        raise NotImplementedError("This method should be overridden!")
