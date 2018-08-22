# -*- coding:utf-8 -*-
import sqlite3
import time


def log_to_file(txt=None):
    if not txt:
        return None
    with open('log.txt', 'a') as fp:
        fp.writelines("%s: %s \n" % (str(time.asctime()), txt))

def open_sqlite(db_name="tmp.db3", tb_name="video_arrange"):
    """创建sqlite数据库存放数据"""
    # con = sqlite3.connect(":memory:")
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    # 文件名, 完整路径, NSFw, 上传结果, 处理时间, 备注
    # cur.executescript("""drop table if exists video_arrange""")
    cur.executescript("""
         create table if not exists %s(
         fid INTEGER PRIMARY KEY AUTOINCREMENT,
         file_name char(255),
         file_local_path char(255),
         NSFW intern,
         upload_result char(255),
         upload_success intern,
         op_time char(255),
         remarkes char(255))""" % (tb_name))
    # cur.close()
    return (con, cur)

def insert_data(con, cur, tb_name=None, data=None):
    if not data or (not type(data) is tuple):
        return None
    try:
        cur.execute(
            'insert into '+ tb_name + ' (file_name, file_local_path, NSFW, upload_result, upload_success, op_time, remarkes)'
            'values (?,?,?,?,?,?,?)', data)
        con.commit()
        return True
    except Exception as bug:
        print(bug)
        return None
