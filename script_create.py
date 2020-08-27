"""
author: liuyuan
description: 根据测试用例excel自动脚本生成工具
version: 1.0 / 2020.08.25 / basicio-jbod-vdbench/fio 自动生成

"""

import shutil
import os

from openpyxl import Workbook
from openpyxl import load_workbook
from control import FuncSet

class case_script_auto_create():
    def __init__(self):
        pass

    def main(self):
        wb = load_workbook('D:\\Sugon_Work\openpyxl_script_create\\基础IO_0815_612.xlsx', read_only=True)
        #print(wb.sheetnames)
        ws = wb.active
        case_row_index = input("输入测试用例行号：")

        # 1. case description info get
        script_name = ws['B{}'.format(case_row_index)].value
        case_number = ws['A{}'.format(case_row_index)].value
        case_title = ws['E{}'.format(case_row_index)].value
        description = case_title
        test_category = ws['K{}'.format(case_row_index)].value
        check_point = ws['L{}'.format(case_row_index)].value
        step_raw_info = ws['O{}'.format(case_row_index)].value    # steps原始信息，需处理
        step_raw = step_raw_info.split('\n')

        # 1.1 抽取测试用例中 vdbench/fio common-parameters
        tool = input('输入测试工具: ')
        vdbench_rdpct = FuncSet.find_vdbench_parameter(step_raw_info, 'rdpct')
        fio_rwmixread = vdbench_rdpct
        print('vdbench/fio 读写比例设置为：{}'.format(vdbench_rdpct))

        vdbench_xfersize = FuncSet.find_vdbench_xfersize(step_raw_info, tool)
        fio_bssplit = vdbench_xfersize
        print('vdbench/fio 块大小设置为：{}'.format(vdbench_xfersize))

        vdbench_seekpct = FuncSet.find_vdbench_parameter(step_raw_info, 'seekpct')
        fio_seekpct = vdbench_seekpct
        print('vdbench 随机比例设置为：{}'.format(vdbench_seekpct))

        # 2. case model get
        script_path = os.getcwd()    # 获取当前路径
        if tool == 'v' or tool == 'vdbench':
            source = script_path+'\case_content_vdb_model.py'
        elif tool == 'f' or tool == 'fio':
            source = script_path+'\case_content_fio_model.py'
        target = script_path+'\case_script'
        shutil.copy(source, target)    # 之后改为新建一个txt

        f_model = open(source, 'r', encoding='UTF-8')
        # slist = f_model.readlines()
        flist = f_model.readlines()

        # 3. modified data
        # 3.1 修改脚本的注释描述内容
        flist[3] = 'case number: {}\n'.format(case_number)
        flist[4] = 'case title: {}\n'.format(case_title)
        flist[5] = 'test category: {}\n'.format(test_category)
        flist[6] = 'check point: {}\n'.format(check_point)

        # step 内容需要特殊处理
        flist[12] = '@steps: {}\n'.format(step_raw[0])
        raw_num = 12
        temp_str = ''
        i = 1
        while i < len(step_raw):
            raw_num += 1
            if len(step_raw[i]) > 70:    # 需要加行
                temp = ''
                step_long_raw = step_raw[i].split('，')
                for x in range(len(step_long_raw)):
                    if len(temp) + len(step_long_raw[x]) < 70:
                        temp += (step_long_raw[x] + '，')
                    elif len(temp) + len(step_long_raw[x]) >= 70:
                        flist.insert(raw_num, '        {}\n'.format(temp))
                        temp = step_long_raw[x]+'，'
                        raw_num += 1
                flist.insert(raw_num, '        {}\n'.format(temp))
            else:
                flist.insert(raw_num, '        {}\n'.format(step_raw[i]))
            i += 1

        # 修改脚本类名
        for i in range(raw_num, len(flist)):
            if 'class' in flist[i]:
                raw_num = i
                break
        script_class_name = input("输入脚本类名：")
        flist[raw_num] = 'class {}(BasicioJBODScriptBase):\n'.format(script_class_name)

        # 3.2 设置测试用例脚本参数
        if tool == 'v' or tool == 'vdbench':
            vdbench_cc = FuncSet.find_vdbench_cc(case_title)
            print('vdbench一致性校验：{}'.format(vdbench_cc))
            vdbench_offset = FuncSet.find_vdbench_parameter(step_raw_info, 'offset')
            print('vdbench偏移量：{}'.format(vdbench_offset))
            vdbench_align = FuncSet.find_vdbench_parameter(step_raw_info, 'align')
            print('vdbench对齐：{}'.format(vdbench_align))
            for i in range(raw_num, len(flist)):
                if 'use' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['use_vdbench'] = {}\n".format(True)
                elif 'rdpct' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['rdpct'] = '{}'\n".format(vdbench_rdpct)
                elif 'seekpct' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['seekpct'] = '{}'\n".format(vdbench_seekpct)
                elif 'xfersize' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['xfersize'] = '({})'\n".format(vdbench_xfersize)
                elif 'check' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['consistency_check'] = {}\n".format(vdbench_cc)
                elif vdbench_offset and 'offset' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['offset'] = {}\n".format(vdbench_offset)
                elif vdbench_align and 'align' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['align'] = {}\n".format(vdbench_align)
        elif tool == 'f' or tool == 'fio':
            fio_rw = FuncSet.find_fio_rw(case_title)
            for i in range(raw_num, 50):
                if 'USE' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_USE.value] = {}\n".format(True)
                elif 'RWMIXREAD' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_RWMIXREAD.value] = '{}'\n".format(fio_rwmixread)
                elif 'RW' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_RW.value] = '{}'\n".format(fio_rw)
                elif 'BSSPLIT' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_BSSPLIT.value] = '({})'\n".format(fio_bssplit)
                elif 'SEEKPCT' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_SEEKPCT.value] = {}\n".format(fio_seekpct)

        else:
            print('别闹，没这工具...')

        # 3.3 修改脚本末尾的内容
        run_raw_num = [x for x in range(45, len(flist)) if 'run' in flist[x]]
        flist[run_raw_num[0]] = '    {}.run()'.format(script_class_name)
        f = open(target, 'w', encoding='UTF-8')
        f.writelines(flist)
        f.close()
        os.rename("case_script", script_name+'.py')    # 格式化

if __name__ == "__main__":
    test = case_script_auto_create()
    while(1):
        test.main()


