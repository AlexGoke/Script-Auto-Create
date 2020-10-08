
# 自动根据excel更改脚本文件名

import os
from openpyxl import Workbook
from openpyxl import load_workbook


def file_name_listdir(file_dir: str) -> list:
    file_name_list = []
    for file in os.listdir(file_dir):
        if file[0] == 'b':
            file_name_list.append(file)
    return file_name_list


# file_path = "D:\\Sugon_Work\\test\\esat\\scripts\\system_test\\basic_io\\raid\\raid0"
# file_path = "D:\\Sugon_Work\\test\\esat\\scripts\\system_test\\basic_io\\raid\\raid1_rename"
# file_path = "D:\\Sugon_Work\\test\\esat\\scripts\\system_test\\basic_io\\interface_medium\\sas_hdd_rename"
# file_path = "D:\\Sugon_Work\\test\\esat\\scripts\\system_test\\basic_io\\parallel_io_rename"
# file_path = "D:\\Sugon_Work\\test\\esat\\scripts\\system_test\\basic_io\\raid\\raid_jbod_rename"
file_path = "D:\\Sugon_Work\\test\\esat\\scripts\\system_test\\basic_io\\jbod\\jbod_x2_rename"


wait_to_rename_list = file_name_listdir(file_path)
print("该文件夹下待修改文件名的数量为：%d" % len(wait_to_rename_list))

wb = load_workbook('./模拟平台调试测试用例_基础IO_20201001.xlsx', read_only=True)
# ws = wb.get_sheet_by_name('基础IO')
ws = wb['基础IO']

# 行号范围
excel_script_name_list = []
# for case_row_index in range(16, 82):    # raid0
# for case_row_index in range(82, 148):    # raid1
# for case_row_index in range(148, 214):    # raid5
# for case_row_index in range(214, 334):    # sas_hdd
# for case_row_index in range(334, 388):    # raid_jbod
# for case_row_index in range(388, 406):    # parallel_io
for case_row_index in range(407, 431):    # jbod
    script_name = ws['B' + str(case_row_index)].value
    excel_script_name_list.append(script_name)
# print(excel_script_name_list)
print("excel中相对应的文件名数量为：%d" % len(excel_script_name_list))
# os.rename("case_script", cls.script_name + '.py')    # 格式化

# rename
if len(excel_script_name_list) == len(wait_to_rename_list):
    for i in range(len(excel_script_name_list)):
        print(wait_to_rename_list[i][0:20])
        print(excel_script_name_list[i])
        if wait_to_rename_list[i][0:20] in excel_script_name_list[i] and os.path.exists(file_path+"\\"+wait_to_rename_list[i]):
            os.chdir(file_path)
            # os.rename(
            #     file_path+"\\"+wait_to_rename_list[i], file_path+"\\"+excel_script_name_list[i])    # rename
            #os.rename(os.path.join(file_path, wait_to_rename_list[i]), os.path.join(file_path, excel_script_name_list[i]))
            old_name = wait_to_rename_list[i]
            new_name = excel_script_name_list[i]
            os.renames(os.path.join(file_path, old_name),
                       os.path.join(file_path, new_name))
