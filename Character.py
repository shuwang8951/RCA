from RCA import Config
from RCA import Utility
import urllib
import requests
from fake_useragent import UserAgent
import jieba.posseg as psg
import jieba
from goose3 import Goose
from goose3.text import StopWordsChinese
import re
from collections import Counter
import gc
from RCA import Utility as ul


class Character:
    def __init__(self):
        self.cf = Config.Config()

        self.ul = Utility.Utility()

        self.character_name = ''

        self.character_belonged_district = ''

        self.character_word_frequency = 0

        self.character_query_number = 0

        self.character_generate_links = []

        self.character_crawler_links = []

        self.character_tf_list = {}

        self.character_in_province_position = 200

        self.character_in_province_value = 0

        self.g = Goose({'browser_user_agent': 'Mozilla', 'stopwords_class': StopWordsChinese})

        self.district_names = ul.Utility.read_txt_to_list(self.cf.ToponymListPath)

    def generate_character_links(self):
        if self.character_name != '':
            temp_word = "\"" + self.cf.Province + " " + self.character_name + "\""
            for page in range(4):
                query_link = self.cf.get_baidu_query_link(urllib.parse.quote(temp_word), page)
                self.character_generate_links.append(query_link)
        else:
            print('存在错误，未获得特征名称！')

    def generate_crawler_links(self):
        if self.character_generate_links:
            for pagelink in self.character_generate_links:
                cr_links = self.ul.get_links(pagelink, self.cf.reCrawlNumber)
                # 存储于待爬linklist
                self.character_crawler_links = self.character_crawler_links + cr_links

    def crawl_txt_to_tf_list(self):
        if self.character_crawler_links:
            i = 0
            wordslist = []
            for eachlinkurl in self.character_crawler_links:
                i = i + 1
                # print('process...... ' + str(i) + ' in ' + str(len(self.character_crawler_links)))
                content_temp = self.get_text_bygoose(eachlinkurl, self.cf.reCrawlNumber)
                wordslist = wordslist + self.word_segment(content_temp)

            tf_count = Counter(wordslist)
            self.character_tf_list = tf_count.most_common(200)

            for tf_word in self.character_tf_list:
                print(tf_word)
            del wordslist
            gc.collect()

    def search_toponym_in_tf_list(self):

        if self.character_tf_list:
            i = 0
            position_int_1 = 200
            position_int_2 = 200
            for key, val in self.character_tf_list:
                i = i + 1
                if key == self.character_belonged_district:
                    position_int_1 = i
                if key == self.character_belonged_district.replace('镇', '').replace('乡', '').replace('街道', ''):
                    position_int_2 = i
            if position_int_1 == 0 and position_int_2 == 0:
                position = 0
            else:
                if position_int_1 > position_int_2:
                    position = position_int_2
                else:
                    position = position_int_1
        print(self.character_name + '在位置：' + str(position))
        self.character_in_province_position = position

    def calculate_char_value(self):
        self.character_in_province_value = (200 - self.character_in_province_position) / 2

    def word_segment(self, str):
        returnwordlist = []
        line_cut = re.sub('[a-zA-Z0-9’!"#$%&\'()*+,-—./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "",
                          str)
        line_cut = re.sub(
            '[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+',
            '', line_cut)

        cut_words = list(jieba.cut(line_cut, cut_all=True))

        for word in cut_words:
            if self.get_placenames(word, self.district_names) != '':
                returnwordlist.append(word)

        #cut_words = [(x.word, x.flag) for x in psg.cut(line_cut) if len(line_cut) > 2]

        # 词频限定
        # returnwordlist = [x[0] for x in cut_words
        #                   # 过滤单个汉字
        #                   if len(x[0]) > 1
        #
        #                   # 只存储地名类别
        #                   # and x[1].startswith('ns')
        #
        #
        #                   and self.get_placenames(x[0], self.district_names) != ''
        #                   ]

        print(returnwordlist)
        return returnwordlist

    def get_text_bygoose(self, url, re_crawlnumber):
        ua = UserAgent()
        headers = {
            "User-Agent": ua.random,
            'Connection': 'close',
        }
        try:
            res = requests.get(url, headers=headers, timeout=8)
            # print('提取正文...from：' + url)
            # print(res.status_code)
            if res.status_code == 200:
                article = self.g.extract(url)
                content = article.cleaned_text
                if content == None and re_crawlnumber > 0:
                    # self.get_text_bygoose(url, re_crawlnumber - 1)
                    content = url
                    print('该链接内容读取超时！_____1')
            else:
                content = url
                if re_crawlnumber > 0:
                    # self.get_text_bygoose(url, re_crawlnumber - 1)
                    content = url
                    print('该链接内容读取超时！_重爬')
        except:
            content = url
            print('该链接内容读取超时！____except')
            if re_crawlnumber > 0:
                # self.get_text_bygoose(url, re_crawlnumber - 1)
                pass
        return content
        del article
        del url
        del res
        del content
        gc.collect()

    def get_placenames(self, word, placenamelist):
        temp_return_word = ''
        if placenamelist:
            if word in placenamelist:
                # 在地名中
                temp_return_word = word
            else:
                pass
        else:
            print('需要载入常用省市名称词表！')

        return temp_return_word
