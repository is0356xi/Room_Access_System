# -*- coding: utf-8 -*-

import mysql.connector as mydb


class db_func:

    def __init__(self):

        # コネクションの作成
        self.conn = mydb.connect(
            user='username',
            host='hostname',
            port='3306',
            password='password',
            database='dbname'
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
                `entr_time` datetime,
                `exit_time` datetime
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
                """.format(table)
            )
    

    def create_user(self, student_id, user_name, full_name, token):
        try:
            cur = self.conn.cursor()
            # クエリを作成
            query = """
                INSERT INTO user (student_id, name, full_name, token) 
                VALUES ('{0}','{1}','{2}','{3}');
                """.format(student_id, user_name, full_name,token)

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

            cur.execute(query)
        
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

    def reset_table(self):
        self.create_table("user", "user")
        self.create_table("access", "access")





if __name__ == "__main__":
    db = db_func()