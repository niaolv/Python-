from traceback import print_tb

import requests,time
from IPython.core.release import author

from lxml import etree


# url = 'https://www.bq555.cc/finish/'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}
#
# responses = requests.get(url= url,headers = headers)
#
# print(responses.text)

def clear_every_chapter(lst):
    lst = lst[:-2]
    s = ''

    for item in lst:
        item = item.replace('\u3000\u3000','')
        s += item

    return s

def oneben(url): # 获取每一本小说的所有章节

    url = url
    response = requests.get(url=url,headers=headers)
    time.sleep(1)
    content  = response.text
    tree = etree.HTML(content)
    chapters = tree.xpath('//div[@class="listmain"]//a/text()')
    chapters.pop(10) # 清除'加载全部章节'。
    return chapters

def novel_content(url_yiben,ls):
    data_chapters = '' # 这本小说的所有章节内容

    for i,item in enumerate(ls,start=1):
        print(f'正在爬取{item}')
        url = url_yiben + str(i) + '.html'
        print(url)
        response = requests.get(url=url,headers=headers)
        response.encoding = 'utf-8'
        tree = etree.HTML(response.text)
        content = tree.xpath('//div[@id="chaptercontent"]/text()')

        # 清洗列表中的数据：
        s= clear_every_chapter(lst=content)
        print(s)
        data_chapters += item + '\n' + s + '\n'
        time.sleep(1)
    return data_chapters


def main(page):

    url = 'https://www.bq555.cc/json'

    for i in range(1,page +1,1): # 笔趣阁整个一大页：
        params = {
            'sortid': 0,
            'page': i
        }
        response = requests.get(url=url,headers=headers,params=params)
        content = response.json()
        for item in content: #每一页的20本：中的每一本处理
            url_list    = item['url_list']
            url_img     = item['url_img']
            articlename = item['articlename']
            author      = item['author']
            intro       = item['intro']

            url_yiben =  'https://www.bq555.cc' + url_list
            print(f'----------------正在爬取{articlename}------------------')
            chapters = oneben(url_yiben) # 拿到一本小说的所有的章节列表数据。
            data_chapters = novel_content( url_yiben,ls = chapters) # 提取出一本小说的所有的内容。
            s2 = ''# 专门用来储存这本小说的名字，作者，简介等
            s2 = articlename + '\n' + '作者:{}\n'.format(author) + '简介:{}\n'.format(intro)
            with open(articlename + '.txt',mode='w',encoding='utf-8') as f:
                f.write(s2 + data_chapters)
            print('---------小说{}爬取完成----------'.format(articlename))
        time.sleep(2)


if __name__ == '__main__':
    # page = 5
    # main(page)
    url = 'https://www.bq555.cc/xs/185852/'
    response = requests.get(url=url,headers=headers)
    content = response.text
    tree = etree.HTML(content)
    articlename = tree.xpath('//div[@class="info"]/h1/text()')[0]
    author = tree.xpath('//div[@class="info"]/div[@class="small"]/span[1]/text()')[0][3:]
    intro = tree.xpath('//div[@class="info"]/div[@class="intro"]//dd/text()')[0]

    chapters = oneben(url=url)
    print(chapters)
    data_chapters = novel_content(url_yiben=url,ls = chapters)
    s2 = articlename + '\n' + '作者:{}\n'.format(author) + '简介:{}\n'.format(intro)
    # with open(articlename + '.txt', mode='w', encoding='utf-8') as f:
    #     f.write(s2 + data_chapters)
    print('---------小说{}爬取完成----------'.format(articlename))




















