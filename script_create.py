"""
author: liuyuan
description: 根据测试用例excel自动脚本生成工具
version: 1.0 / 2020.08.25 / basicio-jbod-vdbench/fio 自动生成

"""

import shutil
import os

from openpyxl import Workbook
from openpyxl import load_workbook
from expand_function import FuncSet

class case_script_auto_create():

    # 类属性
    # tool = None                 # 该用例使用的测试工具
    # script_class_name = None    # 该用例的脚本类名
    # case_row_index = None       # 该用例的excel行号
    flist = []                  # 该用例的脚本内容

    target = None               # 最终生成的脚本对象

    script_name = None
    case_number = None
    case_title = None
    description = None
    test_category = None
    check_point = None
    step_raw_info = ''
    step_raw = ''

    tool_para_dict = {}

    def __init__(self):
        pass

    @classmethod
    def case_excel_access(cls):
        """
        @description: 测试用例excel各种信息获取
        """
        cls.script_name = ws['B{}'.format(case_row_index)].value
        cls.case_number = ws['A{}'.format(case_row_index)].value
        cls.case_title = ws['E{}'.format(case_row_index)].value
        cls.description = cls.case_title
        cls.test_category = ws['K{}'.format(case_row_index)].value
        cls.check_point = ws['L{}'.format(case_row_index)].value
        cls.step_raw_info = ws['O{}'.format(case_row_index)].value    # steps原始信息，需处理
        cls.step_raw = cls.step_raw_info.split('\n')

        # 抽取测试用例中 vdbench/fio common-parameters
        need_tool_parameter = ['rdpct', 'seekpct', 'offset', 'align', 'range']
        cls.tool_para_dict = FuncSet.find_tool_parameter(cls.step_raw_info, need_tool_parameter)

        cls.tool_para_dict['xfersize']  = FuncSet.find_vdbench_xfersize(cls.step_raw_info, tool)
        cls.tool_para_dict['bssplit'] = cls.tool_para_dict['xfersize']
        print('{} 块大小设置为：{}'.format(tool, cls.tool_para_dict['xfersize']))

    @classmethod
    def model_info_access(cls):
        """
        @description ： 复制获取用例的模板内容
        """
        script_path = os.getcwd()    # 获取当前路径
        if tool == 'v' or tool == 'vdbench':
            source = script_path+'\case_content_vdb_model_jbod.py'
        elif tool == 'f' or tool == 'fio':
            source = script_path+'\case_content_fio_model_jbod.py'
        cls.target = script_path+'\case_script'
        shutil.copy(source, cls.target)    # 之后改为新建一个txt
        f_model = open(source, 'r', encoding='UTF-8')
        cls.flist = f_model.readlines()

    @classmethod
    def script_content_compose(cls):
        """
        @description : 组合完成脚本内容
        """
        # 1 修改脚本的注释描述内容
        cls.flist[3] = 'case number: {}\n'.format(cls.case_number)
        cls.flist[4] = 'case title: {}\n'.format(cls.case_title)
        cls.flist[5] = 'test category: {}\n'.format(cls.test_category)
        cls.flist[6] = 'check point: {}\n'.format(cls.check_point)

        # 2 步骤内容需要特殊处理
        cls.flist[12] = '@steps: {}\n'.format(cls.step_raw[0])
        raw_num = 12
        temp_str = ''
        i = 1
        while i < len(cls.step_raw):
            raw_num += 1
            if len(cls.step_raw[i]) > 70:    # 需要加行
                temp = ''
                step_long_raw = cls.step_raw[i].split('，')
                for x in range(len(step_long_raw)):
                    if len(temp) + len(step_long_raw[x]) < 70:
                        temp += (step_long_raw[x] + '，')
                    elif len(temp) + len(step_long_raw[x]) >= 70:
                        cls.flist.insert(raw_num, '        {}\n'.format(temp))
                        temp = step_long_raw[x]+'，'
                        raw_num += 1
                cls.flist.insert(raw_num, '        {}\n'.format(temp))
            else:
                cls.flist.insert(raw_num, '        {}\n'.format(cls.step_raw[i]))
            i += 1

        # 修改脚本类名
        for i in range(raw_num, len(cls.flist)):
            if 'class' in cls.flist[i]:
                raw_num = i
                break
        cls.flist[raw_num] = 'class {}(BasicioMultiVDScriptBase):\n'.format(script_class_name)

        cls.testtool_parameter_set(raw_num, cls.flist, cls.tool_para_dict)

        # 修改脚本末尾的内容
        run_raw_num = [x for x in range(45, len(cls.flist)) if 'run' in cls.flist[x]]
        cls.flist[run_raw_num[0]] = '    {}.run()'.format(script_class_name)
        f = open(cls.target, 'w', encoding='UTF-8')
        f.writelines(cls.flist)
        f.close()
        os.rename("case_script", cls.script_name+'.py')    # 格式化

    @classmethod
    def testtool_parameter_set(cls, raw_num:int, flist:str, tool_para_dict:dict) -> None:
        """
        description: 测试工具的参数设置
        parameter:  raw_num:  脚本内容中工具参数的第一行号
                    flist:    脚本内容
                    tool_para_didt:  工具参数字典
        return：
        """
        if tool == 'v' or tool == 'vdbench':
            vdbench_cc = FuncSet.need_vdbench_cc(cls.case_title, cls.tool_para_dict['offset'], cls.tool_para_dict['align'])
            print('vdbench一致性校验：{}'.format(vdbench_cc))
            for i in range(raw_num, len(flist)):
                # if 'use' in flist[i]:
                #    flist[i] = "        cls.vdbench_parameters_dict['use_vdbench'] = {}\n".format(True)    # 多余了
                if 'rdpct' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['rdpct'] = '{}'\n".format(tool_para_dict['rdpct'])
                elif 'seekpct' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['seekpct'] = '{}'\n".format(tool_para_dict['seekpct'])
                elif 'xfersize' in flist[i]:
                    if ',' in tool_para_dict['xfersize']:
                        flist[i] = "        cls.vdbench_parameters_dict['xfersize'] = '({})'\n".format(tool_para_dict['xfersize'])
                    else:
                        flist[i] = "        cls.vdbench_parameters_dict['xfersize'] = '{}'\n".format(tool_para_dict['xfersize'])
                elif 'check' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['consistency_check'] = {}\n".format(vdbench_cc)
                elif tool_para_dict['offset'] and 'offset' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['offset'] = '{}'\n".format(tool_para_dict['offset'])
                elif tool_para_dict['align'] and 'align' in flist[i]:
                    flist[i] = "        cls.vdbench_parameters_dict['align'] = '{}K'\n".format(tool_para_dict['align'])
        elif tool == 'f' or tool == 'fio':
            fio_rw = FuncSet.find_fio_rw(cls.case_title)
            for i in range(raw_num, 50):
                if 'USE' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_USE.value] = {}\n".format(True)
                elif 'RWMIXREAD' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_RWMIXREAD.value] = '{}'\n".format(tool_para_dict['rdpct'])
                elif 'RW' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_RW.value] = '{}'\n".format(fio_rw)
                elif 'BSSPLIT' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_BSSPLIT.value] = '({})'\n".format(cls.tool_para_dict['bssplit'])
                elif 'SEEKPCT' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_SEEKPCT.value] = {}\n".format(tool_para_dict['seekpct'])
                elif tool_para_dict['offset'] and 'offset' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_OFFSET.value] = {}\n".format(tool_para_dict['offset'])
                elif tool_para_dict['align'] and 'align' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_BLOCKALIGN.value] = {}\n".format(tool_para_dict['align'])
        else:
            print('别闹，没这工具...')

    @classmethod
    def script_generate(cls):
        """
        @description  : 生成脚本[单盘]——主流程
        """
        cls.case_excel_access()
        print(cls.tool_para_dict)
        cls.model_info_access()
        cls.script_content_compose()


if __name__ == "__main__":
    test = case_script_auto_create()
    wb = load_workbook('D:\\SugonWork\Script-Auto-Create\\基础IO_0815_612.xlsx', read_only=True)
    ws = wb.active
    temp  = input("input case raw number:")
    case_row_index = None
    tool = input('输入测试工具: ')
    script_class_name = input("输入脚本类名：")

    if '-' in temp:
      row_range = [int(x) for x in temp.split('-')]
      for i in range(row_range[0], row_range[1]+1):
        case_row_index = i
        test.script_generate()
    else:
      case_row_index = temp
      test.script_generate()
