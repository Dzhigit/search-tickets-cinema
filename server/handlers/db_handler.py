import psycopg2
from data.config import db_config


class BaseDBHandler:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=db_config["dbname"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"]
        )

    def insert_data(self, user_name, email, password):
        with self.connection.cursor() as cur:
            cur.execute("""
            INSERT INTO users (user_name, email, password)
            VALUES ('{}', '{}', '{}');
            """.format(user_name, email, password))
            self.connection.commit()

    def search_data(self):
        with self.connection.cursor() as cur:
            cur.execute("""SELECT * FROM users;""")
            info = cur.fetchall()
            return info

    def update_data(self, password, email):
        with self.connection.cursor() as cur:
            cur.execute("""UPDATE users SET password = '{}' WHERE email = '{}';""".format(password, email))
            self.connection.commit()


if __name__ == '__main__':
    db_handler = BaseDBHandler()
    print(db_handler.search_data())