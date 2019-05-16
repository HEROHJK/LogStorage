import sqlite3.dbapi2
from Logging import find_log_to_idx

'''
구현사항
* 태그 생성 : 태그를 생성
* 태그 삭제 : 태그를 삭제
* 태그 검색 : 태그를 검색
* 태그 수정 : 태그를 수정
* 로그 태그 삭제 : 해당 로그의 태그 삭제
* 로그 태그 입력 : 해당 로그의 태그 입력
* 리스트 태그 횟수 조회 : 태그리스트에서 태그 횟수 조회
* 리스트 태그 조회 : 태그리스트에서 해당 태그 사용중인 로그 조회
'''


def insert_tag(conn: sqlite3.dbapi2, tag_name: str):
    c = conn.cursor()
    result = find_tag(conn, tag_name)
    if result is not -1:
        return result
    # 태그가 없으면 새로 등록
    query = 'INSERT INTO "tag" ("name") VALUES(:tagName)'
    c.execute(query, {"tagName": tag_name})
    conn.commit()
    query = 'SELECT idx FROM tag WHERE name = :tagName LIMIT 1'
    c.execute(query, {"tagName": tag_name})
    result = c.fetchone()[0]

    return result


def delete_tag(conn: sqlite3.dbapi2, tag_name: str):
    c = conn.cursor()
    result = find_tag(conn, tag_name)
    if result == -1:
        return 1
    try:
        # 리스트에 해당 태그들 삭제
        query = 'DELETE FROM "tag_list" WHERE tagidx=:tagIdx'
        c.execute(query, {"tagIdx": result})
        conn.commit()
        # 태그 삭제
        query = 'DELETE FROM "tag" WHERE idx=:tagIdx'
        c.execute(query, {"tagIdx": result})
        conn.commit()

        return 1
    except Exception as e:
        print(str(e))
        return 0


def find_tag(conn: sqlite3.dbapi2, tag_name: str):
    c = conn.cursor()
    query = 'SELECT idx FROM "tag" WHERE name=:tagName'
    c.execute(query, {"tagName": tag_name})
    result = c.fetchone()
    idx = -1
    if result is not None:
        idx = result[0]

    return idx


def modify_tag(conn: sqlite3.dbapi2, tag_name: str, new_tag_name: str):
    c = conn.cursor()
    result = find_tag(conn, tag_name)
    if result is -1:
        return result

    query = 'UPDATE tag SET name = :newtagname WHERE name = :tagname'
    c.execute(query, {"newtagname": new_tag_name, "tagname": tag_name})
    conn.commit()

    return 1


def insert_tag_to_log(conn: sqlite3.dbapi2, tag_name: str, logidx: int):
    c = conn.cursor()
    tag_result = find_tag(conn, tag_name)
    log_result = find_log_to_idx(conn, logidx)
    if (tag_result == -1) or (log_result == -1):
        return -1
    query = '''INSERT INTO "tag_list" ("tagidx", "logidx") VALUES(:tagIdx, :logIdx)'''
    c.execute(query, {"tagIdx": tag_result, "logIdx": logidx})
    conn.commit()

    return 1


def delete_tag_to_log(conn: sqlite3.dbapi2, tagname: str, logidx: int):
    c = conn.cursor()
    tag_result = find_tag(conn, tagname)
    log_result = find_log_to_idx(conn, logidx)
    if (tag_result == -1) or (log_result == -1):
        return -1
    query = 'DELETE FROM "tag_list" WHERE tagidx=:tagIdx AND logidx=:logIdx'
    c.execute(query, {"tagIdx": tag_result, "logIdx": log_result})
    conn.commit()

    return 1


def find_tag_count_to_list(conn: sqlite3.dbapi2, tag_name: str):
    c = conn.cursor()
    result = find_tag(conn, tag_name)
    if result == -1:
        return 0

    query = 'SELECT count(tagidx) FROM "tag_list" WHERE tagidx=:tagIdx'
    c.execute(query, {"tagIdx": result})
    count = c.fetchone()[0]

    return count


def find_tag_to_list(conn: sqlite3.dbapi2, tag_name: str, logidx: int = 0):
    c = conn.cursor()
    result = find_tag(conn, tag_name)
    if result == -1 or find_tag_count_to_list(conn, tag_name) == 0:
        return []
    query = ''
    if logidx == 0:
        query = 'SELECT logidx FROM "tag_list" WHERE tagidx=:tagIdx'
        c.execute(query, {"tagIdx": result})
    else:
        query = 'SELECT logidx FROM "tag_list" WHERE tagidx=:tagIdx AND logidx=:logIdx'
        c.execute(query, {"tagIdx": result, "logIdx": logidx})
    rows = c.fetchall()
    logs = []
    for row in rows:
        logs.append(row[0])

    return logs

