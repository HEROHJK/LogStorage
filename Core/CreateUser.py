import sqlite3
from Encrypter import encrypter
from dbPath import dbPath

'''
* 사용자 생성
* 입력 : ID/PW
* 설명 : ID와PW를 입력받아 새로운 sqliteDB파일을 만든다.
'''
def CreateUser(id:str, pw:str):
    __CreateTables(id)

    conn = sqlite3.connect(dbPath+id+'.db')
    c = conn.cursor()
    encPw = encrypter.encrypt('pw')
    c.execute('INSERT INTO "userinfo" ("key", "value") VALUES ("id", "'+id+'")')
    c.execute('INSERT INTO "userinfo" ("key", "value") VALUES ("pw", "' + encPw + '")')

    conn.commit()

    conn.close()


def __CreateTables(id):
    conn = sqlite3.connect(dbPath + id + '.db')
    c = conn.cursor()

    f = open("query.txt", 'r')
    createQuery = ''
    while True:
        line = f.readline()
        createQuery += line
        if not line: break
    f.close()

    c.executescript(createQuery)

    conn.close()