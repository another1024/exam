import pymysql
db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    db='db_exam',
    user='root',
    password='12345678',
    charset='utf8mb4'
)

cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
