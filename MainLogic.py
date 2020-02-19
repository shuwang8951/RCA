from RCA import RegionLinks
from RCA import CrawlTXT
from RCA import CountCalculate
from RCA import Config as cf
import datetime
from RCA import ValueCalculate
import jieba
import os

starttime = datetime.datetime.now()
config = cf.Config()

# txt爬取
# rl = RegionLinks.RegionLinks()
# rl.generate_links()
# rl.crawl_innerlinks()
# ct = CrawlTXT.CrawlTxt()
# ct.crawl_text()

# 词频计算
# cc = CountCalculate.WordCount()
# cc.process_word_count(config.texts_folder_path)

# 特色计算
# jieba.load_userdict(config.JieBaCutUserDictPath)
vc = ValueCalculate.ValueCount()
vc.load_count_txt()

endtime = datetime.datetime.now()

print('*' * 30)
print("全部完成！")
print('*' * 30)
print('运行时间:   ' + str((endtime - starttime).seconds) + '秒')
