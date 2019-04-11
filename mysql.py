#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"Mysql操作类"

import pymysql


class Mysql(object):
    def __init__(self, config):
        if isinstance(config, dict):
            try:
                self.__address = config['address']
                self.__port = config['port']
                self.__username = config['username']
                self.__password = config['password']
                self.__database = config['database_name']
                self.connect()
            except KeyError as e:
                print("Config Error.")
                print("Check the \"config.py\".")

    def __del__(self):
        self.close()

    def connect(self):
        '''建立Mysql连接'''
        self.__db = pymysql.connect(host=self.__address, port=self.__port, user=self.__username,
                                    passwd=self.__password, db=self.__database, charset='utf8')

    def close(self):
        '''关闭mysql连接'''
        self.ping()
        self.__db.close()

    def insert(self, sql):
        '''插入一条记录'''
        self.ping()
        cursor = self.__db.cursor()
        try:
            cursor.execute(sql)
            self.__db.commit()
        except:
            self.__db.rollback()
            return False
        finally:
            cursor.close()
            return True

    def query(self, sql):
        '''查询一条记录'''
        self.ping()
        cursor = self.__db.cursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchone()
            cursor.close()
            return data
        except:
            print("Query Error.")

    def queryall(self, sql):
        '''查询全部记录'''
        self.ping()
        cursor = self.__db.cursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.close()
            return data
        except:
            print("Query Error.")

    def ping(self):
        '''Mysql断开重连'''
        try:
            self.__db.ping()
        except:
            self.connect()
