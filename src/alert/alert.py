from os import system

'''
TODO: Add header
'''
class Alert:

    '''
    TODO: Add header
    '''
    def send_alert(self, item):
        text = "Item in stock: '" + item['name'] + "' at '" + item['url'] + "'."
        print(text)
        system("spd-say ALERT")
