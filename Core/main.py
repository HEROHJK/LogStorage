import CreateUser
import Logging

#db = CreateUser.CreateUser('herohjk', 'test123')
from dbPath import dbPath
db = dbPath+'herohjk.db'
import sqlite3

conn = sqlite3.connect(db)

Logging.insert_log(conn=conn, message='테스트', tags=["테스트","첫등록", "테스트"])