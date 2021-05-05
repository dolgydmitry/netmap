# -*- coding: utf-8 -*-
# Crate connect to arango db an collection

from arango import ArangoClient
import json

FILE_PATH_PARAMETRS = '/home/dvdolgy/netmap/db_param.json'

class ConnectorDb:
    def __init__(self, file_path_parametrs=None):
        self.file_path_parametrs = file_path_parametrs
        self.db_param = None
        self.db = None
        self.collection = None
        self.collection_name = None
        self.aql_query = None
        self.file_json_array = None

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

    def connect_to_coll(self):
        if self.db.has_collection(self.collection_name):
            self.collection = self.db.collection(self.collection_name)
        else:
            self.collection = self.db.create_collection(self.collection_name)

    def load_doc_to_collection(self):
        for item in self.file_json_array:
            metadata = self.collection.insert(item)

    def query_return_doc(self, ns0_module_name):
        aql_query = 'FOR doc IN ' + '`' + self.collection_name + '`' + '\n' + 'FILTER doc.`ns0:module`.`@name` == ' + '"' + ns0_module_name + '"' + '\n' \
            + 'RETURN doc'
        cursor = self.db.aql.execute(aql_query)
        for document in cursor:
            result= document
        return document
      

    def start_connect_db(self):
        self.db_param = self.load_db_param()
        self.db = self.connect_to_db_v2('db')
        self.connect_to_coll()

    
#
#
#
#==============================================================
#
#
if __name__ == "__main__":
    test = ConnectorDb(file_path_parametrs=FILE_PATH_PARAMETRS)
    test.collection_name = 'optical-transport'
    test.start_connect_db()
    test.connect_to_coll()
    print(test.collection)
    doc = test.query_return_doc('openconfig-optical-amplifier')
    for x in doc['ns0:module']['ns0:identity']:
        print(x)
   
    