import os
import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet

from ..utils import GithubService
from ..servers import ServerInfo

db_name = ServerInfo.getServerName()
table_name = "messages"
message_id = "message_id"
message_content = "message_content"
user_name = "user_name"
create_date = "create_date"


def init():
    create_db()


def create_db():
    con = sqlite3.connect(db_name)
    with con:
        con.execute(
            f'''create table if not exists {table_name} (
                {message_id} INTEGER PRIMARY KEY AUTOINCREMENT,
                {message_content} text not null,
                {user_name} text not null,
                {create_date} datetime
            )'''
        )
    con.close()
