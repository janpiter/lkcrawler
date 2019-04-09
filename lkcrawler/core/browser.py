import os
import random
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


class Browser:
    user_agent_list = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) '
        'Gecko/20100101 Firefox/40.1',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
        'AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3'
        ' Safari/7046A194A',
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/42.0.2311.135 '
        'Safari/537.36 Edge/12.246'
    ]

    def __init__(self, log_path=None, proxy=None):
        self.log_path = log_path
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(
            # executable_path='/usr/local/bin/chromedriver',
            # service_log_path='{}/ghostdriver.log'.format(self.browser_log()),
            chrome_options=chrome_options)
        # self.driver.set_window_size(1366, 768)

    def open(self, url):
        self.driver.get(url)

    def html(self):
        return self.driver.page_source

    def close(self):
        self.driver.close()

    def element_by_id(self, value):
        return self.driver.find_element_by_id(value)

    def element_by_css(self, value):
        return self.driver.find_element_by_css_selector(value)

    def element_by_name(self, value):
        return self.driver.find_element_by_name(value)

    def get_cookies(self):
        return self.driver.get_cookies()

    def set_cookie(self, cookie):
        self.driver.add_cookie(cookie)

    def browser_log(self):
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)

    def desired_capabilities(self):
        d_cap = dict(DesiredCapabilities.PHANTOMJS)
        d_cap["phantomjs.page.settings.userAgent"] = (
            random.choice(self.user_agent_list))
        return d_cap

    @staticmethod
    def set_proxy(proxy):
        service_args = []
        if proxy:
            proxy_host = proxy['host']
            proxy_port = proxy['port']
            proxy_type = proxy['type']
            proxy_host = '{}:{}'.format(proxy_host, proxy_port) \
                if proxy_port else proxy_host
            proxy_type = 'http' if proxy_type == '' else proxy_type
            service_args = ['--proxy={}'.format(proxy_host),
                            '--proxy-type={}'.format(proxy_type)]
        return service_args
