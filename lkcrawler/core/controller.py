# -*- coding: utf-8 -*-
import os
import sys
import time
import pickle
import logging
from selenium.common.exceptions import \
    NoSuchElementException, WebDriverException

from lkcrawler.core.browser import Browser

reload(sys)
sys.setdefaultencoding('utf8')


class Controller:
    def __init__(self, auth, cookies_path=None, log_path=None,
                 sleep_time=0.05, debug=False):
        self.base_url = 'https://www.linkedin.com'
        self.username = auth['email']
        self.password = auth['password']
        self.cookies_path = cookies_path
        self.cookies_file = '{}/{}.pickle'.format(self.cookies_path,
                                                  self.username)
        self.sleep_time = sleep_time
        self.browser = Browser(log_path=log_path, proxy=None)
        if debug:
            self.logger = logging.basicConfig(
                format='%(asctime)s - %(message)s',
                level=logging.DEBUG)

    def login(self):
        """
        :return:
        """
        try:
            self.browser.open(self.base_url)
            time.sleep(self.sleep_time)

            if not os.path.exists(self.cookies_file) \
                    or (os.path.exists(self.cookies_file)
                        and os.path.getsize(self.cookies_file) < 1):

                username_element = self.browser.element_by_id('login-email')
                password_element = self.browser.element_by_id('login-password')

                username_element.send_keys(self.username)
                password_element.send_keys(self.password)
                self.browser.element_by_id('login-submit').click()

                time.sleep(self.sleep_time)

                os.makedirs(self.cookies_path)
                pickle.dump(self.browser.get_cookies(),
                            open(self.cookies_file, "wb"))

            else:
                cookies = pickle.load(open(self.cookies_file, "rb"))
                for cookie in cookies:
                    self.browser.set_cookie(cookie)

                time.sleep(self.sleep_time)

        except (WebDriverException, NoSuchElementException) as e:
            print str(e)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)

    def get_profile(self, profile_url):
        """
        :param profile_url:
        :return:
        """
        result = None
        try:
            self.login()
            self.browser.open(profile_url)
            self.browser.driver.execute_script("window.scrollTo(0, 1000);")
            time.sleep(self.sleep_time)
            result = self.browser.html()
        except (WebDriverException, NoSuchElementException) as e:
            print str(e)
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)
        finally:
            return result
