from alert import Alert
import logging
import json
import os
import random
import requests
import time

'''
TODO: Add header
'''
class Vendor:

    alert = None
    logger = None
    in_stock_result = "IN_STOCK"
    items_json_path = None
    requests_timeout = 10 # seconds
    out_of_stock_result = "OUT_OF_STOCK"
    thread_delay = 2 # seconds
    user_agent_headers = [
        # Android agents
        "Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36",
        "Mozilla/5.0 (Android 9; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0",
        "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/10.2 Chrome/71.0.3578.99 Mobile Safari/537.36",
        # iOS agents
        "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
        # Linux agents
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
        "Mozilla/5.0 (SMART-TV; Linux; Tizen 2.4.0) AppleWebkit/538.1 (KHTML, like Gecko) SamsungBrowser/1.1 TV Safari/538.1",
        # macOS agents
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        # Windows agents
        "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
    ]
    vendor_name = None
    vendor_dir = None

    '''
    TODO: Add header
    '''
    def __init__(self, vendor_name, vendor_dir, logger):
        self.logger = logger
        self.vendor_name = vendor_name
        self.vendor_dir = vendor_dir
        self.items_json_path = self.vendor_dir + "/items.json"
        self.alert = Alert(logger)

    '''
    TODO: Add header
    '''
    def log_msg(self, msg, log_level):
        log = '[[ {} ]] :: {}'.format(self.vendor_name, msg)
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


    '''
    TODO: Add header
    '''
    def check_stock_for_items(self):
        if os.path.isfile(self.items_json_path):
            with open(self.items_json_path, 'r') as file:
                json_data = json.load(file)
                items_to_check = json_data['items']
                stores_to_check = json_data['stores']
                for item in items_to_check:
                    result = self.check_for_item(item, stores_to_check)
                    if result == self.in_stock_result:
                        self.alert.send_alert(item)
                    elif result == self.out_of_stock_result:
                        self.log_msg('\'{}\' not in stock.'.format(item['name']), logging.INFO)
                    else:
                        self.log_msg('An error occurred attempting to check stock for \'{}\'.'.format(item['name']), logging.WARNING)
                        time.sleep(self.thread_delay * 4)
                    time.sleep(self.thread_delay)
        else:
            self.log_msg('File not found at path \'{}\'.'.format(self.items_json_path), logging.ERROR)

    '''
    TODO: Add header
    '''
    def check_for_item(self, item, stores_to_check):
        html = self.make_url_request(item)
        if html:
            return self.parse_item_page(html, stores_to_check)
        return None

    '''
    TODO: Add header
    '''
    def make_url_request(self, item):
        request_headers = {
            'User-Agent': '{}'.format(random.choice(self.user_agent_headers))
        }
        try:
            request = requests.get(item['url'], headers = request_headers, timeout = self.requests_timeout)
            if request.status_code == 200:
                return request.text
            else:
                self.log_msg('Unable to get product page \'{}\''.format(item['url']), logging.ERROR)
        except Exception as e:
            self.log_msg('Caught requests exception \'{}\''.format(str(e)), logging.ERROR)

        return None

    '''
    TODO: Add header
    '''
    def parse_item_page(self, item_page_html, stores_to_check):
        return self.out_of_stock_result
