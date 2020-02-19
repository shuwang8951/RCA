from RCA import Config as cf
from RCA import Utility as ul
import urllib
import gc


class RegionLinks:
    def __init__(self):
        self.config = cf.Config()

        self.region_list = []
        self.belong_province = ''

        self.classification_word_list = []

        self.expected_crawling_links = []
        pass

    def generate_links(self):
        # 读取小镇列表和所属省份
        region_list = ul.Utility.get_col_list(self.config.regionListPath, 'Sheet1', 'G')
        belong_province = ul.Utility.get_province(self.config.regionListPath, 'Sheet1')
        '''
        for i in range(len(region_list)):
            print(region_list[i])
        print('--所属省份：' + belong_province)
        '''
        print('成功读取——小镇列表&所属省份！')
        self.region_list = region_list
        self.belong_province = belong_province

        # 读取分类体系词汇
        classification_list = ul.Utility.get_classification_list(self.config.classificationPath)
        print('成功读取——分类体系词汇！')
        self.classification_word_list = classification_list

        # 依照小镇列表生成小镇待爬链接
        maxpagenum = self.config.maxGeneratePageNumer
        expected_crawl_links = []
        for region_num in range(len(region_list)):
            # get every region
            region_name = region_list[region_num]
            for classname in range(len(self.classification_word_list)):
                for page in range(0, maxpagenum):
                    # get every page
                    temp_word = "\"" + self.belong_province + " " + region_name + " " + self.classification_word_list[
                        classname] + "\""
                    query_link = self.config.get_baidu_query_link(urllib.parse.quote(temp_word), page)
                    expected_crawl_links.append(
                        region_name + '$$$' + self.classification_word_list[classname] + '$$$' + query_link)
                del page
                gc.collect()
            del classname
            gc.collect()
        del region_num
        gc.collect()

        print('成功构建——待爬链接！')
        self.expected_crawling_links = expected_crawl_links

        ul.Utility.write_temp_pagelinklist(expected_crawl_links, self.config.tempPageLinkListPath)
        print('成功存储——待爬链接！')


    def crawl_innerlinks(self):

        ul.Utility.write_temp_allpagelinklist(self, self.expected_crawling_links, self.config.allPageLinkListPath)
        print('成功存储——全部爬取链接！')



