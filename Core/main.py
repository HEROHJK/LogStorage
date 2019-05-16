import CreateUser
import Logging

db = CreateUser.CreateUser('herohjk', 'test123')

Logging.InsertLog(userdb=db, message='테스트', tags=["테스트","첫등록", "테스트"])