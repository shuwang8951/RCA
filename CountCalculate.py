from RCA import Config as cf
import os
import re
from collections import Counter
import jieba.posseg as psg
import jieba
import jieba.analyse
import gc
from RCA import Utility as ul


class WordCount:
    def __init__(self):
        self.config = cf.Config()

        # 载入分词停词表
        self.stopwords = ul.Utility.read_txt_to_list(self.config.StopWordDocumentPath)

        # 载入自定义词频停词表
        self.StopWord_WordFrequency = ul.Utility.read_txt_to_list(self.config.StopWordWordFrequencyPath)

        # 载入常用地名词表，常用省市名称
        self.Common_PlaceName = ul.Utility.read_txt_to_list(self.config.CommonPlaceNamePath)

        # 载入常用村名词表，常用村名称
        self.Common_MiniPlaceName = ul.Utility.read_txt_to_list(self.config.CommonMinimumPlaceNamePath)

    def get_tf_lists(self, input_folder_path, output_folder_path):

        # 遍历文件夹中的所有文件夹，并读取其中文本
        # input_folder_path   XXX镇

        txt_folder_names = os.listdir(input_folder_path)

        for txt_folder in txt_folder_names:

            tf_txt_lists = []  # store the vocabulary

            txt_folder_path = os.path.join(input_folder_path, txt_folder)

            if txt_folder_path.__contains__('.txt'):
                pass
            else:
                print('正在读取' + txt_folder + '文件夹......')
                # txt_files = os.listdir(txt_folder_path)

                unrepetitivefiles = self.delete_repetitive_files(txt_folder_path)

                for txt_file in unrepetitivefiles:
                    txt_path = os.path.join(txt_folder_path, txt_file)

                    txt_f = open(txt_path, encoding='utf-8')
                    # print(os.path.getsize(txt_path))

                    lines = txt_f.readlines()

                    for line in lines:
                        line_cut = re.sub('[a-zA-Z0-9’!"#$%&\'()*+,-—./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "",
                                          line)
                        line_cut = re.sub(
                            '[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+',
                            '', line_cut)

                        cut_words = [(x.word, x.flag) for x in psg.cut(line_cut) if len(line_cut) > 2]

                        # print(cut_words)

                        # 词频限定
                        tf_words = [x[0] for x in cut_words
                                    #   名词
                                    if x[1].startswith('n')
                                    #   去除人名
                                    and x[1] != 'nr'
                                    #   去除分词机构名
                                    and x[1] != 'nt'
                                    #   去除政府公文词汇
                                    and ul.Utility.delete_gov(x[0]) != ''
                                    #   去除行政区划名称
                                    and ul.Utility.delete_district(x[0]) != ''
                                    #   去除常见地名
                                    and ul.Utility.delete_common_placename(x[0], self.Common_PlaceName) != ''
                                    #   去除本地地名
                                    and x[0] not in input_folder_path

                                    ]

                        # print(tf_words)

                        for word in tf_words:
                            if word in self.stopwords:
                                tf_words.remove(word)

                        tf_txt_lists.extend(tf_words)

                tf_count = Counter(tf_txt_lists)

                tf_outpath = os.path.join(output_folder_path, txt_folder + '_词频.txt')

                tf_recode_txt = open(tf_outpath, 'w+', encoding='utf-8')

                firstchar_value = 0
                writechar_num = 0
                for key, val in tf_count.most_common(50):

                    #   过滤自定义词表！！！！！！！！！！！！！！！！！！！
                    #   去除村名
                    #   注意——key是词频词汇，val是词频值
                    if self.filter_stop_word(key) != '' and ul.Utility.delete_usual(
                            key) != '' and ul.Utility.delete_common_placename(key, self.Common_MiniPlaceName) != '':
                        if firstchar_value == 0:
                            firstchar_value = val
                            tf_recode_txt.write(key + ' ' + str(val) + '\n')
                            print('length tf_txt_lists:' + str(len(tf_txt_lists)))
                            print('key= ' + key + ' value= ' + str(val))
                            writechar_num = writechar_num + 1
                        else:
                            # 写入特色词频> 首个特色词频七分之一，的特色  ！！！！！！！！！！！！！！！并且少于10个
                            if val >= 10 and val >= (firstchar_value / 7) and writechar_num < 10:
                                tf_recode_txt.write(key + ' ' + str(val) + '\n')
                                print('length tf_txt_lists:' + str(len(tf_txt_lists)))
                                print('key= ' + key + ' value= ' + str(val))
                                writechar_num = writechar_num + 1

                # tf_recode_txt.write('length tf_txt_lists:' + str(len(tf_txt_lists)))
                print(tf_outpath + '文件存储完成！')

                txt_f.close()
                del txt_f
                gc.collect()
            del tf_txt_lists
            gc.collect()

    # def get_idf_lists(self, input_folder_path, output_folder_path):
    #
    #     txt_folder_names = os.listdir(input_folder_path)
    #
    #     for txt_folder in txt_folder_names:
    #
    #         idf_txt_lists = []  # store the vocabulary
    #
    #         txt_folder_path = os.path.join(input_folder_path, txt_folder)
    #
    #         if txt_folder_path.__contains__('.txt'):
    #             pass
    #         else:
    #             txt_files = os.listdir(txt_folder_path)
    #
    #             for txt_file in txt_files:
    #
    #                 txt_path = os.path.join(txt_folder_path, txt_file)
    #
    #                 txt_f = open(txt_path, encoding='utf-8')
    #
    #                 lines = txt_f.readlines()
    #
    #                 idf_contents = []  # store the text of calculating idf
    #
    #                 for line in lines:
    #                     line_cut = re.sub('[a-zA-Z0-9’!"#$%&\'()*+,-—./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~\s]+', "",
    #                                       line)
    #                     line_cut = re.sub(
    #                         '[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+',
    #                         '', line_cut)
    #
    #                     if line_cut != None:
    #                         idf_contents.append(line_cut)
    #
    #                 idf_sentences = ''.join(idf_contents)
    #                 # print(len(idf_sentences))
    #
    #                 if len(idf_sentences) != 0:
    #                     # print(idf_sentences)
    #
    #                     idf_words = jieba.analyse.extract_tags(idf_sentences, topK=100, withWeight=True)
    #
    #                     # print(idf_words)
    #
    #                     for word in idf_words:
    #                         if word[0] in self.stopwords:
    #                             idf_words.remove(word)
    #
    #                     idf_txt_lists.extend(idf_words)
    #
    #             tf_count = Counter(idf_txt_lists)
    #
    #             # print(tf_count)
    #
    #             tf_outpath = os.path.join(output_folder_path, txt_folder + '_词频.txt')
    #
    #             tf_recode_txt = open(tf_outpath, 'w+', encoding='utf-8')
    #
    #             for key, val in tf_count.most_common(100):
    #                 tf_recode_txt.write(key[0] + '  ' + str(key[1]) + ' ' + str(val) + '\n')

    def process_word_count(self, txt_folder_path):

        txt_folder_towns = os.listdir(txt_folder_path)

        if txt_folder_path.__contains__('.txt'):
            pass
        else:
            for town_folder in txt_folder_towns:
                self.get_tf_lists(os.path.join(txt_folder_path, town_folder),
                                  os.path.join(txt_folder_path, town_folder))

    def delete_repetitive_files(self, folder_path):

        unrepetitivelist = []
        temptxt = set()
        if folder_path.__contains__('.txt'):
            print('contains .txt')
        else:
            txt_files = os.listdir(folder_path)

            for txt_file in txt_files:
                txt_path = os.path.join(folder_path, txt_file)

                txt_f = open(txt_path, encoding='utf-8')

                size = len(temptxt)
                txt = txt_f.read()
                temptxt.add(txt)
                if (len(temptxt) > size):
                    unrepetitivelist.append(txt_file)

            # print('不重复文本为' + str(len(unrepetitivelist)))
            del txt_file
            del txt_files
            del size
        del temptxt
        gc.collect()
        return unrepetitivelist

    def filter_stop_word(self, word):
        if word not in self.StopWord_WordFrequency and len(word) > 1:
            return word
        else:
            return ''
