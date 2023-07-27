#%%
import pyodbc
import numpy as np
import pandas as pd
import warnings
import logging

class DB:
    def __init__(self, database, driver, server, username, password):
        self.database = database
        self.driver = driver
        self.server = server
        self.username = username
        self.password = password

    #ログイン
    def login(self):
        warnings.simplefilter('ignore')
        self.login_sentence = 'DRIVER={'+self.driver+'};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password+';'
        try:
            self.cnxn = pyodbc.connect(self.login_sentence)
            self.cursor = self.cnxn.cursor()
        except:
            logging.exception('SQLサーバーへのログインに失敗しました')
    
    #UPDATE文作成
    def update_SQL_sentence(self, table, columns, keys):
        update = 'UPDATE [dbo].['+table+'] SET ['+columns[0]+']=?'
        if len(columns) != 1:
            for column in columns[1:]:
                update = update+', ['+column+']=?'
        update = update+' WHERE ['+keys[0]+']=?'
        if len(keys) != 1:
            for key in keys[1:]:
                update = update+' AND ['+key+']=?'
        return update
    
    #汎用INSERT処理
    def insert_SQL(self, df, columns, table, keys, updateoption='Yes'):
        err = 0
        insert = self.insert_SQL_sentence(table, columns)
        update = self.update_SQL_sentence(table, columns, keys)
        df = df.replace({np.nan: None})
        for _, row in df.iterrows():
            key = row[keys]
            try:
                #CSVのデータをSQLに挿入
                self.cursor.execute(insert, *row)
            except:
                if updateoption=='Yes':
                    try:
                        self.cursor.execute(update, *row, *key)
                    except:
                        logging.exception('SQLテーブルへのインポートに失敗しました')
                        err += 1
                        break
                else:
                    logging.exception('SQLテーブルへのインポートに失敗しました')
                    err += 1
                    break
        if err == 0:
            self.cnxn.commit()
        return err

    #SQLテーブル読み込み
    def read_SQL(self, table):
        try:
            #データの読み込み
            df_SQL = pd.read_sql('SELECT * FROM [dbo].['+table+'];', self.cnxn)
        except:
            logging.exception('所定のSQLテーブルがありません')
        return df_SQL

    #SQLテーブルカラム取得
    def read_SQL_columns(self, table):
        try:
            #データの読み込み
            df_SQL = pd.read_sql('SELECT TOP 0 * FROM [dbo].['+table+'];', self.cnxn)
        except:
            logging.exception('所定のSQLテーブルがありません')
        return df_SQL.columns

    def logout(self):
        self.cnxn.commit()
        self.cursor.close()
