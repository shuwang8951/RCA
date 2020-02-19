from goose3 import Goose
from goose3.text import StopWordsChinese
import requests
from fake_useragent import UserAgent
import openpyxl
from RCA import Config as cf
import os
from newspaper import Article
import gc
# from boilerpipe.extract import Extractor


class CrawlTxt:
    def __init__(self):
        self.ua = UserAgent()

        # read allpagelinkdocument
        self.regionname = []
        self.classification = []
        self.links = []

        self.config = cf.Config()
        self.read_allpagelinks(self.config.allPageLinkListPath)
        self.g=Goose({'browser_user_agent': 'Mozilla', 'stopwords_class': StopWordsChinese})

    def get_text_bygoose(self, url, re_crawlnumber):

        headers = {
            "User-Agent": self.ua.random,
            'Connection': 'close',
        }


        try:
            res = requests.get(url, headers=headers, timeout=8)
            print('提取正文...from：' + url)
            print(res.status_code)
            if res.status_code == 200:
                article = self.g.extract(url)
                content = article.cleaned_text
                if content == None and re_crawlnumber > 0:
                    # self.get_text_bygoose(url, re_crawlnumber - 1)
                    content = url
                    print('该链接内容读取超时！')


            else:
                content = url
                if re_crawlnumber > 0:
                    # self.get_text_bygoose(url, re_crawlnumber - 1)
                    content = url
                    print('该链接内容读取超时！')
        except:
            content = url
            print('该链接内容读取超时！')
            if re_crawlnumber > 0:
                # self.get_text_bygoose(url, re_crawlnumber - 1)
                pass
        return content
        del article
        del url
        del res
        del content
        gc.collect()


    def get_text_bynewspaper(self, url, re_crawlnumber):
        headers = {
            "User-Agent": self.ua.random,
            'Connection': 'close',
        }
        news = Article(url, language='zh')

        try:
            res = requests.get(url, headers=headers, timeout=8)
            print('提取正文...from：' + url)
            print(res.status_code)
            if res.status_code == 200:
                news.download()
                news.parse()
                content = news.text
                if content == None and re_crawlnumber > 0:
                    self.get_text_bynewspaper(url, re_crawlnumber - 1)
            else:
                content = url
                if re_crawlnumber > 0:
                    self.get_text_bynewspaper(url, re_crawlnumber - 1)
        except:
            content = url
            print('该链接内容读取超时！')
            if re_crawlnumber > 0:
                self.get_text_bynewspaper(url, re_crawlnumber - 1)
        return content

    '''
    def get_text_byboileerpipe(self, url, re_crawlnumber):
        headers = {
            "User-Agent": self.ua.random,
            'Connection': 'close',
        }

        try:
            extractor = Extractor(url=''.join(url))

            res = requests.get(url, headers=headers, timeout=8)
            print('提取正文...from：' + url)
            print(res.status_code)
            if res.status_code == 200:

                content = extractor.getText()

                if content == None and re_crawlnumber > 0:
                    self.get_text_byboileerpipe(url, re_crawlnumber - 1)
            else:
                content = url
                if re_crawlnumber > 0:
                    self.get_text_byboileerpipe(url, re_crawlnumber - 1)
        except:
            content = url
            print('该链接内容读取超时！')
            if re_crawlnumber > 0:
                self.get_text_byboileerpipe(url, re_crawlnumber - 1)
        return content
    '''

    def crawl_text(self):
        for eachlink in range(len(self.links)):
            if eachlink > 0:
                currentregionname = self.regionname[eachlink]
                currentclassification = self.classification[eachlink]

                regionpath = os.path.join(self.config.texts_folder_path, currentregionname)
                if not os.path.exists(regionpath):
                    os.mkdir(regionpath)
                RCpath = os.path.join(regionpath, currentclassification)
                if not os.path.exists(RCpath):
                    os.mkdir(RCpath)

                self.write_to_file(RCpath, self.links[eachlink], eachlink + 1)
                print('存储txt中...——' + RCpath)
                gc.collect()
        print('成功存储——全部TXT文本！')

    def write_to_file(self, txtpath, url, title):

        # 用goose抓网页正文
        content = self.get_text_bygoose(url, self.config.reCrawlNumber)
        # # 用newspaper抓网页正文
        # content = self.get_text_bynewspaper(url, self.config.reCrawlNumber)
        # 用boilerpip抓网页正文
        #content = self.get_text_byboileerpipe(url, self.config.reCrawlNumber)

        try:
            txt_path = os.path.join(txtpath, str(title) + '.txt')
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(content)
                f.flush()

        except:
            print(txt_path + '存储txt错误！')
        del content
        del f
        gc.collect()


    def read_allpagelinks(self, allpagelinklistPath):
        workbook_allpagelinks = openpyxl.load_workbook(allpagelinklistPath)

        sheet_allpagelinks = workbook_allpagelinks['Sheet']

        for x in range(len(sheet_allpagelinks['C'])):
            if x > 0:
                self.regionname.append(str(sheet_allpagelinks['A'][x].value))
                self.classification.append(str(sheet_allpagelinks['B'][x].value))
                self.links.append(str(sheet_allpagelinks['C'][x].value))
        print('成功读取——全部爬取链接！准备爬取全文txt...')
