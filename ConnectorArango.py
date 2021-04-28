# -*- coding: utf-8 -*-
# Connect to DB 
import json
from pyArango.connection import *
from pyArango.document import *
from pyArango.database import *
from pyArango.collection import *

FILE_PATH_PARAMETRS = '/home/dvdolgy/netmap/db_param.json'


class ConnectorDb:
    def __init__(self, file_path_parametrs=None):
        self.file_path_parametrs = file_path_parametrs
        self.db_param = None
        self.conn = None
        self.db = None


    def load_db_param(self):
        with open(self.file_path_parametrs, 'r') as fp:
             data = json.load(fp)
        return data

    def connect_to_db(self, db_hostname):
        conn = Connection(
            arangoURL=self.db_param[db_hostname]['url'],
            username=self.db_param[db_hostname]['username'],
            password=self.db_param[db_hostname]['password']
        )
        db = conn[self.db_param[db_hostname]['name']]
        return db

    def launcher(self):
        self.db_param = self.load_db_param()
        self.db = self.connect_to_db('db')


class DbIntArango(ConnectorDb):
    def __init__(self, file_path_parametrs=None, db_name=None, file_path_document=None, query_arango=None):
        super().__init__(file_path_parametrs=file_path_parametrs)
        self.file_path_document = file_path_document
        self.query_arango = query_arango
        self.db_name = db_name
        self.collection_name = None

    # def connect_to_db(self):
        # db = Database(self.conn, self.db_name)
        # return db

    # def create_collection(self):
    #     db = self.connect_to_db()
    #     db.createCollection(self.collection_name)
        
    def launcher(self):
        super().launcher()


if __name__ == "__main__":
    # test = ConnectorDb(FILE_PATH_PARAMETRS)
    # test.launcher()

    test = DbIntArango(FILE_PATH_PARAMETRS, db_name='otn-test')
    test.launcher()
    print(test.db)
    # test.collection_name = 'optical-transport'
    # test.create_collection()
