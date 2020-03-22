'''
Selenium Testing Tools
'''

from DockerTestFramework.data_classes import ENVars
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, ErrorInResponseException, TimeoutException
import time


class SeleniumTools:
    data: ENVars
    options: []
    driver: None

    def __init__(self, data: ENVars = None):
        if data is None:
            raise Exception('SeleniumTools Should not be called without ENVars object as the argument.')
        else:
            self.data = data
        self.options = ['--no-sandbox',
                        '--headless',
                        '--disable-gpu',
                        '--window-size=1920x1080',
                        '--ignore-certificate-errors']

    '''
    Have to setup selenium in order to test with it.
    '''
    def setup_selenium(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            for option in self.options:
                chrome_options.add_argument(option)
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(60)
            self.driver.get(self.data.endpoint)
            time.sleep(60)
            print('Selenium setup complete.')
        except ErrorInResponseException:
            self.data.log_result(
                name='Selenium {}'.format(self.data.docker_tag),
                value='FAIL SERVER ERROR')
        except TimeoutException:
            self.data.log_result(
                name='Selenium {}'.format(self.data.docker_tag),
                value='FAIL CONNECTION TIMEOUT ERROR')
        except WebDriverException:
            self.data.log_result(
                name='Selenium {}'.format(self.data.docker_tag),
                value='FAIL DRIVER ERROR')

    '''
    Screenshot is the main test of selenium
    '''
    def take_screenshot(self):
        try:
            self.driver.get_screenshot_as_file(self.data.screenshot_name)
            self.data.log_result(
                name='Screenshot {}'.format(self.data.docker_tag),
                value='PASSED')
            print('Screenshot of {} captured at {}.'.format(self.data.image,self.data.screenshot_name))
        except IOError:
            self.data.log_result(
                name='Screenshot {}'.format(self.data.docker_tag),
                value='FAIL IOERROR')

    '''
    Tear down the testbed neatly
    '''
    def teardown_selenium(self):
        self.driver.quit()
        print('Selenium teardown complete.')
