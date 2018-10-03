import pymysql

from settings import Config

def connect():
    conn = Config.POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn,cursor


def connect_close(conn,cursor):
    cursor.close()
    conn.close()

def fetch_all(sql,args):
    conn,cursor = connect()

    cursor.execute(sql, args)
    record_list = cursor.fetchall()
    connect_close(conn,cursor)

    return record_list




def fetch_one(sql, args):
    conn, cursor = connect()
    cursor.execute(sql, args)
    result = cursor.fetchone()
    connect_close(conn, cursor)

    return result


def insert(sql, args):
    conn, cursor = connect()
    row = cursor.execute(sql, args)
    conn.commit()
    connect_close(conn, cursor)
    return row