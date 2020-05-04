import json
import os

import requests
import bs4

class GetHzw:

    def __init__(self):
        pass

    def mk_dir(self,name):
        try:
            os.mkdir(str(name))
        except Exception as e:
            print(e)

    def request_hzw(self):
        begin_chapter = 915
        for_level = 1
        self.mk_dir(begin_chapter)
        while 1:
            for i in range(0,50):
                url = "https://www.fzdm.com/manhua/2//" + str(begin_chapter) + "/index_" + str(i) + ".html"
                print(url)
                resp = requests.get(url)
                if resp.status_code == 200:
                    try:
                        resp_content = resp.content
                        soup = bs4.BeautifulSoup(resp_content, 'lxml')
                        title = soup.select('#pjax-container > h1')[0].text
                        aaa = soup.select("body > script:nth-child(9)")
                        a2 = str(aaa[0]).split(";")[2].split('"')[1]
                        pic_url = "http://p17.manhuapan.com/" + a2
                        print(title, pic_url)
                        pic_resp = requests.get(pic_url).content
                    except Exception as e:
                        print(e)
                        i -=  1
                        continue

                    try:
                        with open("./"+str(begin_chapter)+"/"+title + ".jpg", 'wb') as f:
                            f.write(pic_resp)
                    except IOError as e:
                        print(e)
                    check_next = soup.select("#pjax-container > div.navigation")
                    if "最后一页了" in str(check_next[0]):
                        print("已看到当前章节最后一页")
                        begin_chapter += 1
                        print(begin_chapter)
                        self.mk_dir(begin_chapter)
                        break
                else:
                    print("已是最新章节")
                    for_level = 2
                    break
            if for_level == 2:
              break



if __name__ == "__main__":
    GetHzw().request_hzw()