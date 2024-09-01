import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

stock ='2002'
date = '20240712'

"""
 # 要抓取的網址
url = 'https://tw.stock.yahoo.com/q/q?s=' + stock 

#請求網站
req = requests.get(url)

#防呆
if req.status_code != 200:
    print(f"股票代码 {stock} 不存在")
    sys.exit()  # 退出程序

#將整個網站的程式碼爬下來
soup = BeautifulSoup(req.content, "html.parser")

#stock資訊list
stock_text = []

# 查找stock中文名
Ch = soup.find('h1', class_='C($c-link-text) Fw(b) Fz(24px) Mend(8px)')

# 查找stock代號
id = soup.find('span', class_='C($c-icon) Fz(24px) Mend(20px)')

stock_text.append(Ch.text)
stock_text.append(id.text)

# 查找stock當日交易內容
ul_element = soup.find('ul', class_='D(f) Fld(c) Flw(w) H(192px) Mx(-16px)')

# 如果找到该<ul>元素
if ul_element:
    # 查找<ul>元素中的所有<span>元素
    spans = ul_element.find_all('span')
    
    # 遍历这些<span>元素，并筛选出非空白的文本内容
    for i in spans:
        text = i.text
        if text:  # 如果文本内容非空
            stock_text.append(text)

# 打印存储的非空白<span>内容的列表
for i in range(0, len(stock_text) - 1, 2):
    print(f"{stock_text[i]}\t{stock_text[i+1]}")
"""
"""
#畫圖用
add = "https://query1.finance.yahoo.com/v8/finance/chart/2330.TW?period1=0&period2=1549258857&interval=1d&events=history&=hP2rOschxO0"
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0' }
response = requests.get(add, headers=headers)
print(response.text)
"""

url = f"https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={date}&stockNo={stock}&response=json&_=1725123305039"
req = requests.get(url)

#防呆
if req.status_code != 200:
    print(f"股票代码 {stock} 不存在")
    sys.exit()  # 退出程序

# 解析 JSON
json = req.json()

# 提取 
title = json['title']
fields = json['fields']
data = json['data']

df = pd.DataFrame(data, columns=fields)

#output  
print(title)
print(df)

with open('test.txt', 'w', encoding='utf-8') as f:
    f.write(f"{title}\n")
    f.write('\t'.join(fields) + '\n')
    for index, row in df.iterrows():
        f.write('\t'.join(map(str, row.values)) + '\n')