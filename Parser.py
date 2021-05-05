# -*- coding: utf-8 -*-
# Convert xml to json format and load to db
from pyang import plugin
from pyangbind import *
import xml.etree.ElementTree
import xmltodict
import json
import xmljson
import os
import re
from arango import ArangoClient
from multiprocessing import Process, Queue
from queue import Empty

FILE_PATH_PARAMETRS = '/home/dvdolgy/netmap/db_param.json'


FILE_PATH_IN = '/home/dvdolgy/netmap/xml_file'
FILE_PATH_OUT = '/home/dvdolgy/netmap/json_file/collection'


class ConnectorDb:
    def __init__(self, file_path_parametrs=None):
        self.file_path_parametrs = file_path_parametrs
        self.db_param = None
        self.db = None
        self.db_name = None
        self.collection = None
        self.collection_name = None

    def load_db_param(self):
        with open(self.file_path_parametrs, 'r') as fp:
             data = json.load(fp)
        return data

    def connect_to_db_v2(self, db_hostname):
        conn = ArangoClient(hosts=self.db_param[db_hostname]['url'])
        db = conn.db(
            name=self.db_param[db_hostname]['name'],
            username=self.db_param[db_hostname]['username'], 
            password=self.db_param[db_hostname]['password']
            )
        return db

    def start_connect_db(self):
        self.db_param = self.load_db_param()
        #self.db = self.connect_to_db('db')
        self.db = self.connect_to_db_v2('db')


class Parser(ConnectorDb):
    def __init__(
        self, 
        file_path_in=None, 
        file_path_out=None, 
        file_path_parametrs=None, 
        db_name=None, 
        file_path_document=None, 
        query_arango=None
        ):
        super().__init__(file_path_parametrs=file_path_parametrs)
        self.file_path_in = file_path_in
        self.file_path_out = file_path_out
        self.query_arango = query_arango
        self.db_name = db_name
        self.collection = None
        self.collection_name = None
        self.json_reciver = Queue(maxsize=4)
        self.json_array = []

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

    def writer_file_array(self, data, file_out):
         with open(file_out, 'w') as fp:
            fp.write('[' + '\n')
            for item in data:
                fp.write(item)
            fp.write('\n' + ']')
      
    def handler_files(self, files_array):
        for file_path in files_array:
            file_out = self.file_path_out + '/' + re.sub(r'xml', 'json', file_path[1])
            sands = xml.etree.ElementTree.parse(file_path[0])
            gold_json = self.translater_file_to_json(sands)
            gold_dict = self.translater_file_to_dict(sands)
            self.json_array.append(gold_dict)

    def handler_files_multiproc(self, files_array):
        p_array = []
        for file_path in files_array:
            p = Process(target=self.translater_file_to_dict_proc, args=(file_path,))
            p.start()
            p_array.append(p)

        #Queu handler    
        #--------------------------------------------------------------------------------
        while True:
            try:
                # get up in the queue
                gold = self.json_reciver.get(timeout=1)
                # put gold in resulting array
                self.json_array.append(gold)
            # if queue empty we will check how many procces is alive
            except Empty:
                if not any(p.is_alive() for p in p_array):
                    break
        #--------------------------------------------------------------------------------
        for p in p_array:
            p.join()
   
    def translater_file_to_dict_proc(self, file_path):
        sands = xml.etree.ElementTree.parse(file_path[0])
        gold_dict = self.translater_file_to_dict(sands)
        self.json_reciver.put(gold_dict)


    def translater_file_to_json(self, sands):
        root = sands.getroot()
        sands_string = xml.etree.ElementTree.tostring(root, encoding='UTF-8', method='xml')
        sands_dict = xmltodict.parse(sands_string)
        gold = json.dumps(sands_dict, indent=4)
        return gold

    def translater_file_to_dict(self, sands):
        root = sands.getroot()
        sands_string = xml.etree.ElementTree.tostring(root, encoding='UTF-8', method='xml')
        sands_dict = xmltodict.parse(sands_string)
        return sands_dict

    def launcher_file_handler(self):
        files_array = self.directory_scout()
        #self.handler_files(files_array)
        self.handler_files_multiproc(files_array)

    def connect_to_coll(self):
        if self.db.has_collection(self.collection_name):
            self.collection = self.db.collection(self.collection_name)
        else:
            self.collection = self.db.create_collection(self.collection_name)

    def load_doc_to_collection(self):
        for item in self.json_array:
            #print(item['ns0:module']['@name'])
            print(item)
            #metadata = self.collection.insert(item)
            # p = Process(target=self.self.collection.insert, args=(item,))
            # p.start()
        # for p in p_array:
        #     p.join()
        







#
#
#
#==============================================================
#
#
if __name__ == "__main__":
    test = Parser(
        file_path_in=FILE_PATH_IN, 
        file_path_out=FILE_PATH_OUT, 
        file_path_parametrs=FILE_PATH_PARAMETRS
        )

    test.start_connect_db()
    test.launcher_file_handler()
    print(len(test.json_array))
    test.collection_name = 'optical-transport-juniper'
    #test.connect_to_coll()
    test.load_doc_to_collection()
    #print(test.collection)
 

 
    