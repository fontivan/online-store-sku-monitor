#!/usr/bin/env python3

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
This script orchestrates the monitoring of online store SKUs by initializing 
vendor threads and managing logging and configuration.
"""

import logging
from datetime import datetime
import os
import sys
import time
import yaml

# Update path so that imports can use full module path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# pylint: disable=wrong-import-position
from src.utility.alert import Alert
from src.utility.vendor_thread import VendorThread
from src.vendors.amd_ca import AMDCA
from src.vendors.bestbuy_ca import BestBuyCA
from src.vendors.canadacomputers_ca import CanadaComputersCA
from src.vendors.memoryexpress_ca import MemoryExpressCA
from src.vendors.newegg_ca import NeweggCA
# pylint: enable=wrong-import-position

def configure_logger(config):
    """
    Configures the logger based on the provided configuration settings.

    Args:
        config: The configuration settings for logging.

    Returns:
        logger: The configured logger object.
    """
    logger_name = "online-store-sku-monitor"
    logger = logging.getLogger(logger_name)
    # Set global log level to DEBUG
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[[ %(asctime)s ]] :: [[ %(levelname)s ]] :: %(message)s')
    log_file_name = datetime.now().strftime('/tmp/online_store_sku_monitor_%H_%M_%d_%m_%Y.log')

    # Log to file if enabled
    if config['log_to_file']:
        fh = logging.FileHandler(log_file_name, mode='w', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # Log to stdout if enabled
    if config['log_to_stdout']:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def log_info(logger, msg):
    """
    Logs an informational message with the specified logger.

    Args:
        logger: The logger object.
        msg: The message to be logged.
    """
    logger.info(f"[[ Main ]] :: {msg}")


def main():
    """
    Main function for executing the script.
    """
    # Try to load configuration from file, set defaults if it fails
    config = {
        "loop_forever": True,
        "log_to_stdout": True,
        "log_to_file": False,
        "sleep_timer": 60,
        "sleep_range_rng_spread": 20,
        "voice_alerts": True
    }
    try:
        with open('config.yaml', 'r', encoding='UTF-8') as config_file:
            yaml_config = config_file.read()
            read_config = yaml.load(yaml_config, Loader=yaml.SafeLoader)
            config = read_config
    except (FileNotFoundError, PermissionError):
        pass

    logger = configure_logger(config)
    alert = Alert(logger, config)

    try:
        # Open data file
        with open('data.yaml', 'r', encoding='UTF-8') as data_file:
            yaml_text = data_file.read()
            data = yaml.load(yaml_text, Loader=yaml.SafeLoader)['data']

        # Save the thread data
        thread_list = []

        # Loop over data
        for store in data:
            if store['enabled']:
                match(store['name']):
                    case 'amd_ca':
                        thread_list.append(
                            VendorThread(
                                AMDCA(store, logger, alert),
                                logger,
                                config
                            )
                        )
                    case 'bestbuy_ca':
                        thread_list.append(
                            VendorThread(
                                BestBuyCA(store, logger, alert),
                                logger,
                                config
                            )
                        )
                    case 'canadacomputers_ca':
                        thread_list.append(
                            VendorThread(
                                CanadaComputersCA(store, logger, alert),
                                logger,
                                config
                            )
                        )
                    case 'newegg_ca':
                        thread_list.append(
                            VendorThread(
                                NeweggCA(store, logger, alert),
                                logger,
                                config
                            )
                        )
                    case 'memoryexpress_ca':
                        thread_list.append(
                            VendorThread(
                                MemoryExpressCA(store, logger, alert),
                                logger,
                                config
                            )
                        )
                    case _:
                        logger.error("Unknown store: \'%s\'", store['name'])
            else:
                logger.info("Store \'%s\' not enabled.", {store['name']})

        # Start all the threads
        for thread in thread_list:
            thread.start()

        # Loop forever, letting the threads run in the background
        while config['loop_forever']:
            time.sleep(999999999)
    # Catch keyboard interrupt for exit
    except KeyboardInterrupt:
        log_info(logger, 'Exiting on keyboard interrupt')
        sys.exit(0)


if __name__ == '__main__':
    main()
