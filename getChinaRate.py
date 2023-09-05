from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import cx_Oracle
from sys import modules
from decimal import Decimal

#爬取網頁資料
url = 'https://www.safe.gov.cn/AppStructured/hlw/RMBQuery.do'
html = requests.get(url)
doc = html.text
s = BeautifulSoup(html.text, 'html.parser')    #整理格式
dfs = pd.read_html(s.select('#InfoTable')[0].prettify('utf-8-sig'),header=0)
df_rates=dfs[0]

print(df_rates)

df_rates=pd.melt(df_rates,col_level=0, id_vars=['日期'])  #降維
df_rates.columns = ['date', 'currency', 'exchange']

print(df_rates)

connection = cx_Oracle.connect('BPM_TEST/BPM12345@192.168.82.13/orcl',encoding='UTF-8',nencoding='UTF-8') 
c = connection.cursor()

sql = '''select * from CHIRATE''' # 輸入你要查找的資料表語法  
df = pd.read_sql(sql, con=connection) # 將資料表存成DataFrame格式

len(df)
print(df.columns)
print(df.items())
M = []
for name,oo in df.items():
    M.append((name,oo))
    pass

len(M)

for j in df_rates.index:
    day = df_rates['date'][j]
    print (day)
    dfcurrency = df_rates['currency'][j]
    print(dfcurrency)
    if(dfcurrency == "美元"):
        cur_id = "USD"
    elif(dfcurrency == "欧元"):
        cur_id = "EUR"   
    elif(dfcurrency == "日元"):
        cur_id = "JPY"
    elif(dfcurrency == "港元"):
        cur_id = "HKD"
    elif(dfcurrency == "英镑"):
        cur_id = "GBP"
    elif(dfcurrency == "林吉特"):
        cur_id = "MYR"
    elif(dfcurrency == "卢布"):
        cur_id = "BYN"
    elif(dfcurrency == "澳元"):
        cur_id = "AUD"
    elif(dfcurrency == "加元"):
        cur_id = "CAD"
    elif(dfcurrency == "新西兰元"):
        cur_id = "NZD"
    elif(dfcurrency == "新加坡元"):
        cur_id = "SGD"
    elif(dfcurrency == "瑞士法郎"):
        cur_id = "CHF"
    elif(dfcurrency == "兰特"):
        cur_id = "ZAR"
    elif(dfcurrency == "韩元"):
        cur_id = "KRW"
    elif(dfcurrency == "迪拉姆"):
        cur_id = "AED"
    elif(dfcurrency == "里亚尔"):
        cur_id = "IRR"  #里亞爾有夠多，這是伊朗的
    elif(dfcurrency == "福林"):
        cur_id = "HUF"
    elif(dfcurrency == "兹罗提"):
        cur_id = "PLN"
    elif(dfcurrency == "丹麦克朗"):
        cur_id = "DKK"
    elif(dfcurrency == "瑞典克朗"):
        cur_id = "SEK"
    elif(dfcurrency == "挪威克朗"):
        cur_id = "NOK"
    elif(dfcurrency == "里拉"):
        cur_id = "TRY"
    elif(dfcurrency == "比索"):
        cur_id = "PHP"  #比索更多...這是菲律賓的
    elif(dfcurrency == "泰铢"):
        cur_id = "THB"
    dfexchange = df_rates['exchange'][j]
    dfexchange = dfexchange.astype(str)
    dfexchange = Decimal(dfexchange)
    fin_exc = dfexchange/100
    fin_exc = str(fin_exc)
    print(fin_exc)
    dfexchange = str(dfexchange)
    sqll ="SELECT count(1) FROM CHIRATE WHERE DAY = TO_DATE('"+day+"','yyyy-mm-dd') AND CURRENCY = '"+dfcurrency+"' "
    c.prepare(sqll)
    c.execute(sqll)
    rows = c.fetchone()
    print(rows[0])
    if(rows[0]<=0):
    #sql = 'insert into BPM_TEST.CHIRATE(DAY , ,欄位3) values(@變數1,@變數2,@變數3)'
        sql = "INSERT INTO CHIRATE(DAY,CURRENCY,CUR_ID,EXCHANGE,FINAL_EXC) VALUES (TO_DATE('"+day+"','yyyy-mm-dd'),'"+dfcurrency+"', '"+cur_id+"', '"+dfexchange+"', '"+fin_exc+"')"
        print(sql)
        c.prepare(sql)
        c.execute(sql)
        connection.commit()
connection.close()

