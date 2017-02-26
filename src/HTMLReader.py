from bs4 import BeautifulSoup as bs
from contextlib import closing
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import datetime

class HTMLReader:

    def __init__(self, config_path):
        self._config = {'Search keyword': '', 'Date separator': ''}
        self._html = bs('', 'html.parser')
        self._html_text = ''
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
            WebDriverWait(driver, timeout = timeout).until(lambda x: x.find_element_by_tag_name(self._config['Search keyword']))
            page_source = driver.page_source
            driver.quit()
            self._html = bs(page_source, 'html.parser')
            self._html_text = page_source
        except:
            raise RuntimeError('Error reading the supplied URL ' + url)

    def GetDate(self, regex_pattern_file):
        try:
            fh = open(regex_pattern_file, 'r')
            pattern = fh.read().strip()
            fh.close()
        except FileNotFoundError:
            raise FileNotFoundError('Date stamp regex pattern file ' + regex_pattern_file + ' not found!')
        try:
            data_date = re.search(pattern, self._html_text)
            data_date = data_date.group()
            data_date = data_date.split(self._config['Date separator'])
            data_date = datetime.date(int(data_date[2]), int(data_date[1]), int(data_date[0]))
        except AttributeError:
            raise AttributeError('Date pattern not found in the text!')

        if data_date.year >= 2017: # This program has been written in 2017. (Semi) live feeds should be from at least 2017.
            return data_date
        else:
            raise ValueError('Problem with date - year should be at least 2017!')
