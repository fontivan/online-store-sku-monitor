from os import system

'''
TODO: Add header
'''
class Alert:

    logger = None

    def __init__(self, logger):
        self.logger = logger

    '''
    TODO: Add header
    '''
    def send_alert(self, item):
        self.logger.critical('Item in stock \'{}\' at \'{}\''.format(item['name'], item['url']))
        system('spd-say IN STOCK ALERT')
