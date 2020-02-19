import os


class Config:
    def __init__(self):
        # root_dir = os.path.dirname(os.path.abspath('.'))  ## 获取相对目录
        root_dir = os.getcwd()  ## 获取相对目录

        # path
        self.classificationPath = os.path.join(root_dir, 'data', 'classificationmodel.xlsx')

        # texts folder path
        self.texts_folder_path = os.path.join(root_dir, 'data', 'texts')

        # list path
        self.regionListPath = os.path.join(root_dir, 'data', '福建.xlsx')

        # temp document path
        self.tempPageLinkListPath = os.path.join(root_dir, 'data', 'tempPageLinkList.xlsx')

        # all page link document path
        self.allPageLinkListPath = os.path.join(root_dir, 'data', 'allPageLinkList.xlsx')

        # max generate page number max=76
        self.maxGeneratePageNumer = 50

        # selenium re crawl number
        self.reCrawlNumber = 1

        # stop word document path-分词停用停词表
        self.StopWordDocumentPath = os.path.join(root_dir, 'data', 'stopword', '中文停用词表.txt')

        # 词频停词表-自建
        self.StopWordWordFrequencyPath = os.path.join(root_dir, 'data', '词频停词表.txt')

        # 常用省市名称——地名
        self.CommonPlaceNamePath = os.path.join(root_dir, 'data',  '常用省市名称.txt')

        # 常用地区村名称——地名
        self.CommonMinimumPlaceNamePath = os.path.join(root_dir, 'data', '地区村名.txt')

        # 常用地区村名称——地名
        self.Province = '福建'

        # jieba分词自定义词典路径
        self.JieBaCutUserDictPath = os.path.join(root_dir, 'data',  'jieba_地名.txt')

        # 地名列表路径
        self.ToponymListPath = os.path.join(root_dir, 'data', '地名列表.txt')

    def get_baidu_query_link(self, targetword, pagenumber):
        return 'https://www.baidu.com/s?wd=' + targetword + '&pn=' + str(
            10 * pagenumber) + '&op=' + targetword + '&ie=utf-8&usm=3&rsv_idx=2&rsv_page=1'
