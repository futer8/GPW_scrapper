from bs4 import BeautifulSoup as bs
from contextlib import closing
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

SEARCH_KEYWORD = 'table'

class HTMLReader:

    def __init__(self, config_path):
        self._config = {'Search keyword': ''}
        try:
            fh = open(config_path, 'r')
            lines = fh.readlines()
            fh.close()
        except FileNotFoundError:
            raise FileNotFoundError('Error: HTMLReader config file ' + config_path + ' not found!')

        error_msg = 'Incorrect HTMLReader config file ' + config_path + '! It should be (without <>):'
        for key in self._config.keys():
            error_msg += ' \n ' + key + ': <value>'

        config_update_count = 0
        try:
            for line in lines:
                split_line = [item.strip() for item in line.split(':')]
                if len(split_line) == 2 and split_line[0] in self._config:
                    key = split_line[0]
                    value = split_line[1]
                    if self._config[key] == '':
                        self._config[key] = value
                        config_update_count += 1
                    else:
                        raise RuntimeError(error_msg)
                else:
                    raise RuntimeError(error_msg)
        except:
            raise RuntimeError(error_msg)

        if config_update_count != len(self._config):
            raise RuntimeError(error_msg)

    def GetHTML(self, url, timeout = 10):
        try:
            driver = webdriver.PhantomJS()
            driver.get(url)
            WebDriverWait(driver, timeout = timeout).until(lambda x: x.find_element_by_tag_name(SEARCH_KEYWORD))
            page_source = driver.page_source
            driver.quit()
            self.html = bs(page_source, 'html.parser')
        except:
            raise RuntimeError('Error reading the supplied URL ' + url)
