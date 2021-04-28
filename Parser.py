# -*- coding: utf-8 -*-
# Convert xml to json format 
from pyang import plugin
from pyangbind import *
import xml.etree.ElementTree
import xmltodict
import json
import xmljson
import os
import re


FILE_PATH_IN = '/home/dvdolgy/netmap/xml_file'
FILE_PATH_OUT = '/home/dvdolgy/netmap/json_file'


class Parser:
    def __init__(self, file_path_in=None, file_path_out=None):
        self.file_path_in = file_path_in
        self.file_path_out = file_path_out


    def directory_scout(self):
        files_array = [] 
        for filenames in os.walk(self.file_path_in):
            for filename in filenames[2]:    
                file_path = self.file_path_in + '/' + filename
                files_array.append([file_path, filename])
        return files_array

    def load_file(self):
        result = xml.etree.ElementTree.parse(self.file_path_in)
        return result

    def writer_file(self, data, file_out):
         with open(file_out, 'w') as fp:
             fp.write(data)
   
    def handler_files(self, files_array):
        for file_path in files_array:
            file_out = self.file_path_out + '/' + re.sub(r'xml', 'json', file_path[1])
            sands = xml.etree.ElementTree.parse(file_path[0])
            gold = self.translater_file(sands)
            self.writer_file(gold, file_out)

    def translater_file(self, sands):
        root = sands.getroot()
        sands_string = xml.etree.ElementTree.tostring(root, encoding='UTF-8', method='xml')
        sands_dict = xmltodict.parse(sands_string)
        gold = json.dumps(sands_dict, indent=4)
        return gold

    def launcher(self):
        file_array = self.directory_scout()
        self.handler_files(file_array)


if __name__ == "__main__":
    test = Parser(FILE_PATH_IN, FILE_PATH_OUT)
    test.launcher()
    