import CreateUser
import Logging

db = CreateUser.create_user('herohjk', 'test123')
from dbPath import dbPath
db = dbPath+'herohjk.db'
import sqlite3

conn = sqlite3.connect(db)

number = Logging.insert_log(conn=conn, message='테스트', tags=["테스트","첫등록", "테스트"])
Logging.modify_log(conn,number,"뉴메시지")
Logging.modify_log(conn, number, "뉴메시지2", ["테스트", "수정된등록"])