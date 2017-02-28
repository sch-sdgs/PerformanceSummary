import json
import sqlite3
from enum import Enum
import os
from pybedtools import BedTool
import os
#from app import models

class Database():
    def __init__(self):
        path = os.path.dirname(os.path.dirname(__file__))
        print(path)
        #self.performance = path + '/resources/performance.db'
        self.performance = '/home/bioinfo/mparker/wc/PerformanceSummary/resources/performance.db'
        print self.performance
        self.performance_conn = sqlite3.connect(self.performance,check_same_thread=False)

    def query_db(self,c, query, args=(), one=False):
        """

        general method to do a select statement and format result into an easy to use dict

        :param c:
        :param query:
        :param args:
        :param one:
        :return: list of dicts
        """
        c.execute(query, args)
        r = [dict((c.description[i][0], value) \
                  for i, value in enumerate(row)) for row in c.fetchall()]
        return (r[0] if r else None) if one else r

    def __del__(self):
        self.performance_conn.commit()
        self.performance_conn.close()



class Users(Database):
    def query_db(self, c, query, args=(), one=False):
        return Database.query_db(self, c, query, args, one)

    def get_users(self):
        # pp = self.panelpal_conn.cursor()
        # users = self.query_db(pp,"SELECT * FROM users")
        # return users
        #print models.Users.query.all()
        pass

    def add_user(self,user, admin):
        pp = self.performance_conn.cursor()
        try:
            pp.execute("INSERT OR IGNORE INTO users(username,admin) VALUES (?,?)", (user,admin))
            self.performance_conn.commit()
            return pp.lastrowid
        except self.performance_conn.Error as e:
            self.performance_conn.rollback()
            print e.args[0]
            return -1