# _*_ coding:utf-8 _*_

"""
    功能：获取猫眼电影的top100排行榜
    版本：v1.0
    日期：2019.6.6
    作者：loki
"""

import requests
from multiprocessing import Pool
import re
from requests.exceptions import RequestException
import json

def get_one_page(url):
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/73.0.3683.103 Safari /537.36'
    }
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None

def parse_one_html(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?"fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:] if len(item[3]) > 3 else None,
            'releasetime':item[4].strip()[5:] if len(item[4]) > 5 else None,
            'score':item[5] + item[6]
        }

def write_to_file(file):
    file_path = 'movie.text'
    with open(file_path,'a',encoding='utf-8') as fp:
        fp.write(json.dumps(file,ensure_ascii=False) + '\n')

def main(offset):
    domain_url = 'http://maoyan.com/board/4?offset=' + str(offset)
    content = get_one_page(domain_url)

    for item in parse_one_html(content):
        print(item)
        write_to_file(item)


GroupStart = 0
GroupEnd = 10

if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        # time.sleep(1)
    # main(0)
    # pool = Pool()
    # groups = ([ x * 10 for x in range(GroupStart,GroupEnd+1)])
    # pool.map(main,groups)
    # pool.close()
    # pool.join()
