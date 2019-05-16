from time import time
import sqlite3, sqlite3.dbapi2

current_milli_time = lambda: int(round(time() * 1000))


def InsertLog(conn: sqlite3.dbapi2, message:str, tags:[]):
    c = conn.cursor()
    #로그인포생성
    c.execute('INSERT INTO "loginfo" ("last") VALUES (0)')
    conn.commit()
    #생성된 번호 가져오기
    c.execute('SELECT idx FROM loginfo ORDER BY idx DESC')
    idx = c.fetchone()[0]
    #로그작성
    result = c.execute('INSERT INTO "log" ("infoidx", "message", "writedate") VALUES(?,?,?)', (idx, message, current_milli_time()))
    conn.commit()
    #로그번호 가져오기
    query = 'SELECT idx FROM log WHERE infoidx = :infoIdx ORDER BY idx DESC'
    c.execute(query, {"infoIdx": idx})
    logidx = c.fetchone()[0]

    if tags is not None:
        #태그 수만큼 반복
        for tag in tags:
            #태그를 찾는다
            query = 'SELECT idx FROM tag WHERE name = :tagName LIMIT 1'
            c.execute(query, {"tagName": tag})
            tagidx = -1
            result = c.fetchone()
            if result == None:
                #태그가 없으면 새로 등록
                query = 'INSERT INTO "tag" ("name") VALUES(:tagName)'
                c.execute(query, {"tagName":tag})
                conn.commit()
                query = 'SELECT idx FROM tag WHERE name = :tagName LIMIT 1'
                c.execute(query, {"tagName": tag})
                result = c.fetchone()
            tagidx = result[0]
            #태그리스트에서 해당 조건 검색
            query = 'SELECT count(*) FROM "tag_list" WHERE tagidx=:tagIdx AND logidx=:logIdx'
            c.execute(query, {"tagIdx":tagidx, "logIdx":idx})
            result = c.fetchone()[0]
            if result == 0:
                #조건대로 찾아서 안나오면 등록
                query = 'INSERT INTO "tag_list" ("tagidx", "logidx") VALUES(:tagIdx, :logIdx)'
                c.execute(query, {"tagIdx":tagidx, "logIdx":idx})
                conn.commit()
    return idx

def find_log_to_idx(conn: sqlite3.dbapi2, logidx:int):
    c = conn.cursor()
    query = 'SELECT idx FROM "loginfo" WHERE idx=:logIdx'
    c.execute(query, {"logIdx": logidx})
    result = c.fetchone()
    if result == None:
        return -1
    return result[0]

#def ModifyLog(conn: sqlite3.dbapi2, "",message:str, tags:[])