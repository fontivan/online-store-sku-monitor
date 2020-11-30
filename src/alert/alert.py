from os import system

'''
TODO: Add header
'''
class Alert:

    '''
    TODO: Add header
    '''
    def send_alert(self, item):
        print('Item in stock \'{}\' at \'{}\''.format(item['name'], item['url']))
        system("spd-say ALERT")
