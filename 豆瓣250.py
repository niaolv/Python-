
from concurrent.futures import ThreadPoolExecutor # 引入线程池
import requests,csv,time
from lxml import etree
def get_web_source_code(start):

    url ='https://movie.douban.com/top250'
    params = {
        'start':start
    }
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url,params=params,headers = headers)
    result = response.text
    return result

def parse(web_source_code,ls):
    tree = etree.HTML(web_source_code)

    next_page = tree.xpath('//div[@class="article"]/div[@class="paginator"]/span[@class="next"]/a/text()')
    #所有电影信息：
    movies = tree.xpath('//div[@class="article"]/ol[@class="grid_view"]/li')
    for movie in movies:
        title = movie.xpath('.//div[@class="hd"]/a/span[1]/text()') # 题目
        mark = movie.xpath('.//div[@class="bd"]/div[@class="star"]/span[2]/text()')
        for i in range(len(title)):
            dit = {}
            dit['title'] = title[i]
            dit['mark']  = mark[i]
            ls.append(dit)

    return next_page

def csv_into(data_ls):
    f = open('豆瓣Top250.csv',mode = 'w',encoding='utf-8-sig',newline='')
    #  定义表头
    file_header = ['title','mark']
    # 创建DictWriter对象
    writer = csv.DictWriter(f,file_header)
    # 写入表头：
    writer.writeheader()
    for i in data_ls:
        writer.writerow(i)
    f.close()

if __name__ == '__main__':
    start_time = time.time()

    # with ThreadPoolExecutor(5) as t:
    #判断何时该停下提取数据
    # flag 判断合适停下
    Flag = True         # 判断何为尽头。
    data_list_dict = [] #存储所有数据
    start = 0
    while Flag:
        print(f'-----------正在爬取第{(start+25)/25}页------------')
        html = get_web_source_code(start=start)
        next_page = parse(web_source_code=html,ls = data_list_dict)
        if next_page == []: # 翻页判断
            Flag = False

        start+=25 # 实现翻页尽头逻辑。

    # 数据存储：
    csv_into(data_list_dict)

    end_time = time.time()
    print('------------------豆瓣Top250爬取完毕---------------')
    print(f'spider crawl running {end_time - start_time}')




