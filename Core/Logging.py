from time import time
import sqlite3.dbapi2
import Tag

current_milli_time = lambda: int(round(time() * 1000))


def insert_log(conn: sqlite3.dbapi2, message:str, tags:[]):
    c = conn.cursor()
    # 로그인포생성
    c.execute('INSERT INTO "loginfo" ("last") VALUES (0)')
    conn.commit()
    # 생성된 번호 가져오기
    c.execute('SELECT idx FROM loginfo ORDER BY idx DESC')
    idx = c.fetchone()[0]
    # 로그작성
    c.execute('INSERT INTO "log" ("infoidx", "message", "writedate") VALUES(?,?,?)',
              (idx, message, current_milli_time()))
    conn.commit()
    # 로그번호 가져오기
    query = 'SELECT idx FROM log WHERE infoidx = :infoIdx ORDER BY idx DESC'
    c.execute(query, {"infoIdx": idx})

    if tags is not None:
        # 태그 수만큼 반복
        for tag in tags:
            # 태그를 찾는다
            tag_find_result = Tag.find_tag(conn, tag)
            tagidx = -1
            if tag_find_result == -1:
                # 태그가 없으면 새로 등록
                Tag.insert_tag(conn, tag)
            tagidx = Tag.find_tag(conn,tag)
            # 태그리스트에서 해당 조건 검색
            find_result = Tag.find_tag_to_list(conn, tag, idx)
            if len(find_result) > 0:
                # 조건대로 찾아서 안나오면 등록
                Tag.insert_tag_to_log(conn, tag, idx)
    return idx


def modify_log(conn: sqlite3.dbapi2, logidx: int, message: str, tags: [] = []):
    c = conn.cursor()

    # 리비전 확인
    query = 'SELECT last FROM "loginfo" WHERE idx=:logIdx'
    c.execute(query, {"logIdx": logidx})
    revision = c.fetchone[0]

    # 로그작성
    query = 'INSERT INTO "log" ("infoidx", "message", "writedate", "revisioncount") ' \
            'VALUES(:logIdx, :Message, :writeDate, :revisionCount)'

    c.execute(query, {"logIdx": logidx, "Message": message, "writeDate": current_milli_time(),
                      "revisionCount": revision+1})
    conn.commit()

    # 로그인포에서 리비전 변경
    query = 'UPDATE "loginfo" SET last=:revisionCount WHERE idx=:logIdx'
    c.execute(query, {"revisionCount": revision+1, "logIdx": logidx})

    # 태그가 들어왔다면, 로그의 태그 모두 삭제 후 등록된 태그들 삽입
    if len(tags) > 0:
        # 모든 태그 삭제
        Tag.delete_all_tag_to_log(conn, logidx)
        for tag in tags:
            # 태그를 찾는다
            tag_find_result = Tag.find_tag(conn, tag)
            tagidx = -1
            if tag_find_result == -1:
                # 태그가 없으면 새로 등록
                Tag.insert_tag(conn, tag)
            tagidx = Tag.find_tag(conn, tag)
            # 태그리스트에서 해당 조건 검색
            find_result = Tag.find_tag_to_list(conn, tag, logidx)
            if len(find_result) > 0:
                # 조건대로 찾아서 안나오면 등록
                Tag.insert_tag_to_log(conn, tag, logidx)

