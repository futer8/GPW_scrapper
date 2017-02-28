import unittest
from src.HTMLReader import HTMLReader

from bs4 import BeautifulSoup as bs
import os
import pathlib
import datetime

RES_PATH = 'tests/res/'

class TestCase1(unittest.TestCase):

    def setUp(self):
        self.instance = HTMLReader(RES_PATH + 'HTMLReader.conf')
        self.instance2 = HTMLReader(RES_PATH + 'HTMLReader.conf')
        absolute_path = os.path.abspath(RES_PATH + 'GPW.html')
        uri = pathlib.Path(absolute_path).as_uri()
        self.instance2.GetHTML(uri, 0)

    def test_HTMLReader_construtor_failure(self):
        incorrect_file_name = 'non-existent HTMLReader config file'
        with self.assertRaises(FileNotFoundError) as context:
            instance = HTMLReader(incorrect_file_name)
        self.assertEqual('Error: HTMLReader config file ' + incorrect_file_name + ' not found!', str(context.exception))

    def test_HTMLReader_constsructor_incorrect(self):
        file_name = 'HTMLReader_incorrect.conf'
        with self.assertRaises(RuntimeError) as context:
            instance = HTMLReader(RES_PATH + file_name)
        error_msg = 'Incorrect HTMLReader config file ' + RES_PATH + file_name + '! It should be (without <>):'
        self.assertTrue(error_msg in str(context.exception))
        self.assertTrue('Search keyword: <value>' in str(context.exception))
        self.assertTrue('Date separator: <value>' in str(context.exception))
        self.assertTrue('Table headers: <value>' in str(context.exception))

    def test_GetHTML_success(self):
        self.assertEqual(type(self.instance2._html), type(bs('','html.parser')))
        self.assertEqual(self.instance2._html, bs(self.instance2._html_text, 'html.parser'))
        
    def test_GetHTML_failure(self):
        incorrect_url = 'non-existent URL'
        with self.assertRaises(RuntimeError) as context:
            self.instance.GetHTML(incorrect_url, 0)
        self.assertEqual('Error reading the supplied URL ' + incorrect_url, str(context.exception))

    def test_GetDate_success(self):
        result = self.instance2.GetDate(RES_PATH + 'Date_stamp_regex_pattern.txt')
        self.assertEqual(type(datetime.date.today()), type(result))
        self.assertGreaterEqual(result.year, 2017)

    def test_GetDate_failure_reading(self):
        incorrect_file_name = 'non-existent path'
        with self.assertRaises(FileNotFoundError) as context:
            result = self.instance.GetDate(incorrect_file_name)
        self.assertEqual('Date stamp regex pattern file ' + incorrect_file_name + ' not found!', str(context.exception))

    def test_GetDate_failure_incorrect_date(self):
        absolute_path = os.path.abspath(RES_PATH + 'GPW_incorrect_date.html')
        uri = pathlib.Path(absolute_path).as_uri()
        self.instance.GetHTML(uri, 0)

        with self.assertRaises(ValueError) as context:
            result = self.instance.GetDate(RES_PATH + 'Date_stamp_regex_pattern.txt')
        self.assertEqual('Problem with date - year should be at least 2017!', str(context.exception))

    def test_GetDate_failure_pattern_not_found(self):
        with self.assertRaises(AttributeError) as context:
            result = self.instance.GetDate(RES_PATH + 'Date_stamp_regex_pattern.txt')
        self.assertEqual('Date pattern not found in the text!', str(context.exception))

    def test_IsLayoutOK_success(self):
        result = self.instance2.IsLayoutOK(RES_PATH + 'Table_header_stamp.txt')
        self.assertEqual(result, True)

    def test_IsLayoutOK_failure(self):
        result = self.instance2.IsLayoutOK(RES_PATH + 'Table_header_stamp_unavailable.txt')
        self.assertEqual(result, False)

    def test_IsLayoutOK_failure_reading(self):
        incorrect_file_name = 'non-existent path'
        with self.assertRaises(FileNotFoundError) as context:
            result = self.instance.IsLayoutOK(incorrect_file_name)
        self.assertEqual('HTML pattern file ' + incorrect_file_name + ' not found!', str(context.exception))
       
    def test_ReadData_success(self):
        self.instance2.ReadData(RES_PATH + 'Date_stamp_regex_pattern.txt')

    def test_ReadData_failure(self):
        with self.assertRaises(ValueError) as context:
            self.instance2.ReadData()
        self.assertEqual(str(context.exception), 'Problem with the table layout: number of columns does not match the expected value!')

    def test_ReadData_failure_html_pattern(self):
        with self.assertRaises(RuntimeError) as context:
            self.instance2.ReadData(html_pattern_file = RES_PATH + 'Table_header_stamp_unavailable.txt')
        self.assertEqual(str(context.exception), 'HTML pattern check failed')

if __name__ == '__main__':
    unittest.main()
