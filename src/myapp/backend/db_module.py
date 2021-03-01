# -*- coding: utf-8 -*-

import mysql.connector as mydb


class db_func:

    def __init__(self):

        # コネクションの作成
        self.conn = mydb.connect(
            user='ras',
            host='192.168.100.60',
            port='3306',
            password='InfoNetworking',
            database='ras_db'
        )

        # コネクションが切れた時に再接続してくれるよう設定
        self.conn.ping(reconnect=True)

        # 接続できているかどうか確認
        try:
            print(self.conn.is_connected())
        except mydb.Error as err:
            print("Something went wrong: {}".format(err))


    def get_access_info(self, field_name, wh_field, value):
        # DB操作用にカーソルを作成
        cur = self.conn.cursor()
        
        query = "SELECT {0} FROM access where {1} = '{2}';".format(
            field_name, 
            wh_field, 
            value
        )

        cur.execute(query)
        get_value = cur.fetchall()

        # 取得した値を返す
        return get_value


    def get_where(self, field_name, table_name, wh_field, value, not_flag=False):

        cur = self.conn.cursor()

        if type(value) is str:
            if not_flag:
                query = "SELECT {0} FROM {1} where {2} != '{3}';".format(
                    field_name, 
                    table_name,
                    wh_field, 
                    value
                )
            else:
                query = "SELECT {0} FROM {1} where {2} = '{3}';".format(
                    field_name, 
                    table_name,
                    wh_field, 
                    value
                )

        else:
            if not_flag:
                query = "SELECT {0} FROM {1} where {2} != {3};".format(
                    field_name, 
                    table_name,
                    wh_field, 
                    value
                )
            else:
                query = "SELECT {0} FROM {1} where {2} = {3};".format(
                    field_name, 
                    table_name,
                    wh_field, 
                    value
                )

        cur.execute(query)
        get_value = cur.fetchall()

        # 取得した値を返す
        return get_value[0]


