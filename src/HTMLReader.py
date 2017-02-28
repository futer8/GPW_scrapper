from bs4 import BeautifulSoup as bs
from contextlib import closing
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import datetime

class HTMLReader:

    def __init__(self, config_path):
        self._config = {'Search keyword': None, 'Date separator': None, 'Table headers': None}
        self._html = bs('', 'html.parser')
        self._html_text = ''
        self._data = []
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
                if len(split_line) == 2:
                    if split_line[0] in self._config:
                        key = split_line[0]
                        value = split_line[1]
                        if key == 'Table headers': value = [val.strip() for val in value.split(',')]
                        if self._config[key] == None:
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
            html_date = re.search(pattern, self._html_text)
            html_date = html_date.group()
            html_date = html_date.split(self._config['Date separator'])
            html_date = datetime.date(int(html_date[2]), int(html_date[1]), int(html_date[0]))
        except AttributeError:
            raise AttributeError('Date pattern not found in the text!')

        if html_date.year >= 2017: # This program has been written in 2017. (Semi) live feeds should be from at least 2017.
            return html_date
        else:
            raise ValueError('Problem with date - year should be at least 2017!')

    def IsLayoutOK(self, html_pattern_file):
        try:
            fh = open(html_pattern_file, 'r')
            pattern = fh.read().strip()
            fh.close()
        except FileNotFoundError:
            raise FileNotFoundError('HTML pattern file ' + html_pattern_file + ' not found!')
        return pattern in self._html_text

    def ReadData(self, regex_date_pattern_file = None, html_pattern_file = None):
        if html_pattern_file:
            if not self.IsLayoutOK(html_pattern_file):
                raise RuntimeError('HTML pattern check failed')
        
        additional_columns = 1
        html_date = None
        if regex_date_pattern_file:
            html_date = self.GetDate(regex_date_pattern_file).__str__()
            additional_columns += 1

        timestamp = datetime.datetime.now().__str__()

        tr = self._html.table.find('tr')
        max_field_cnt = len(self._config['Table headers']) - additional_columns
        while tr:
            field_cnt = 0
            td = tr.find('td')
            if td:
                a = td.find('a')
                if a:
                    field_cnt = 2
                    self._data.append([timestamp])
                    if html_date:
                        self._data[len(self._data) - 1].append(html_date)
                        field_cnt = 3
                    href = list(filter(None, a['href'].split('/')))[-1]
                    self._data[len(self._data) - 1].append(href)
                    field_cnt = 1
                    td = td.find_next_sibling('td')
                else:
                    break
            while td:
                item = td.text
                item = item.replace('\xa0', '').replace(',', '.')
                self._data[len(self._data) - 1].append(item)
                field_cnt += 1
 
                if field_cnt == max_field_cnt:
                    break
           
                td = td.find_next_sibling('td')
                if not td and field_cnt != max_field_cnt :
                    raise ValueError('Problem with the table layout: number of columns does not match the expected value!')
                   
            tr = tr.find_next_sibling('tr')
        print (self._data[0])
        print (self._data[len(self._data) - 1])
