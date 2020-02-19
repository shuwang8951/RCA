from RCA import Config as cf
import os
from RCA import DistrictCharacter


class ValueCount:
    def __init__(self):
        self.config = cf.Config()

    def load_count_txt(self):
        txt_folder_towns = os.listdir(self.config.texts_folder_path)

        for each_town_name in txt_folder_towns:

            each_town_file_path = os.path.join(self.config.texts_folder_path, each_town_name)

            # 实例化小镇
            dc = DistrictCharacter.District()
            dc.district_name = each_town_name

            for each_town_folder_file in os.listdir(each_town_file_path):
                # 只处理词频统计文件
                if each_town_folder_file.__contains__('_词频.txt'):
                    # 载入词频文件
                    dc.load_character_txt_file(os.path.join(each_town_file_path, each_town_folder_file))
                    print(each_town_name + '_' + each_town_folder_file + '词频文件载入成功。')

            # process 小镇特征
            dc.calculate_character_query_value()
            dc.get_char_class_query_num()

            # 特征值爬取计算
            dc.calculate_hischaracter()
            print('history 特征值计算完成')
            dc.calculate_culcharacter()
            print('culture 特征值计算完成')
            dc.calculate_tourcharacter()
            print('tour 特征值计算完成')
            dc.calculate_viewcharacter()
            print('view 特征值计算完成')

            print(dc.district_name)
            print(dc.district_query_num)
            print(dc.history_list)
            print(dc.history_list_val)
            print(dc.history_list_query_num)
            print(dc.history_list_class_queryNum)
            print(dc.history_list_toponym_value)

            print(dc.culture_list)
            print(dc.culture_list_val)
            print(dc.culture_list_query_num)
            print(dc.culture_list_class_queryNum)
            print(dc.culture_list_toponym_value)

            print(dc.tour_list)
            print(dc.tour_list_val)
            print(dc.tour_list_query_num)
            print(dc.tour_list_class_queryNum)
            print(dc.tour_list_toponym_value)

            print(dc.view_list)
            print(dc.view_list_val)
            print(dc.view_list_query_num)
            print(dc.view_list_class_queryNum)
            print(dc.view_list_toponym_value)

            # 写结果文件
            filename = './data/results/'+dc.district_name+'_results.txt'
            with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                f.write(dc.district_name)
                f.write("\n")
                f.write("地名总检索数目：")
                f.write("\n")
                f.write(str(dc.district_query_num))
                f.write("\n")
                f.write("历史特征结果：")
                f.write("\n")
                for hischar in dc.history_list:
                    f.write(hischar+'       ')
                f.write("\n")
                for hisval in dc.history_list_val:
                    f.write(str(hisval)+'       ')
                f.write("\n")
                for hisquerynum in dc.history_list_query_num:
                    f.write(str(hisquerynum)+'      ')
                f.write("\n")
                for histoponymvalue in dc.history_list_toponym_value:
                    f.write(str(histoponymvalue)+'      ')
                f.write("\n")
                f.write("文化特征结果：")
                f.write("\n")
                for culchar in dc.culture_list:
                    f.write(str(culchar)+'      ')
                f.write("\n")
                for culval in dc.culture_list_val:
                    f.write(str(culval)+'       ')
                f.write("\n")
                for culquerynum in dc.culture_list_query_num:
                    f.write(str(culquerynum)+'       ')
                f.write("\n")
                for cultoponumvalue in dc.culture_list_toponym_value:
                    f.write(str(cultoponumvalue)+'      ')
                f.write("\n")
                f.write("旅游特征结果：")
                f.write("\n")
                for tourchar in dc.tour_list:
                    f.write(str(tourchar)+'      ')
                f.write("\n")
                for tourval in dc.tour_list_val:
                    f.write(str(tourval)+'      ')
                f.write("\n")
                for tourquerynum in dc.tour_list_query_num:
                    f.write(str(tourquerynum)+'     ')
                f.write("\n")
                for tourtoponymvalue in dc.tour_list_toponym_value:
                    f.write(str(tourtoponymvalue)+'     ')
                f.write("\n")
                f.write("风景特征结果：")
                f.write("\n")
                for viewchar in dc.view_list:
                    f.write(str(viewchar)+'     ')
                f.write("\n")
                for viewval in dc.view_list_val:
                    f.write(str(viewval)+'      ')
                f.write("\n")
                for viewquerynum in dc.view_list_query_num:
                    f.write(str(viewquerynum)+'     ')
                f.write("\n")
                for viewtoponymvalue in dc.view_list_toponym_value:
                    f.write(str(viewtoponymvalue)+'     ')
                f.write("\n")
                f.write('历史类总检索量和' + str(dc.history_list_class_queryNum))
                f.write("\n")
                f.write('文化类总检索量和' + str(dc.culture_list_class_queryNum))
                f.write("\n")
                f.write('旅游类总检索量和' + str(dc.tour_list_class_queryNum))
                f.write("\n")
                f.write('风景类总检索量和'+str(dc.view_list_class_queryNum))
                f.write("\n")
