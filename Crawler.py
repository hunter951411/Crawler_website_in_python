import re
from bs4 import BeautifulSoup
import urllib2
import requests
import mysql.connector
#Ket noi voi csdl
conn = mysql.connector.Connect(host='127.0.0.1',user='root',password='trung',database='CrawlerDB')
c = conn.cursor()
#Ham lay thong tin gom URL, CODE, NAME, RANK va them vao csdl
def Insert_DB(url):
	url = 'http://data.alexa.com/data?cli=10&url=' + url
	req = urllib2.Request(url)
	response = urllib2.urlopen(req).read()
	regexUrl = 'Y\s?URL="\s?(.+?)\s?\/"'
	Url = re.findall(regexUrl, response)
	regexCC = 'CODE="\s?(.+?)\s?\"'	
	Code  = re.findall(regexCC, response)
	regexName = 'NAME="\s?(.+?)\s?\"'
	Name  = re.findall(regexName, response)
	regexRank = '\"\s?RANK="\s?(.+?)\s?\"'
	Rank  = re.findall(regexRank, response)
	MANGDL = [Url, Code,Name,Rank]
	if MANGDL[1] == []:
		#print "Mang rong!!!"
		#Neu khong the tim duoc Code ta gan cho MANGDL la mang rong va khong them vao csdl
		MANGDL = []
	#print MANGDL	
	if MANGDL != []:
		status = 0
		sql = "Select Url from CrawlerTB Where Url='"+Url[0]+"'"
		c.execute(sql)
		for row in c:
			#print (row)
			if (row[0]) == Url[0]:
				status = 1
				#Neu tim thay gia tri giong nhau trong csdl se gan status = 1 va khong them vao csdl
				#print status
				#print Url[0]
		conn.commit()
		#print status
		if status == 0:
			#Them vao csdl
			sql = "Insert into CrawlerTB(Url,Code,Name,Rank) Values('"+Url[0]+"','"+Code[0]+"','"+Name[0]+"',"+Rank[0]+")"
			#print sql
			c.execute(sql)
			conn.commit()
	return MANGDL

#Ham thuc hien get link, neu loi thi hien ra thong bao
def Get_Link(url):
	MANG_GET = [] #Mang chua cac link co trong mot url
	MANG_DEM = []
	#Su dung try-except de bat ngoai le truong hop url duoc dua vao khong get duoc
	try:
		#Thuc hien phat hien cac link trong mot url dung BeautifulSoup	
		r = requests.get("http://"+url)
		data = r.text
		soup = BeautifulSoup(data, "lxml")
		regexLink = 'href=\"http://s?(.+?)\s?\"'
		link = re.findall(regexLink, data)
		for i in link:	
			url = re.sub(r'/.*$',"",i)
			#Goi den ham Insert_DB de thuc hien lay cac thong so URL, CODE, NAME, RANK cua url va day vao csdl
			#Insert_DB(url)
			#Day URL tim thay vao MANG_DEM, de thong ke ra mang chua tat cac cac link trong url do
			MANG_DEM.append(url) 
		MANG_DEM = set(MANG_DEM)
		#Loai tru nhung ket qua giong nhau trong MANG_DEM va luu vao MANG_GET
		for i in MANG_DEM:
			MANG_GET.append(i)
	except:
		print "Link khong get duoc!!!!"
	return MANG_GET


#Ham thuc hien crawl qua do sau
MANG_DA_GET = []
def Do_sau(dosau, MANGDL):
	if dosau > 0:
		print "************** DO SAU = "+str(dosau)+" ****************"
		#Thuc lay cac thong so cua cac URL trong MANGDL
		MANG_CHUA_GET = []
		MANG_DEM = []
		for i in MANGDL:
				print "DANG GET: ",i
				Insert_DB(i)
				MANG_DA_GET.append(i)
				for j in Get_Link(i):
					MANG_CHUA_GET.append(j)
		#Loai bo nhung link trung lap trong MANG_CHUA_GET		
		MANG_DEM = set(MANG_CHUA_GET)
		del MANG_CHUA_GET[:] 
		for i in MANG_DEM:
			MANG_CHUA_GET.append(i)
		print MANG_CHUA_GET
		print "\n\n\n"
		dosau = dosau -1
		Do_sau(dosau, MANG_CHUA_GET)

#Ham chinh thuc hien chay chuong trinh
def Run(dosau, url):
	print "************** DO SAU = "+str(dosau)+" ****************"
	print "DANG GET LINK: ",url
	Insert_DB(url)
	MANG_DA_GET.append(url)
	MANG = []
	MANG = Get_Link(url)
	MANG.remove(url)
	print MANG

	print "\n\n\n"	#Tao khoang cach giua cac do sau quet
	dosau = dosau - 1 #Do sau duoc giam di 1 sau lan quyet dau tien
	#Thuc hien quet do sau neu do sau lon hon 0
	if dosau != 0:	
		Do_sau(dosau, MANG)

	#Thong bao quet hoan tat khi ket thuc	
	print "Quet hoan tat!!!!"

#Nhap url va do sau muon crawler
url = raw_input("Nhap url: ")
dosau = int(raw_input("Nhap do sau: "))

#Thuc hien goi ham run de chay chuong trinh
Run(dosau, url)