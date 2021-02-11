# -*- coding: utf-8 -*-

import mysql.connector as mydb


class db_func:

    def __init__(self):

        # コネクションの作成
        self.conn = mydb.connect(
            user='ras',
            host='192.168.100.58',
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
            


    def create_table(self, table_type, table_name):
        # DB操作用にカーソルを作成
        cur = self.conn.cursor()

        if table_type == "user":
            # id, name, tokenを持つテーブルを作成 (存在していたら消してから作成)
            table = table_name
            cur.execute("DROP TABLE IF EXISTS {0};".format(table))
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS {0} (
                `id` int auto_increment primary key,
                `student_id` varchar(12) not null unique,
                `name` varchar(50) not null unique,
                `full_name` varchar(50) not null,
                `token` varchar(50) not null,
                `img_num` int default 0
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
                """.format(table)
            )

        elif table_type == "access":
            # id, 入室時間, 退出時間を持つテーブルを作成 (存在していたら消してから作成)
            table = table_name
            cur.execute("DROP TABLE IF EXISTS {0};".format(table))
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS {0} (
                `id` int not null,
                `date` date not null,
                `entry_time` datetime,
                `exit_time` datetime
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
                """.format(table)
            )
    

    def create_user(self, student_id, user_name, full_name, token, mac_addr, email):
        try:
            cur = self.conn.cursor()
            # クエリを作成
            query = """
                INSERT INTO user (student_id, name, full_name, token, mac_addr, email) 
                VALUES ('{0}','{1}','{2}','{3}', '{4}', '{5}');
                """.format(student_id, user_name, full_name,token, mac_addr, email)

            print("")
            print("ユーザの作成")
            print("")

            # 実行&コミット
            cur.execute(query)
            self.conn.commit()

        except mydb.Error as err:
            self.conn.rollback()
            return False


    def get_user_id(self, user_name):
        cur = self.conn.cursor()

        # ユーザ名から対応するIDを取得
        query = "SELECT id FROM user where name = '{0}';".format(user_name)

        print("")
        print("ユーザIDの取得")
        print("")

        cur.execute(query)

        
        get_value = cur.fetchone()[0]

        # IDを返す
        return get_value



    def select(self, table_name):
        # DB操作用にカーソルを作成
        cur = self.conn.cursor()

        # 全件取得
        query = "SELECT * FROM {0};".format(table_name)
        cur.execute(query)

        rows = cur.fetchall()
        for row in rows:
            print(row[0])


    def get_where(self, field_name, table_name, wh_field, value, not_flag=False):
        # DB操作用にカーソルを作成
        try:
            cur = self.conn.cursor()
        except:
            # コネクションの作成
            self.conn = mydb.connect(
                user='ras',
                host='192.168.100.68',
                port='3306',
                password='InfoNetworking',
                database='ras_db'
            )
            # コネクションが切れた時に再接続してくれるよう設定
            self.conn.ping(reconnect=True)

            # 接続できているかどうか確認
            print("get_where : {0}".format(self.conn.is_connected()))

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
        return get_value


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



    def update_where(self, table_name, field_name, value, user_id):
        try:
            cur = self.conn.cursor()

            # 値の更新
            query = "UPDATE {0} SET {1} = {2} WHERE id = {3};".format(
                table_name, 
                field_name,
                value,
                user_id
                )
        
            # 実行&コミット
            cur.execute(query)
            self.conn.commit()

        except mydb.Error as err:
            self.conn.rollback()
            raise err

    def check_user_name(self, user_name):
        # 既存のユーザかどうかチェックする
        cur = self.conn.cursor()
        query = "SELECT id FROM user where name = '{0}';".format(user_name)

        cur.execute(query)

        value = cur.fetchone()

        # 既存か新規か判定
        if value == None:
            return True
        else:
            return False
    

    def access_info_manage(self, user_id, date, access_time, entry_flag=False):
        cur = self.conn.cursor()

        # flagが「入室」の場合
        if entry_flag:
            # クエリの作成
            query = """
                INSERT INTO access (id, date, entry_time) 
                VALUES ({0}, '{1}', '{2}');
                """.format(user_id, date, access_time)
        else:
            query = """
                UPDATE access SET exit_time = '{0}' 
                WHERE date = '{1}' and id = {2} ;
                """.format(access_time, date, user_id)

        # 実行&コミット
        cur.execute(query)
        self.conn.commit()
    

    def get_user_list(self, user_id_list):
        cur = self.conn.cursor()

        if user_id_list == 1:
            query = """
            SELECT id, full_name, student_id, token FROM user where id = {0};
            """.format(user_id_list)
        else:
            query = """
            SELECT id, full_name, student_id, token FROM user where id in {0};
            """.format(user_id_list)

        cur.execute(query)
        get_value = cur.fetchall()

        # 取得した値を返す
        return get_value
            
    def reset_table(self):
        # self.create_table("user", "user")
        # self.create_table("access", "access")
        pass        
    


if __name__ == "__main__":
    db = db_func()

    

    field_name = "token"
    table_name = "user"
    wh_field = "name"

    # db.get_user_id("Komiya")
    # db.get_where(field_name, table_name, wh_field, "Komiya")
    db.reset_table()