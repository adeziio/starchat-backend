import sqlite3
from datetime import datetime

from ..utils import GithubService
from ..servers import ServerInfo

db_name = ServerInfo.getServerName()
table_name = "rooms"
room_id = "room_id"
create_date = "create_date"
room_name = "room_name"


def init():
    create_db()


def create_db():
    con = sqlite3.connect(db_name)
    with con:
        con.execute(
            f'''create table if not exists {table_name} (
                {room_id} INTEGER PRIMARY KEY AUTOINCREMENT,
                {create_date} datetime,
                {room_name} text not null unique
            )'''
        )
    con.close()


def hasRoom(roomname):
    ret = True
    try:
        ls = []
        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        query = f"select * from {table_name} where {room_name} = '{roomname}'"
        for row in cur.execute(query):
            ls.append({
                room_id: row[room_id],
                create_date: row[create_date],
                room_name: row[room_name],
            })
    except Exception as e:
        ret = False
    if (len(ls) == 0):
        ret = False
    return ret


def getAllRoom():
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
                room_id: row[room_id],
                create_date: row[create_date],
                room_name: row[room_name],
            })
    except Exception as e:
        status = 'error'
        message = str(e)
    return ls, len(ls), status, message


def addRoom(roomname):
    status = 'success'
    message = ''
    if (not hasRoom(roomname)):
        try:
            con = sqlite3.connect(db_name)
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            now = datetime.now()
            params = (now, roomname)
            cur.execute(
                f"insert into {table_name} values (null, ?, ?)", params
            )
            con.commit()
            con.close()
            GithubService.pushToGithub()
        except Exception as e:
            status = 'error'
            message = str(e)
    else:
        status = 'error'
        message = 'Room Name Already Exists'
    return status, message
