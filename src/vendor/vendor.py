import json
import os
import requests
from alert import Alert

'''
TODO: Add header
'''
class Vendor:

    alert = Alert()
    vendor_name = ""
    vendor_dir = ""
    items_json_path = ""
    out_of_stock_result = "OUT_OF_STOCK"
    in_stock_result = "IN_STOCK"

    '''
    TODO: Add header
    '''
    def __init__(self, vendor_name, vendor_dir):
        self.vendor_name = vendor_name
        self.vendor_dir = vendor_dir
        self.items_json_path = self.vendor_dir + "/items.json"

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
                    if result != self.out_of_stock_result:
                        self.alert.send_alert(item)
                    else:
                        print("Item '" + item['name'] +"' not in stock at vendor '" + self.vendor_name + "'.")
        else:
            print("File not found: '" + self.items_json_path + "'.")

    '''
    TODO: Add header
    '''
    def check_for_item(self, item, stores_to_check):
        return self.parse_item_page(self.make_url_request(item), stores_to_check)

    '''
    TODO: Add header
    '''
    def make_url_request(self, item):
        request = requests.get(item['url'])
        if request.status_code == 200:
            return request.text
        else:
            raise Exception("Unable to get product page: '" + item['url'] + '.')

    '''
    TODO: Add header
    '''
    def parse_item_page(self, item_page_html, stores_to_check):
        return self.out_of_stock_result
