import sqlite3
from Encrypter import encrypter
from dbPath import dbPath

'''
* 사용자 생성
* 입력 : ID/PW
* 설명 : ID와PW를 입력받아 새로운 sqliteDB파일을 만든다.
'''


def create_user(id: str, pw: str):
    __create_tables(id)

    conn = sqlite3.connect(dbPath+id+'.db')
    c = conn.cursor()
    enc_pw = encrypter.encrypt('pw')
    c.execute('INSERT INTO "userinfo" ("key", "value") VALUES ("id", "'+id+'")')
    c.execute('INSERT INTO "userinfo" ("key", "value") VALUES ("pw", "' + enc_pw + '")')

    conn.commit()

    conn.close()

    return dbPath+id+'.db'


def __create_tables(id: str):
    conn = sqlite3.connect(dbPath + id + '.db')
    c = conn.cursor()

    f = open("query.txt", 'r')
    create_query = ''
    while True:
        line = f.readline()
        create_query += line
        if not line:
            break
    f.close()

    c.executescript(create_query)

    conn.close()