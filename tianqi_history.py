# 导入需要的库
import requests
from lxml import etree
import pandas as pd

# 设置城市名拼音和查询时间
city = 'guangnan'  # 城市名拼音
month = '202310'   # 查询时间

# 定义函数，用于获取指定城市和月份的天气数据的HTML页面
def get_html(city, month):
    # 设置请求头
    headers = {
        "Accept-Encoding": "Gzip",  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    }
    # 构建URL
    url = f'https://lishi.tianqi.com/{city}/{month}.html'
    
    # 发送请求并获取HTML页面
    r = requests.get(url, headers=headers)
    r_html = etree.HTML(r.text)
    
    return r_html

# 生成月份列表
month_list = pd.period_range(month, month, freq='M').strftime('%Y%m')

# 创建一个空的DataFrame，用于存放天气数据
df = pd.DataFrame(columns=['日期', '最高气温', '最低气温', '天气', '风向'])

# 遍历月份列表
for i, month in enumerate(month_list):
    # 获取HTML页面
    r_html = get_html(city, month)
    
    # 找到存放历史天气数据的div节点
    div = r_html.xpath('.//div[@class="tian_three"]')[0]
    
    # 获取每个日期的历史天气数据的li节点组成的列表
    lis = div.xpath('.//li')
    
    # 遍历每个li节点，提取天气数据
    for li in lis:
        item = {
            '日期': li.xpath('./div[@class="th200"]/text()')[0],
            '最高气温': li.xpath('./div[@class="th140"]/text()')[0],
            '最低气温': li.xpath('./div[@class="th140"]/text()')[1],
            '天气': li.xpath('./div[@class="th140"]/text()')[2],
            '风向': li.xpath('./div[@class="th140"]/text()')[3]
        }
        new_df = pd.DataFrame([item])
        df = pd.concat([df, new_df], ignore_index=True)

# 构建文件名，并将DataFrame保存为Excel文件
file_name = f'{city}_历史天气数据_{month}.xlsx'
df.to_excel(file_name, index=None)
