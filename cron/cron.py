# cron file
import pymysql
import datetime
from cron_setting import db

del_limit = datetime.date.today() - datetime.timedelta(days=7) # 일주일 전 날짜

conn = pymysql.connect(host=db['host'], user=db['user'], password=db['pw'], db=db['db'])
print(f'{datetime.date.today()} db connection success')

sql = "DELETE FROM recommendation WHERE recommend_at < '%s';" %(del_limit) # 일주일 이전의 추천리스트들은 삭제
print(sql)
curs = conn.cursor()
result = curs.execute(sql)
print('delete execute result : ', result)

curs.close()
conn.close()
