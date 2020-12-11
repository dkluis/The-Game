import sqlite3
import os
import ast

from Utils import logging


class config:
    def __init__(self):
        """
            Config is the routine to read 'secrets' from the configuration file so that they are never visible
            or hard-coded in the source files
        """
        self.__log = logging(caller='Lib config', filename='TheGame')
        secret = ''
        try:
            secret = open('/Volumes/HD-Data-CA-Server/Development/PycharmProjects/The Game/.thegame/config', 'r')
        except IOError as err:
            self.__log.write(f'The Game config is not found at .thegame/config with error {err}')
            quit()
        secrets = ast.literal_eval(secret.read())
        if not secrets:
            self.__log.write(f'No config info found')
            quit()
        self.host_network = secrets['host_network']
        self.host_local = secrets['host_local']
        self.db_admin = secrets['db_admin']
        self.db_password = secrets['db_password']
        self.db_prod = secrets['db_prod']
        self.db_test = secrets['db_test']
        self.user_admin = secrets['user_admin']
        self.user_password = secrets['user_password']
        self.host = ''
        self.check_host()
        self.db = ''
        self.check_db()
        secret.close()
    
    def check_host(self):
        """
            Set the db host to Network access or localhost access
        """
        check = os.getcwd()
        if 'SharedFolders' in check:
            self.host = self.host_network
        else:
            self.host = self.host_local
    
    def check_db(self):
        """
            Set the DB to Production or Test
        """
        check = os.getcwd()
        if 'Pycharm' in check:
            self.db = self.db_test
        else:
            self.db = self.db_prod
    
    
class sqliteDB:
    def __init__(self, batch=False):
        """
            sqliteDB handles the DB activities for a sqlite3 Database

        :param batch:   Default False, which mean a commit after all executes of sql which normally require a commit
                        True, mean that commits are postpone until a commit is manually called or when the DB is closed
        """
        self.batch = batch
        self.__log = logging(caller='sqliteDB', filename='TheGame')
        self.__active = False
        self.__fields = []

        self.__db_loc = os.getcwd() + '/Data/TheGame.db'
        self.__connection = sqlite3.connect(self.__db_loc)
        self.__cursor = self.__connection.cursor()
        self.__log.write(f'sqliteDB: Initialized the DB {self.__db_loc}')
        
    def open(self):
        """
            Opens a Connection and Cursor
            
        :return: None
        """
        if not self.__active:
            self.__connection = sqlite3.connect(self.__db_loc)
            self.__cursor = self.__connection.cursor()
            self.__active = True
            self.__log.write(f'sqliteDB: Opened the DB connection')
        else:
            self.__log.write(f'sqliteDB: Tried to open a DB connection while already open')
    
    def close(self):
        """
            Closes the connection 
        
        :return: None
        """
        if self.__active:
            if self.batch:
                self.commit()
            self.__connection.close()
            self.__active = False
            self.__log.write(f'sqliteDB: Closed the DB connection')
        else:
            self.__log.write(f'sqliteDB: Tried to close the DB connection while already closed')
    
    def commit(self):
        """
            Commits outstanding transactions
            
        :return: None
        """
        if self.__active:
            self.__connection.commit()
            self.__log.write(f'Committed outstanding transactions')
        else:
            self.__log.write(f'Commit requested but no DB connection is active')
        return
    
    def rollback(self):
        """
            Rolls back outstanding transactions
            
        :return: 
        """
        if self.__active:
            self.__log.write(f'Rollback outstanding transactions')
            self.__connection.rollback()
        else:
            self.__log.write(f'Rollback requested but no DB connection is active')
            
    def execute_sql(self, sql='', sql_type='Fetch', data_dict=False, row_id=False, field_list=[]):
        """
                Execute SQL
                
        :param sql:         The SQL to execute
        :param sql_type:    Default if 'Fetch' other option is 'Commit'
        :param data_dict:   Default False, True create a dictionary out of the result of a fetch
        :param field_list:  The list of fields to be returned in the dict.  
                            Is optional since the lib will try to figure out the
                                field array itself but for joins and select * (for now) 
                                you need the list to be passed in.
        :param row_id        Default False, True adds and id number for every row of data returned in the data_dict
        :return:            True, False or the result or data_dict set from a fetch
        """
        if not self.__active:
            self.open()
        if sql_type == 'Commit':
            try:
                self.__cursor.execute(sql)
                if not self.batch:
                    self.__connection.commit()
            except sqlite3.Error as er:
                self.__log.write(f'Execute SQL (Commit) Database Error: {self.__db_loc}, {er}, {sql}', 0)
                self.__log.write('----------------------------------------------------------------------')
                return False, er
            return True
        elif sql_type == "Fetch":
            try:
                self.__cursor.execute(sql)
                result = self.__cursor.fetchall()
            except sqlite3.Error as er:
                self.__log.write(f'Execute SQL (Fetch) Database Error: {self.__db_loc}, {er}, {sql}', 0)
                self.__log.write(f'----------------------------------------------------------------------')
                return False, er
            self.__log.write(f'sqliteDB: SQL execution of {sql_type}: {sql} with {len(result)} records returned')
            if data_dict and len(result) > 0:
                if field_list:
                    self.__fields = field_list
                else:
                    self.__extract_fields(sql)
                self.__log.write(f'Transforming the result into a dictionary result length: {len(result)}')
                self.__data_as_dict(result, row_id)
                return self.data_dict
            else:
                return result
        else:
            return False, 'Not implemented yet'
    
    def __extract_fields(self, sql):
        """
            Extract the fields from the sql
            Note: Current does not support the select * option
            
        :param sql:     The sql
        :return:        List of Fields (also self.fields)
        """
        sr = sql.lower().replace('select ', '').replace("`", "")
        sp = sr.lower().split(' from')[0]
        # st = ''
        if sp == '*':
            '''
            sf = sql.lower().split('from ')
            if len(sf) == 2:
                st = str(sf[1]).lower()
            fields_sql = f"SHOW COLUMNS FROM {st}"
            self.__cursor.execute(fields_sql)
            columns = self.__cursor.fetchall()
            self.fields = []
            for column in columns:
                self.fields.append(column[0])
            return self.fields
            '''
            return []
        else:
            fields = sp.split(", ")
            for field in fields:
                self.__fields.append(field)
            return self.__fields
    
    def __data_as_dict(self, result, idx_id=False):
        """
            Returns the data as a dictionary (with or without and index in front of every row
            
        :param  result:     The Data to be processed
        :param  idx_id:     Default False, otherwise it adds and numbered ID to the dict
        :return:
        """
        if len(self.__fields) != len(result[0]):
            self.__log.write(f'The length {len(self.__fields)} of the data array does not match '
                             f'the length {len(result)} of the field array', 0)
            self.data_dict = []
            return
        response = ''
        id_idx = 1
        for rec in result:
            if idx_id:
                row = "{" + f'''"id": "{id_idx}", '''
                id_idx += 1
            else:
                row = "{"
            f_idx = 0
            for field in self.__fields:
                row += f'''"{field}": "{str(rec[f_idx]).replace('"', '~~')}", '''
                f_idx += 1
            response = response + row[:-2] + "},"
        response = "[" + response[:-1] + "]"
        self.data_dict = ast.literal_eval(response)
