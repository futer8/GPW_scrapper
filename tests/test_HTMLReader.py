import unittest
from src.HTMLReader import *

from bs4 import BeautifulSoup as bs
import os
import pathlib

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
        error_msg += ' \n Search keyword: <value>'
        self.assertTrue(error_msg == str(context.exception))

    def test_GetHTML_success(self):
        absolute_path = os.path.abspath(RES_PATH + 'GPW.html')
        uri = pathlib.Path(absolute_path).as_uri()
        self.instance.GetHTML(uri, 0)
        self.assertEqual(type(self.instance.html), type(bs('','html.parser')))
        
    def test_GetHTML_failure(self):
        incorrect_url = 'non-existent URL'
        with self.assertRaises(RuntimeError) as context:
            self.instance.GetHTML(incorrect_url, 0)
        self.assertTrue('Error reading the supplied URL ' + incorrect_url == str(context.exception))

#    def test_CheckTimeStamp(self):
#        result = self.instance.CheckTimeStamp('

if __name__ == '__main__':
    unittest.main()
