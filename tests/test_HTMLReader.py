import unittest
from src.HTMLReader import HTMLReader

from bs4 import BeautifulSoup as bs
import os
import pathlib
import datetime

RES_PATH = 'tests/res/'

class Test(unittest.TestCase):

    def setUp(self):
        self.instance = HTMLReader(RES_PATH + 'HTMLReader.conf')

    def test_HTMLReader_construtor_failure(self):
        incorrect_file_name = 'non-existent HTMLReader config file'
        with self.assertRaises(FileNotFoundError) as context:
            instance = HTMLReader(incorrect_file_name)
        self.assertTrue('Error: HTMLReader config file ' + incorrect_file_name + ' not found!' == str(context.exception))

    def test_HTMLReader_constsructor_incorrect(self):
        file_name = 'HTMLReader_incorrect.conf'
        with self.assertRaises(RuntimeError) as context:
            instance = HTMLReader(RES_PATH + file_name)
        error_msg = 'Incorrect HTMLReader config file ' + RES_PATH + file_name + '! It should be (without <>):'
        self.assertTrue(error_msg in str(context.exception))
        self.assertTrue('Search keyword: <value>' in str(context.exception))
        self.assertTrue('Date separator: <value>' in str(context.exception))

    def test_GetHTML_success(self):
        absolute_path = os.path.abspath(RES_PATH + 'GPW.html')
        uri = pathlib.Path(absolute_path).as_uri()
        self.instance.GetHTML(uri, 0)
        self.assertEqual(type(self.instance._html), type(bs('','html.parser')))
        self.assertEqual(self.instance._html, bs(self.instance._html_text, 'html.parser'))
        
    def test_GetHTML_failure(self):
        incorrect_url = 'non-existent URL'
        with self.assertRaises(RuntimeError) as context:
            self.instance.GetHTML(incorrect_url, 0)
        self.assertTrue('Error reading the supplied URL ' + incorrect_url == str(context.exception))

    def test_GetDate_success(self):
        absolute_path = os.path.abspath(RES_PATH + 'GPW.html')
        uri = pathlib.Path(absolute_path).as_uri()
        self.instance.GetHTML(uri, 0)

        result = self.instance.GetDate(RES_PATH + 'Date_stamp_regex_pattern.txt')
        self.assertEqual(type(datetime.date.today()), type(result))
        self.assertGreaterEqual(result.year, 2017)

    def test_GetDate_failure_reading(self):
        incorrect_file_name = 'non-existent path'
        with self.assertRaises(FileNotFoundError) as context:
            result = self.instance.GetDate(incorrect_file_name)
        self.assertTrue('Date stamp regex pattern file ' + incorrect_file_name + ' not found!' == str(context.exception))

    def test_GetDate_failure_incorrect_date(self):
        absolute_path = os.path.abspath(RES_PATH + 'GPW_incorrect_date.html')
        uri = pathlib.Path(absolute_path).as_uri()
        self.instance.GetHTML(uri, 0)

        with self.assertRaises(ValueError) as context:
            result = self.instance.GetDate(RES_PATH + 'Date_stamp_regex_pattern.txt')
        self.assertTrue('Problem with date - year should be at least 2017!' == str(context.exception))

    def test_GetDate_failure_pattern_not_found(self):
        with self.assertRaises(AttributeError) as context:
            result = self.instance.GetDate(RES_PATH + 'Date_stamp_regex_pattern.txt')
        self.assertTrue('Date pattern not found in the text!' == str(context.exception))



        
if __name__ == '__main__':
    unittest.main()
