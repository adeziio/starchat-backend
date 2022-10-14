import os
import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet

from ..utils import GithubService
from ..servers import ServerInfo
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

db_name = ServerInfo.getServerName()
table_name = "users"
user_id = "user_id"
create_date = "create_date"
user_name = "user_name"
pass_word = "pass_word"
email = "email"

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
                {create_date} datetime,
                {user_name} text not null unique,
                {pass_word} text not null,
                {email} text not null
            )'''
        )
    con.close()


def hasUser(username):
    ret = True
    try:
        ls = []
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        query = f"select * from {table_name} where {user_name} = '{username}'"
        for row in cur.execute(query):
            ls.append({
                user_id: row[user_id],
                user_name: row[user_name],
            })
    except Exception as e:
        ret = False
    if (len(ls) == 0):
        ret = False
    return ret


def getUser(username):
    status = 'success'
    message = ''
    try:
        ls = []
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        query = f"select * from {table_name} where {user_name} = '{username}'"
        for row in cur.execute(query):
            ls.append({
                user_id: row[user_id],
                create_date: row[create_date],
                user_name: row[user_name],
                pass_word: fernet.decrypt(row[pass_word]).decode(),
                email: row[email]
            })
    except Exception as e:
        status = 'error'
        message = str(e)
    return ls, len(ls), status, message


def addUser(username, password, email):
    status = 'success'
    message = ''
    if (not hasUser(username)):
        try:
            con = sqlite3.connect(db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            now = datetime.now()
            params = (now, username, fernet.encrypt(password.encode()), email)
            cur.execute(
                f"insert into {table_name} values (null, ?, ?, ?, ?)", params
            )
            con.commit()
            con.close()
            GithubService.pushToGithub()
        except Exception as e:
            status = 'error'
            message = str(e)
    else:
        status = 'error'
        message = 'Username Already Exists'
    return status, message
