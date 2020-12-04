import mariadb
import sys
import os
import ast

from Utils import logging


class config:
    def __init__(self):
        """
            Config is the routine to read 'secrets' from the configuration file so that they are never visible
            or hard-coded in the source files
        """
        self.__log = logging(caller='Lib config', filename='The Game')
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


class mariaDB:
    def __init__(self, h='', d='', batch=False):
        """
            mariaDB handles the DB activities for the mariadb DB of TVM-Management

        :param h:       manually assign a host
        :param d:       manually assign Production or Testing DB
        :param batch:   Default False, which mean a commit after all executes of sql with require a commit
                        True, mean that commits are postpone until a commit is trigger or when the DB is closed
        """
        self.__log = logging(caller='Lib mariaDB', filename='The Game')
        conf = config()
        if h != '':
            self.__host = h
        else:
            self.__host = conf.host
        self.__user = conf.db_admin
        self.__password = conf.db_password
        self.__user_admin = conf.user_admin
        self.__user_password = conf.user_password
        if d != '':
            self.__db = d
        else:
            self.__db = conf.db
        self.__batch = batch
        
        self.__connection = ''
        self.__cursor = ''
        self.__active = False
        self.open()
        
        self.fields = []
        self.data_dict = []
    
    def open(self):
        if self.__active:
            return
        try:
            self.__connection = mariadb.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__db)
        except mariadb.Error as err:
            if err:
                self.__log.write(f"Connect {self.__db}: Error connecting to MariaDB Platform: {err}", 0)
                self.__log.write('--------------------------------------------------------------------------')
                sys.exit(1)
        self.__cursor = self.__connection.cursor()
        self.__active = True
    
    def close(self):
        if self.__active:
            if self.__batch:
                self.commit()
            self.__connection.close()
            self.__active = False
    
    def commit(self):
        """
            Execute a commit for outstanding transactions
        """
        if self.__active:
            self.__connection.commit()
    
    def execute_sql(self, sql='', sqltype='Fetch', data_dict=False, dd_id=False, field_list=[]):
        """
                Execute SQL
        :param sql:         The SQL to execute
        :param sqltype:     Default if 'Fetch' other option is 'Commit'
        :param data_dict:   Default False, True create a dictionary out of the result of a fetch
        :param field_list:  The list of fields to be returned in the dict.  The lib will try to figure out the
                                field array itself but for joins you need the list to be passed in.
        :param dd_id        Default False, True adds and id number for every row of data returned in the data_dict
        :return:            True, False or the result or data_dict set from a fetch
        """
        if not self.__active:
            self.open()
        if sqltype == 'Commit':
            try:
                self.__cursor.execute(sql)
                if not self.__batch:
                    self.__connection.commit()
            except mariadb.Error as er:
                self.__log.write(f'Execute SQL (Commit) Database Error: {self.db}, {er}, {sql}', 0)
                self.__log.write('----------------------------------------------------------------------')
                return False, er
            return True
        elif sqltype == "Fetch":
            try:
                self.__cursor.execute(sql)
                result = self.__cursor.fetchall()
            except mariadb.Error as er:
                self.__log.write(f'Execute SQL (Fetch) Database Error: {self.db}, {er}, {sql}', 0)
                self.__log.write(f'----------------------------------------------------------------------')
                return False, er
            if data_dict and len(result) > 0:
                if field_list:
                    self.fields = field_list
                else:
                    self.__extract_fields(sql)
                self.__data_as_dict(result, dd_id)
                return self.data_dict
            else:
                return result
        else:
            return False, 'Not implemented yet'
    
    def __extract_fields(self, sql):
        """
            Extract the fields from the sql
        :param sql:     The sql
        :return:        List of Fields (also self.fields)
        """
        sr = sql.lower().replace('select ', '').replace("`", "")
        sp = sr.lower().split(' from')[0]
        if sp == '*':
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
        else:
            fields = sp.split(", ")
            for field in fields:
                self.fields.append(field)
            return self.fields
    
    def __data_as_dict(self, result, idx_id=False):
        """
            Returns the data as a dictionary (with or without and index in front of every row
        :param  result:     The Data to be processed
        :param  idx_id:     Default False, otherwise it adds and numbered ID to the dict
        :return:
        """
        if len(self.fields) != len(result[0]):
            self.__log.write(f'The length {len(self.fields)} of the data array does not match '
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
            for field in self.fields:
                row += f'''"{field}": "{str(rec[f_idx]).replace('"', '~~')}", '''
                f_idx += 1
            response = response + row[:-2] + "},"
        response = "[" + response[:-1] + "]"
        self.data_dict = ast.literal_eval(response)
        return


class tables:
    def __init__(self):
        self.create_players = "CREATE TABLE Players " \
                              "(nick_name varchar(30) NOT NULL, " \
                              "password varchar(30) NOT NULL, " \
                              "CONSTRAINT Players_UN UNIQUE KEY (nick_name), " \
                              "CONSTRAINT Players_PK PRIMARY KEY (nick_name)) " \
                              "ENGINE=InnoDB " \
                              "DEFAULT CHARSET=utf16 COLLATE=utf16_general_ci;"
        self.drop_players = "DROP TABLE Players;"
        self.init_players = "INSERT INTO TheGameDB.Players (nick_name,password) " \
                            "VALUES " \
                            "('Admin','admin'), " \
                            "('Dick','admin');"
