import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Weibo:
    def __init__(self):
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "Cookie": "SUB=_2AkMWiYz2f8NxqwJRmf8QxWLjb4xxzA3EieKg1X0tJRMxHRl-yT8XqmsstRB6PQmiGUAXiADtwpUFhj7eE1z9Gqdz5yra; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhC3BeSqJ6e1rEu5xiVZizj; _s_tentry=passport.weibo.com; Apache=9780790028659.691.1641350084099; SINAGLOBAL=9780790028659.691.1641350084099; ULV=1641350084104:1:1:1:9780790028659.691.1641350084099:"
    }
        self.url = "https://s.weibo.com/top/summary"
        self.hot_list = []

    def get_html_data(self):
        res = requests.get(self.url, headers=self.headers).text
        return res

    def deal_html_data(self, res):
        self.hot_list = []
        res = BeautifulSoup(res, "lxml")
        # 遍历热搜的标签
        # #pl_top_realtimehot 根据id, > table > tbody > tr 逐层查找

        # 提取热搜网址
        website = []
        for a in res.find_all('a', href=True):
            if ("&Refer=top" in a['href'] or "java" in a['href']) and "&bottomnav=1" not in a['href']:
                website.append(a['href'])
        print(website)
        print(len(website))
        i = 0
        for item in res.select("#pl_top_realtimehot > table > tbody > tr"):
            # print(item)
            # 按类名.td-01提取热搜排名
            _rank = item.select_one('.td-01').text
            if not _rank:
                continue
            # 按类名.td-02提取热搜关键词
            keyword = item.select_one(".td-02 > a").text

            # 提取热搜热度
            heat = item.select_one(".td-02 > span").text

            # 提取热搜标签
            icon = item.select_one(".td-03").text
            self.hot_list.append({"rank": _rank, "keyword": keyword, "heat": heat, "icon": icon, "time":
                                  datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "website": website[i]})
            i += 1
        return self.hot_list

    def txt_data(self, tmp):
        tmp_s = str(tmp)
        rank_f = re.compile("'rank': '(.*?)'")
        keyword_f = re.compile("'keyword': '(.*?)'")
        heat_f = re.compile("'heat': '(.*?)'")
        time_f = re.compile("'time': '(.*?)'")
        website_f = re.compile("'website': '(.*?)'")
        rank = re.findall(rank_f, tmp_s)
        keyword = re.findall(keyword_f, tmp_s)
        heat = re.findall(heat_f, tmp_s)
        time = re.findall(time_f, tmp_s)
        website = re.findall(website_f, tmp_s)
        print(len(rank))
        print(len(keyword))
        print(len(heat))
        print(len(website))
        if len(website) != len(rank):
            raise RuntimeError('testError')
        lujing = './Weibo/' + time[0][0:7] + '.md'
        readbook = ''
        with open(lujing, 'r', encoding="utf-8") as lines:
            for line in lines:
                readbook += line.strip()
        print(readbook)
        with open(lujing, 'a', encoding="utf-8") as outlines:
            outlines.write("更新时间：" + time[0] + '    \n')
            for i in range(len(rank)):
                if keyword[i] not in readbook:
                    if "java" not in website[i]:
                        if len(heat[i].strip()):
                            outlines.write('<' + rank[i] + '>' + '[' + keyword[i] + '](https://s.weibo.com' + website[i] + ')[' + heat[i].strip() + ']' + '\n')
                        else:
                            outlines.write('<' + rank[i] + '>' + '[' + keyword[i] + '](https://s.weibo.com' + website[i] + ')' + '\n')
                    else:
                        if len(heat[i].strip()):
                            outlines.write('<' + rank[i] + '>' + keyword[i] + '[' + heat[i].strip() + ']' + '\n')
                        else:
                            outlines.write('<' + rank[i] + '>' + keyword[i] + '\n')
            outlines.write("\n")
    def run(self):
        res = self.get_html_data()
        tmp = self.deal_html_data(res)
        self.txt_data(tmp)


if __name__ == '__main__':
    weibo = Weibo()
    flag = True
    weibo.run()
    flag = False
