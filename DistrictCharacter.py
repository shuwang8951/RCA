from RCA import Utility as ul
from fake_useragent import UserAgent
import requests
from RCA import Config
import re
import urllib
from RCA import Character
import time
import gc


class District:
    def __init__(self):
        self.cf = Config.Config()
        self.district_name = ''
        self.district_query_num = 0

        self.history_list = []
        self.history_list_val = []
        self.history_list_query_num = []
        self.history_list_class_queryNum = 0
        self.history_list_toponym_value = []

        self.culture_list = []
        self.culture_list_val = []
        self.culture_list_query_num = []
        self.culture_list_class_queryNum = 0
        self.culture_list_toponym_value = []

        self.tour_list = []
        self.tour_list_val = []
        self.tour_list_query_num = []
        self.tour_list_class_queryNum = 0
        self.tour_list_toponym_value = []

        self.view_list = []
        self.view_list_val = []
        self.view_list_query_num = []
        self.view_list_class_queryNum = 0
        self.view_list_toponym_value = []

        self.ua = UserAgent()

    def load_character_txt_file(self, txtfilepath):
        readlist = ul.Utility.read_txt_to_list(txtfilepath)

        if txtfilepath.__contains__('历史'):
            self.history_list = self.read_character_in_list(readlist, 'word')
            self.history_list_val = self.read_character_in_list(readlist, 'value')
        elif txtfilepath.__contains__('文化'):
            self.culture_list = self.read_character_in_list(readlist, 'word')
            self.culture_list_val = self.read_character_in_list(readlist, 'value')
        elif txtfilepath.__contains__('旅游'):
            self.tour_list = self.read_character_in_list(readlist, 'word')
            self.tour_list_val = self.read_character_in_list(readlist, 'value')
        elif txtfilepath.__contains__('风景'):
            self.view_list = self.read_character_in_list(readlist, 'word')
            self.view_list_val = self.read_character_in_list(readlist, 'value')

    def read_character_in_list(self, readlist, word_or_value):
        templist = []
        if word_or_value == 'word':
            index = 0
        else:
            index = 1
        if readlist:
            for character_item in readlist:
                templist.append(character_item.split(' ')[index])
        return templist

    def calculate_character_query_value(self):
        self.district_query_num = self.get_queryNum('', self.district_name, self.cf.Province)

        if self.history_list:
            for historychar in self.history_list:
                self.history_list_query_num.append(self.get_queryNum(historychar, self.district_name, self.cf.Province))

        if self.culture_list:
            for culturechar in self.culture_list:
                self.culture_list_query_num.append(self.get_queryNum(culturechar, self.district_name, self.cf.Province))

        if self.tour_list:
            for tourchar in self.tour_list:
                self.tour_list_query_num.append(self.get_queryNum(tourchar, self.district_name, self.cf.Province))

        if self.view_list:
            for viewchar in self.view_list:
                self.view_list_query_num.append(self.get_queryNum(viewchar, self.district_name, self.cf.Province))

    def get_queryNum(self, word, district, province):
        querynum = 0
        headers = {
            "User-Agent": self.ua.random,
            'Connection': 'close',
        }
        temp_word = "\"" + province + " " + district + " " + word + "\""

        url = Config.Config.get_baidu_query_link(self, urllib.parse.quote(temp_word), 10)
        try:
            res = requests.get(url, headers=headers, timeout=8)
            # print(res.status_code)
            if res.status_code == 200:
                querynum = self.get_queryNum_from_request(res)

                # 防止网络错误，重爬一遍
                if querynum == 0:
                    res = requests.get(url, headers=headers, timeout=8)
                    querynum = self.get_queryNum_from_request(res)

        except:
            print('未获取' + temp_word + '网页信息！')
        return querynum

    def get_queryNum_from_request(self, request):
        number = 0
        try:
            pattern = '''<span class="nums_text">百度为您找到相关结果约(.*?)个</span>'''
            results = re.compile(pattern).findall(request.text)
            if results:
                number = int(results[0].replace(',', ''))
        except:
            print('request 存在问题。')
        return number

    def get_char_class_query_num(self):
        if self.history_list_query_num:
            for hisnum in self.history_list_query_num:
                self.history_list_class_queryNum = self.history_list_class_queryNum + int(hisnum)
        if self.culture_list_query_num:
            for culnum in self.culture_list_query_num:
                self.culture_list_class_queryNum = self.culture_list_class_queryNum + int(culnum)
        if self.tour_list_query_num:
            for tounum in self.tour_list_query_num:
                self.tour_list_class_queryNum = self.tour_list_class_queryNum + int(tounum)
        if self.view_list_query_num:
            for vienum in self.view_list_query_num:
                self.view_list_class_queryNum = self.view_list_class_queryNum + int(vienum)

    def calculate_hischaracter(self):
        if self.history_list:
            i = 0
            for str_character in self.history_list:
                c = Character.Character()
                c.character_name = str_character
                c.character_belonged_district = self.district_name
                c.character_word_frequency = self.history_list_val[i]
                c.character_query_number = self.history_list_query_num[i]
                c.generate_character_links()
                c.generate_crawler_links()
                c.crawl_txt_to_tf_list()
                c.search_toponym_in_tf_list()
                c.calculate_char_value()
                self.history_list_toponym_value.append(c.character_in_province_value)
                # print(self.history_list_toponym_value)
                i = i + 1
                del c
                gc.collect()

    def calculate_culcharacter(self):
        if self.culture_list:
            i = 0
            for str_character in self.culture_list:
                c = Character.Character()
                c.character_name = str_character
                c.character_belonged_district = self.district_name
                c.character_word_frequency = self.culture_list_val[i]
                c.character_query_number = self.culture_list_query_num[i]
                c.generate_character_links()
                c.generate_crawler_links()
                c.crawl_txt_to_tf_list()
                c.search_toponym_in_tf_list()
                c.calculate_char_value()
                self.culture_list_toponym_value.append(c.character_in_province_value)
                # print(self.history_list_toponym_value)
                i = i + 1
                del c
                gc.collect()

    def calculate_tourcharacter(self):
        if self.tour_list:
            i = 0
            for str_character in self.tour_list:
                c = Character.Character()
                c.character_name = str_character
                c.character_belonged_district = self.district_name
                c.character_word_frequency = self.tour_list_val[i]
                c.character_query_number = self.tour_list_query_num[i]
                c.generate_character_links()
                c.generate_crawler_links()
                c.crawl_txt_to_tf_list()
                c.search_toponym_in_tf_list()
                c.calculate_char_value()
                self.tour_list_toponym_value.append(c.character_in_province_value)
                # print(self.history_list_toponym_value)
                i = i + 1
                del c
                gc.collect()

    def calculate_viewcharacter(self):
        if self.view_list:
            i = 0
            for str_character in self.view_list:
                c = Character.Character()
                c.character_name = str_character
                c.character_belonged_district = self.district_name
                c.character_word_frequency = self.view_list_val[i]
                c.character_query_number = self.view_list_query_num[i]
                c.generate_character_links()
                c.generate_crawler_links()
                c.crawl_txt_to_tf_list()
                c.search_toponym_in_tf_list()
                c.calculate_char_value()
                self.view_list_toponym_value.append(c.character_in_province_value)
                # print(self.history_list_toponym_value)
                i = i + 1
                del c
                gc.collect()
