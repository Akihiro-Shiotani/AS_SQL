#%%
import pyodbc
import numpy as np
import pandas as pd
import warnings
import logging

#INSERT文作成
def insert_SQL_sentence(table, columns):
    column_names = '['+columns[0]+']'
    column_range = '?'
    if len(columns != 1):
        for column in columns[1:]:
            column_names = column_names + ', ['+column+']'
            column_range = column_range + ', ?'
    insert = 'INSERT INTO [dbo].['+table+']('+column_names+') VALUES ('+column_range+')'
    return insert

#DELETE文作成
def delete_SQL_sentence(table, columns):
    delete = 'DELETE FROM [dbo].['+table+'] WHERE ['+columns[0]+']=?'
    if len(columns) != 1:
        for key in columns[1:]:
            delete = delete+' AND ['+key+']=?'
    return delete

#UPDATE文作成
def update_SQL_sentence(table, columns, keys):
    update = 'UPDATE [dbo].['+table+'] SET ['+columns[0]+']=?'
    if len(columns) != 1:
        for column in columns[1:]:
            update = update+', ['+column+']=?'
    update = update+' WHERE ['+keys[0]+']=?'
    if len(keys) != 1:
        for key in keys[1:]:
            update = update+' AND ['+key+']=?'
    return update

class DB:
    def __init__(self, database, driver, server, username, password):
        warnings.simplefilter('ignore')
        login_sentence = 'DRIVER={'+driver+'};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password+';'
        try:
            self.cnxn = pyodbc.connect(login_sentence)
            self.cursor = self.cnxn.cursor()
        except:
            logging.exception('SQLサーバへのログインに失敗しました')
    
    def get_key(self, table):
        keys = pd.read_sql('EXEC sp_pkeys ['+table+']', self.cnxn)['COLUMN_NAME'].values
        return keys
    
    #汎用INSERT処理
    def insert_SQL(self, df, columns, table, updateoption='Yes'):
        insert = insert_SQL_sentence(table, columns)
        keys = self.get_key(table)
        df = df.replace({np.nan: None})
        self.err_df = pd.DataFrame([], columns=columns)
        for _, row in df.iterrows():
            try:
                #CSVのデータをSQLに挿入
                self.cursor.execute(insert, *row)
            except:
                if updateoption=='Yes':
                    try:
                        update = update_SQL_sentence(table, columns, keys)
                        key = row[keys]
                        self.cursor.execute(update, *row, *key)
                    except:
                        logging.exception('テーブルへのインポートに失敗しました')
                        self.err_df = pd.concat([self.err_df, pd.DataFrame([row])])
                else:
                    logging.exception('テーブルへのインポートに失敗しました')
                    self.err_df = pd.concat([self.err_df, pd.DataFrame([row])])
            self.cnxn.commit()
            if len(Test.err_df) != 0:
                logging.info('テーブルにインポートできていないデータがあります')

    #SQLテーブル読み込み
    def read_SQL(self, table):
        try:
            #データの読み込み
            df_SQL = pd.read_sql('SELECT * FROM [dbo].['+table+'];', self.cnxn)
            return df_SQL
        except:
            logging.exception('所定のテーブルがありません')

    #SQLテーブルカラム取得
    def read_SQL_columns(self, table):
        try:
            #データの読み込み
            df_SQL = pd.read_sql('SELECT TOP 0 * FROM [dbo].['+table+'];', self.cnxn)
            columns = df_SQL.columns
            return columns
        except:
            logging.exception('所定のテーブルがありません')

    def logout(self):
        self.cnxn.commit()
        self.cursor.close()
        
if __name__ == '__main__':
    Test = DB('TEST', 'SQL Server', '128.1.137.214', 'test', 'test')
    columns = Test.read_SQL_columns('T_TEST')
    keys = Test.get_key('T_TEST') 
    df1 = Test.read_SQL('T_TEST')
    print('COLUMN_LIST')
    print(columns)
    print('\n')
    print('PRIMARY_KEYS')
    print(keys)
    print('\n')
    print(df1)
    print('\n')
    df2 = pd.DataFrame([['あ',1,1],[1,1,1]])
    df2.columns = columns
    print(df2)
    print('\n')
    Test.insert_SQL(df2, columns, 'T_TEST')
    df3 = Test.read_SQL('T_TEST')
    print(df3)
    print('\n')
    print(Test.err_df)
    print('\n')
    Test.insert_SQL(df1, columns, 'T_TEST')
    df4 = Test.read_SQL('T_TEST')
    print(df4)
    Test.logout()