'''
实现一个爬虫程序，抓取小说内容
'''
import requests
# bs4 -> BeautifulSoup4
import bs4
import re
import time

#1. 先构造一个HTTP请求，把这个请求发送出去获取到响应
# 可以打开各种各样的页面
def open_page(url):
    response = requests.get(url)
    #手动将程序解析的编码方式设定为gbk
    response.encoding = 'gbk'
    #status_code 状态码
    if response.status_code != 200:
        print(f"requests get {url} failed! {response}")
        return ''
    return response.text
# def test1():
#     print(open_page('https://www.booktxt.net/1_1486/'))

#2. 根据内容来进行解析
# 解析出每个章节的url(a 标签中解析)
def parse_man_page(html):
    #a.创建一个soup对象
    soup = bs4.BeautifulSoup(html,"html.parser")
    #b.找到所有href属性由6个连续的数字构成的url
    charts = soup.find_all(href=re.compile(r'\d{6}.html'))
    #c.根据上一步的结果生成所有章节的url的列表  遍历上面列表的每一个属性，取href
    url_list = ['https://www.booktxt.net/1_1486/' + item['href'] for item in charts]
    return url_list
# def test2():
#     html = open_page('https://www.booktxt.net/1_1486/')
#     print(parse_man_page(html))

# test2()
# def test3():
#     #验证一下使用open_page 来打开小说详情页内容
#     print(open_page('https://www.booktxt.net/1_1486/491996.html'))

#3.解析每个网址的详情页
def parse_detail_page(html):
    '''解析出当前章节的标题和正文'''
    soup = bs4.BeautifulSoup(html,'html.parser')
    #按照属性查找文章名称
    title = soup.find_all(class_='bookname')[0].h1.get_text()
    content = soup.find_all(id='content')[0].get_text()
    return title,content

# def test4():
# #     html = open_page('https://www.booktxt.net/1_1486/491996.html')
# #     title,content = parse_detail_page(html)
# #     print('title:', title)
# #     print('content:',content)

# test4()

#写进文件
def write_file(title,content):
    with open('tmp.txt','a',encoding='gbk', errors='ignore') as f:
        f.write(title + '\n' + content + '\n\n\n')


def run():
    url = 'https://www.booktxt.net/1_1486'
    #1.打开入口页面，并分析出其中的所有详情页的url
    html = open_page(url)
    url_list = parse_man_page(html)
    #2.遍历详情页的url，依次分析每个详细内容页
    for url in url_list:
        print("crawler url:",url)
        detail_html = open_page(url)
        title,content = parse_detail_page(detail_html)
        write_file(title,content)
        time.sleep(5)
    print('crawler done!')

run()