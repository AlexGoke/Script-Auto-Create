
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


# 获取待rename文件
file_path = "D:\\Sugon_Work\\test\\esat\\scripts\\system_test\\basic_io\\parallel_io\\diff_dg\\raid_raid"

wait_to_rename_list = file_name_listdir(file_path)
print(wait_to_rename_list)
print("该文件夹下待修改文件名的数量为：%d" % len(wait_to_rename_list))

wb = load_workbook('./模拟平台联调测试用例_生成用_1008.xlsx', read_only=True)
# ws = wb.get_sheet_by_name('基础IO')
ws = wb['基础IO']

# 获取修改目标名称
# 行号范围
excel_script_name_list = []
for case_row_index in range(358, 376):
    script_name = ws['B' + str(case_row_index)].value
    if script_name:
        excel_script_name_list.append(script_name)
# print(excel_script_name_list)
print("excel中相对应的文件名数量为：%d" % len(excel_script_name_list))
# os.rename("case_script", cls.script_name + '.py')    # 格式化

# rename
if len(excel_script_name_list) == len(wait_to_rename_list):
    for i in range(len(excel_script_name_list)):
        print("origin_name:"+wait_to_rename_list[i][0:20])
        print("rename:"+excel_script_name_list[i])
        if wait_to_rename_list[i][0:20] in excel_script_name_list[i] and os.path.exists(file_path+"\\"+wait_to_rename_list[i]):
            print("文件名称匹配成功，重命名ing")
            os.chdir(file_path)
            # os.rename(
            #     file_path+"\\"+wait_to_rename_list[i], file_path+"\\"+excel_script_name_list[i])    # rename
            #os.rename(os.path.join(file_path, wait_to_rename_list[i]), os.path.join(file_path, excel_script_name_list[i]))
            old_name = wait_to_rename_list[i]
            new_name = excel_script_name_list[i].split('/')[-1]
            os.renames(os.path.join(file_path, old_name),
                       os.path.join(file_path, new_name))
        else:
            print("文件名称匹配失败")
