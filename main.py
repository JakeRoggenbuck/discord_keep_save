import discord
import os.path
import sqlite3
from datetime import datetime


class Discord:
    def get_token(self):
        return open("token.txt", "r").read()

    def connect_client(self):
        return discord.Client()


class DataBase:
    def __init__(self):
        self.db_name = "database.db"

    def check_file(self):
        return os.path.isfile(self.db_name)

    def setup_db(self):
        if not self.check_file():
            self.connect_db()
            self.create_table()

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        sql_command = """
            CREATE TABLE message (
            message_number INTEGER PRIMARY KEY,
            content VARCHAR(2000),
            author VARCHAR(50),
            userid INTEGER(18),
            discriminator INTEGER(4),
            time TIME);"""
        self.write_create(sql_command)

    def write_create(self, command):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()

    def write(self, content, author, userid, discriminator, time):
        sql_command = """INSERT INTO message
        (message_number, content, author, userid, discriminator, time)
        VALUES (NULL, ?, ?, ?, ?, ?);"""
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(sql_command, (content, author, userid, discriminator, time))
        connection.commit()

    def read_db(self, command):
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(command)
        result = cursor.fetchall()
        return result

    def read_all(self, name):
        data = "SELECT * FROM message WHERE author = ?"
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(data, (name,))
        result = cursor.fetchall()
        for r in result:
            print(r)


DISCORD = Discord()
CLIENT = DISCORD.connect_client()
TOKEN = DISCORD.get_token()

DATABASE = DataBase()
DATABASE.setup_db()


@CLIENT.event
async def on_ready():
    print(f'We have logged in as {CLIENT.user}')


@CLIENT.event
async def on_message(message):
    content = message.content
    author = message.author.name
    userid = message.author.id
    discriminator = message.author.discriminator
    time = datetime.now().strftime("%H:%M:%S")
    if content[:2] == ";s":
        if content[2:] is not None:
            DATABASE.write(content[2:], author, userid, discriminator, time)

if __name__ == "__main__":
    CLIENT.run(TOKEN)
