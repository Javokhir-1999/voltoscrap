import random
from time import sleep

class Base:
    driver = None
    def __init__(self):
        self.driver = self.driver()
        self.driver.get('https://www.facebook.com/')

    def driver(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from fp.fp import FreeProxy
        proxy = FreeProxy(country_id=['US']).get()

        service = Service()
        options = webdriver.FirefoxOptions()
        options.add_argument('--proxy-server=%s' % proxy)

        driver = webdriver.Firefox(service=service, options=options)
        print('proxy:', proxy)
        return driver
        
    def slp(self):
        return sleep(random.randint(2,3))

    def scroll_range(self):
        return random.randint(random.randint(180, 290), random.randint(291, 400))
    
    def quit(self):
        self.driver.quit()