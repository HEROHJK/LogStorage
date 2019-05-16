import CreateUser
import Logging
import Tag

# db = CreateUser.CreateUser('herohjk', 'test123')
from dbPath import dbPath
db = dbPath+'herohjk.db'
import sqlite3

conn = sqlite3.connect(db)

Logging.InsertLog(conn=conn, message='테스트', tags=["테스트","첫등록", "테스트"])

# result = Tag.FindTagToList(conn,"테스트",1)
# result = Tag.ModifyTag(conn,"테스트","뉴테스트")
result = Tag.find_tag_to_list(conn,"테스트", 3)
print(result)