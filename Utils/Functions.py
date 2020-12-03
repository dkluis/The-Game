import os
import time
import ast
from timeit import default_timer as timer


def get_next_id(entity):
    # ToDo create an entity id generator
    if entity == 'player':
        return 1
    elif entity == 'race':
        return 10000


"""
    Logging Class
"""


class logging:
    def __init__(self, caller='Unknown', filename='Unknown'):
        """
        :param env      Anything but 'Prod' (is default) will put the log file in the test environment mode
                          All paths come from the key_values in the DB
        :param caller   The program opening the log file
        :param filename The filename to use

        :function open
        """
        self.log_path = ""
        self.logfile = 'NotSet'
        if len(caller) < 15:
            spaces = '               '
            needed = 15 - len(caller)
            caller = caller + spaces[:needed]
        self.caller = caller
        self.filename = filename
        self.file_status = False
        self.content = []
        self.started = 0
        self.ended = 0
        self.elapsed = 0
    
    def open(self, mode='a+', read=False):
        """
                    Open the log file
        :param mode:    The open mode for the file, default = a+
        :param read:    Also put contents into: log file .content
        """
        try:
            self.logfile = open(f'{self.log_path}{self.filename}.log', mode)
        except IOError as error:
            self.logfile = open(f'{self.log_path}{self.filename}.log', 'w+')
            self.write(f'Created the log file {self.filename} due to open error: {error}', 0)
            self.logfile.close()
            self.logfile = open(f'{self.log_path}{self.filename}.log', mode)
        self.file_status = True
        if read:
            self.read()
    
    def close(self):
        """
                    Close the file
        """
        if self.file_status:
            self.logfile.close()
            self.file_status = False
    
    def write(self, message='', level=1, read=False):
        """
                    Write the message to the log file
        :param message:     Text to be written
        :param level:       Information Level Indicator
        :param read:        Also read file into log file .content
        """
        message = f"{self.caller} > Level {level} > {time.strftime('%D %T')} > {message}\n"
        if not self.file_status:
            self.open(mode='a+')
            self.logfile.write(message)
            self.close()
        else:
            self.logfile.write(message)
        if read:
            self.read()
    
    def empty(self):
        """
                    Empty the log file
        :return:
        """
        if self.file_status:
            self.close()
        self.logfile = open(f'{self.log_path}{self.filename}.log', 'w+')
        self.close()
        self.file_status = False
    
    def read(self):
        """
                    Read the whole log file
                    Info is in the .content list
        return:     Log File content
        """
        self.close()
        self.open(mode='r+')
        self.content = self.logfile.readlines()
        self.close()
        return self.content
    
    def start(self):
        """
            Record Start time
        """
        self.started = timer()
        self.write('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    
    def end(self):
        """
            Record End time
        """
        self.ended = timer()
        self.elapsed = self.ended - self.started
        self.write(f'{self.caller} Elapsed Time is:s {round(self.elapsed, 3)} seconds')
        self.write('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
