import requests,csv,time
from lxml import etree
from threading import Thread
from queue import Queue

def get_all_urls(url_queue):
    for i in range(0,226,25):
        url = f'https://movie.douban.com/top250?start={i}'
        url_queue.put(url)

def csv_into(data_ls):
    f = open('豆瓣Top250多线程.csv',mode = 'w',encoding='utf-8-sig',newline='')
    #  定义表头
    file_header = ['title','mark']
    # 创建DictWriter对象
    writer = csv.DictWriter(f,file_header)
    # 写入表头：
    writer.writeheader()
    for i in data_ls:
        writer.writerow(i)
    f.close()


def spider(ls):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }
    while not url_queue.empty():
        url = url_queue.get()
        print(url)
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            print('请求成功！')
        result = response.text
        time.sleep(3)
        tree = etree.HTML(result)

        # next_page = tree.xpath('//div[@class="article"]/div[@class="paginator"]/span[@class="next"]/a/text()')
        #所有电影信息：
        movies = tree.xpath('//div[@class="article"]/ol[@class="grid_view"]/li')
        for movie in movies:
            title = movie.xpath('.//div[@class="hd"]/a/span[1]/text()') # 题目
            mark = movie.xpath('.//div[@class="bd"]/div[@class="star"]/span[2]/text()')
            for i in range(len(title)):
                dit = {}
                dit['title'] = title[i]
                dit['mark']  = mark[i]
                print(dit)
                ls.append(dit)

    url_queue.task_done() # 标记任务已经完成

if __name__ == '__main__':
    # 计算程序执行的时间
    start_time = time.time()
    data_list_dict = []  # 存储所有数据
    # 创建队列：
    url_queue = Queue()
    get_all_urls(url_queue = url_queue) # 生成urls队列
    print(url_queue)

    # 等待线程列表：
    wait_ls = []
    for i in range(5): # 启用5个线程
        thread = Thread(target=spider,args=(data_list_dict,))
        thread.start()
        wait_ls.append(thread)

    # 等待所有线程执行完毕：
    for thread in wait_ls:
        thread.join()
    print(data_list_dict)
    csv_into(data_list_dict)
    end_time = time.time()
    print('spider crawling {0}'.format(end_time - start_time))
    
    # 仅仅9秒