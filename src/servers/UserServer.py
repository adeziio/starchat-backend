import os
import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet

from ..utils import GithubService
from ..servers import ServerInfo

db_name = ServerInfo.getServerName()
table_name = "users"
user_id = "user_id"
user_name = "user_name"
pass_word = "pass_word"
create_date = "create_date"

key = bytes(os.getenv("USER_CRYPTO_KEY"), encoding='utf-8')
fernet = Fernet(key)


def init():
    create_db()


def create_db():
    con = sqlite3.connect(db_name)
    with con:
        con.execute(
            f'''create table if not exists {table_name} (
                {user_id} INTEGER PRIMARY KEY AUTOINCREMENT,
                {user_name} text not null unique,
                {pass_word} text not null,
                {create_date} datetime
            )'''
        )
    con.close()
