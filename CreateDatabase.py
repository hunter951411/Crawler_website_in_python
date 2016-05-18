import mysql.connector
#login vao csdl mysql
conn = mysql.connector.Connect(host='127.0.0.1',user='root',password='trung')
c = conn.cursor()
#Tao database
sql = "CREATE DATABASE IF NOT EXISTS CrawlerDB"
c.execute(sql)
conn.commit()
#Su dung database vua tao ra
sql = "USE CrawlerDB"
c.execute(sql)
conn.commit()
#Tao table
sql = ("""CREATE TABLE IF NOT EXISTS CrawlerTB(
    Ids	int	PRIMARY KEY NOT NULL AUTO_INCREMENT,
	Url		varchar(30),
	Code	varchar(30),
	Name	varchar(30),
	Rank		int)""")
c.execute(sql)
conn.commit()
#Kiem tra cac cot trong bang
# sql = "SHOW COLUMNS FROM CrawlerTB"
c.execute(sql)
for row in c:
	print (row)
conn.commit()