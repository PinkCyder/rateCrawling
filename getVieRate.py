from bs4 import BeautifulSoup
import requests
#import pandas as pd
#import sqlite3
import cx_Oracle
from sys import modules
from decimal import Decimal
import time

#建立資料庫連線
connection = cx_Oracle.connect('BPM_TEST/BPM12345@192.168.82.13/orcl',encoding='UTF-8',nencoding='UTF-8') 
c = connection.cursor()

#抓資料的時間
localtime = time.localtime()
day = time.strftime("%Y-%m-%d", localtime) #%I:%M:%S %p
print(day)

#串越南匯率網站
url = 'https://www.indovinabank.com.vn/en/lookup/rates'
html = requests.get(url)
doc = html.text
#print(doc)
soup = BeautifulSoup(html.text, 'lxml')
#soup = BeautifulSoup(html.text, 'html.parser')
#解析抓到的內容--每個網站不同
currency = soup.find_all("span",{"class":"pull-right"})#"country-select"})
ccstitle = BeautifulSoup(str(currency), 'html.parser')
arr = ccstitle.text.replace('     ','').split(' ,')  #轉換的空格只要有誤，資料就會跑掉，目前是5個
print(arr)
print(len(arr))
for i in range(len(arr)):
    arr[i] = arr[i].replace(' ','').replace('[','').replace(']','')
print(arr)
print(len(arr))

rate = soup.find_all("span",{"class":"red"})
stitle = BeautifulSoup(str(rate), 'html.parser')
arr2 = stitle.text.replace('[','').split(', ') 
def split_list(l, n):
  # 將list分割 (l:list, n:每個matrix裡面有n個元素)
  for idx in range(0, len(l), n):
    yield l[idx:idx+n]
reeeee = list(split_list(arr2, 3)) #將list分割成每份中有3個元素
print(reeeee) #[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]

for i in range(len(arr)):
    cur = arr[i]
    cash = reeeee[i][0].replace(',','')
    print(type(cash))  #cash不參與計算
    #cash = Decimal(cash)
    transfer = reeeee[i][1].replace(',','')
    print(transfer)
    if(transfer==''):  
        transfer = 0
        bankbuy = 0  #分母不可為0，所以直接強制給0
        bankmid = 0  #分母不可為0，所以直接強制給0
    else:
        transfer = Decimal(transfer)
        bankbuy = 1/transfer
    sold = reeeee[i][2].replace(']','').replace(',','')
    if(sold==''):
        sold=str(0)
        banksold = 0
        bankmid = 0
    else:
        sold = Decimal(sold)
        banksold = 1/sold
        avg = (transfer+sold)/2
        bankmid = 1/avg
    bankbuy = str(bankbuy)
    banksold = str(banksold)
    bankmid = str(bankmid)
    sold = str(sold)
    transfer = str(transfer)
    sqll ="SELECT count(1) FROM VIERATE WHERE DAY = TO_DATE('"+day+"','yyyy-mm-dd') AND CURRENCY = '"+cur+"' "
    c.prepare(sqll)
    c.execute(sqll)
    rows = c.fetchone()
    print(rows[0])
    if(rows[0]<=0):
        #sql = 'insert into 資料庫.資料表(欄位1, 欄位2, 欄位3) values(@變數1,@變數2,@變數3)'
            sql = "INSERT INTO VIERATE(DAY,CURRENCY,CASH,TRANSFER,SOLD,BANKBUY,BANKSOLD,BANKMID) VALUES (TO_DATE('"+day+"','yyyy-mm-dd'),'"+cur+"', '"+cash+"', '"+transfer+"', '"+sold+"','"+bankbuy+"','"+banksold+"','"+bankmid+"')"
            print(sql)
            c.prepare(sql)
            c.execute(sql)
            connection.commit()
connection.close()