
import requests
import json,time

from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray


#处理日期中的/
def riqi(strings):
    ls = strings.split('/')

    return '-'.join(ls)


# 发送请求，拿到数据
def oneye(first,end,page):
    url = 'http://www.xinfadi.com.cn/getPriceData.html'
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'

    }
    params ={
        'limit': 20,
        'current': page,
        'pubDateStartTime': first,
        'pubDateEndTime': end
        }

    response = requests.post(url,data=params,params=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200 :
        try :
            response.json()
            return  response.json()
        except:
            print('非json响应内容，{}'.format(response.text))
    else:
        print(f'请求失败；状态码：{response.status_code}')


all_data_list_dict = [] # 所有数据


# 处理数据，数据清洗 ; 保存数据为dict嵌套list
def parse(url_json):
    data_json = url_json
    lists = data_json['list']
    for list in lists:
        prodName = list['prodName']
        place    = list['place']
        lowPrice = list['lowPrice']
        highPrice=list['highPrice']
        avgPrice = list['avgPrice']

        if place == '':
            place = '产地未知'

        dit ={}
        dit['proName'] = prodName
        dit['place'] = place
        dit['lowPrice'] = lowPrice
        dit['highPrice'] = highPrice
        dit['avgPrice'] = avgPrice
        all_data_list_dict.append(dit)


# 主要逻辑
if __name__ == '__main__':
    #定义我爬取的起止时间
    pubDateStartTime =  '2024/01/01'
    pubDateEndTime   =  '2024/11/01'
    # 计算我的程序执行时间。
    t1 = time.time()
    # 定义我要爬取的页数。
    for page in range(1,300+1):
        print(f'-----------正在爬取第{page}页数据------------')
        # time.sleep(0.1)
        data_json = oneye(first = pubDateEndTime,end = pubDateEndTime,page=page) # 拿到一页josn数据

        parse(data_json) # 数据的清洗和提取。

    first_time = riqi(pubDateStartTime)
    end_time = riqi(pubDateEndTime)

    file_title = f'北京新发地从{first_time}到{end_time}的蔬菜价格'
    # with open(file_title + '.json',mode='w',encoding='utf-8') as fp:
    #     json.dump(all_data_list_dict,fp=fp,ensure_ascii=False,indent = 4)

    t2 = time.time()
    print('running time {}'.format(t2 - t1))
