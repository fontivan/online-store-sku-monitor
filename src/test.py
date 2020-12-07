import requests
import time

base_url = 'https://www.amd.com/en/direct-buy/'
suffix = 'ca'
user_agent = 'Mozilla/5.0 (Linux; Android 7.1.2; AFTMM Build/NS6265; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.110 Mobile Safari/537.36'

for i in range(0, 100):
    product_code = '545837{}00'.format(str(i).zfill(2))
    print('Testing: \'{}\''.format(product_code))
    r = requests.get('{}/{}/{}'.format(
            base_url,
            product_code,
            suffix
            ),
            headers={'User-Agent': user_agent},
            timeout=15
    )
    print(r.text)
    if '6900XT' in r.text:
        print('Found => ', product_code, ':', r.status_code)
    #time.sleep(1)    
exit(0)

