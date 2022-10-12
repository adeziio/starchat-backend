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


def getAllMessages():
    status = 'success'
    message = ''
    try:
        ls = []
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        query = f"select * from {table_name}"
        for row in cur.execute(query):
            ls.append({
                message_id: row[message_id],
                message_content: row[message_content],
                user_name: row[user_name],
                create_date: row[create_date]
            })
    except Exception as e:
        status = 'error'
        message = str(e)
    return ls, len(ls), status, message


def addMessage(username):
    status = 'success'
    message = ''
    try:
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        now = datetime.now()
        params = (username, now)
        cur.execute(
            f"insert into {table_name} values (null, ?, ?)", params
        )
        con.commit()
        con.close()
        GithubService.pushToGithub()
    except Exception as e:
        status = 'error'
        message = str(e)
    return status, message
