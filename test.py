import shutil
import os
from openpyxl import Workbook
from openpyxl import load_workbook

wb = load_workbook('D:\\Sugon_Work\openpyxl_script_create\\基础IO_0815_612.xlsx', read_only=True)
print(wb.sheetnames)

ws = wb.active

case_row_index = input("输入测试用例行号：")


# case description
script_name = ws['B{}'.format(case_row_index)].value
case_number = ws['A{}'.format(case_row_index)].value
case_title = ws['E{}'.format(case_row_index)].value
description = case_title
test_category = ws['K{}'.format(case_row_index)].value
check_point: ws['L{}'.format(case_row_index)].value
step_raw_info = ws['O{}'.format(case_row_index)].value    # steps原始信息，需处理

# case model
script_path = os.getcwd()    # 获取当前路径
print(script_path)
source = script_path+'\case_content_model.py'
target = script_path+'\case_script'
shutil.copy(source, target)

# modified data

# 1. 修改脚本描述内容
lines = []
f = open(target, 'r', encoding='UTF-8')
flist = f.readlines()
f = open(target, 'w', encoding='UTF-8')
flist[3] = 'case number: {}\n'.format(case_number)
flist[4] = 'case title: {}\n'.format(case_title)
flist[5] = 'test category: {}\n'.format(test_category)
#flist[6] = 'check point: {}\n'.format(check_point)
flist[10] = 'description: {}\n'.format(description)
f.writelines(flist)
f.close()

# 1. 抽取 vdbench parameters
def find_vdbench_parameter(step_content:str, parameter:str) -> int:
    index = step_content.find(parameter)
    num_str = ''
    for i in range(index+len(parameter)+1, index+len(parameter)+5):
        if step_content[i].isdigit():
            num_str += step_content[i]
    return int(num_str)

def find_vdbench_xfersize(step_content:str) -> str:
    index1 = step_content.find('（')
    index2 = step_content.find('）')
    res = step_content[index1+1:index2]
    return res

vdbench_cc = False
if '写' in case_title:
    vdbench_cc = True
    
vdbench_seekpct = find_vdbench_parameter(step_raw_info, 'seekpct')
print(vdbench_seekpct)
vdbench_rdpct = find_vdbench_parameter(step_raw_info, 'rdpct')
print(vdbench_rdpct)
vdbench_xfersize = find_vdbench_xfersize(step_raw_info)
print(vdbench_xfersize)


# 2. 设置脚本相关的变量名
lines = []
f = open(target, 'r', encoding='UTF-8')
flist = f.readlines()
f = open(target, 'w', encoding='UTF-8')
# 2.1 修改脚本类名
script_class_name = input("输入脚本类名：")
flist[22] = 'class {}(BasicioJBODScriptBase):\n'.format(script_class_name)

# 2.2 设置脚本参数
flist[29] = "        cls.vdbench_parameters_dict['seekpct'] = '{}'\n".format(vdbench_seekpct)
flist[30] = "        cls.vdbench_parameters_dict['rdpct'] = '{}'\n".format(vdbench_rdpct)
flist[31] = "        cls.vdbench_parameters_dict['xfersize'] = '({})'\n".format(vdbench_xfersize)
flist[32] = "        cls.vdbench_parameters_dict['consistency_check'] = {}\n".format(vdbench_cc)

flist[36] = '    {}.run()'.format(script_class_name)

f.writelines(flist)
f.close()

# replace  a  py
os.rename("case_script", script_name+'.py')    # 重命名(可以放到最后)


