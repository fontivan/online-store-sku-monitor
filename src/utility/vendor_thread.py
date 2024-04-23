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
This module contains the VendorThread class, which represents a thread
responsible for continuously checking the stock status of items for a specific vendor.
"""

import time
import logging
import random
import threading


class VendorThread(threading.Thread):
    """
    Thread class for continuously checking the stock status of items for
    a specific vendor.
    """

    vendor = None
    logger = None
    config = None

    def __init__(self, vendor, logger, config):
        """
        Initializes the VendorThread with the specified vendor, logger,
        and configuration.

        Args:
            vendor: The vendor object to be monitored.
            logger: The logger object for logging messages.
            config: Configuration settings for the thread.
        """
        self.vendor = vendor
        self.logger = logger
        self.config = config

        super().__init__(daemon=config['loop_forever'])

    def run(self):
        """
        Executes the thread's main loop for checking the stock status of items.
        """
        self.vendor.log_msg(
            f"Daemon thread \'{self.name}\' started for vendor.",
            logging.INFO
        )
        while True:
            self.vendor.check_stock_for_items()
            if not self.config['loop_forever']:
                break
            generated_time = self.config['sleep_timer'] + \
                random.randrange(self.config['sleep_range_rng_spread'])
            self.vendor.log_msg(
                f"Checked all items for vendor, sleeping for \'{generated_time}\' seconds.",
                logging.INFO
            )
            time.sleep(generated_time)
