"""
author: liuyuan
description: 根据测试用例excel自动脚本生成工具
version: 1.0 / 2020.08.25 / basicio-jbod-vdbench/fio 自动生成

"""

import shutil
import os
import abc

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
    test_scene_info = None
    step_raw_info = ''
    step_info = ''

    tool_para_dict = {}    # 该类测试用例

    def __init__(self):
        pass

    @classmethod
    def case_excel_access(cls, need_parameter:list):
        """
        description: 测试用例excel各种信息获取
        parameter:   need_parameter: 想要在测试用例的excel中获取到的参数名称列表
        """
        cls.script_name = ws['B{}'.format(case_row_index)].value
        cls.case_number = ws['A{}'.format(case_row_index)].value
        cls.case_title = ws['E{}'.format(case_row_index)].value
        cls.description = cls.case_title
        cls.test_category = ws['K{}'.format(case_row_index)].value
        cls.check_point = ws['L{}'.format(case_row_index)].value
        cls.test_scene_info = ws['N{}'.format(case_row_index)].value
        cls.step_raw_info = ws['O{}'.format(case_row_index)].value    # steps原始信息，需处理
        cls.step_info = cls.step_raw_info.split('\n')
        # 抽取测试用例中 vdbench/fio common-parameters
        cls.tool_para_dict = FuncSet.find_tool_parameter(cls.step_raw_info, need_parameter)
        # if cls.tool_para_dict['xfersize']:
        #     print('{} 块大小设置为：{}'.format(tool, cls.tool_para_dict['xfersize']))

    @classmethod
    def model_info_access(cls, template:str) -> None:
        """
        description ： 复制获取用例的模板内容
        parameter:     模板文件名称
        """
        script_path = os.getcwd()    # 获取当前路径
        # if tool == 'v' or tool == 'vdbench':
        #     source = script_path+'\case_content_vdb_model_jbod.py'
        # elif tool == 'f' or tool == 'fio':
        #     source = script_path+'\case_content_fio_model_jbod.py'
        source = script_path + '\\' + template
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
        cls.flist[12] = '@steps: {}\n'.format(cls.step_info[0])
        raw_num = 12
        temp_str = ''
        i = 1
        while i < len(cls.step_info):
            raw_num += 1
            if len(cls.step_info[i]) > 70:    # 需要加行
                temp = ''
                step_long_raw = cls.step_info[i].split('，')
                for x in range(len(step_long_raw)):
                    if len(temp) + len(step_long_raw[x]) < 70:
                        temp += (step_long_raw[x] + '，')
                    elif len(temp) + len(step_long_raw[x]) >= 70:
                        cls.flist.insert(raw_num, '        {}\n'.format(temp))
                        temp = step_long_raw[x]+'，'
                        raw_num += 1
                cls.flist.insert(raw_num, '        {}\n'.format(temp))
            else:
                cls.flist.insert(raw_num, '        {}\n'.format(cls.step_info[i]))
            i += 1

        # 2 修改脚本类名
        run_raw_num = [x for x in range(raw_num, len(cls.flist)) if 'class' in cls.flist[x]][0]
        cls.flist[run_raw_num] = cls.flist[run_raw_num].replace('xxx', script_class_name)
        
        # 测试场景设置 —— 先针对raid&jbod部分 添加这个函数，之后重构
        cls.testscene_parameter_set(run_raw_num, cls.flist, cls.test_scene_info)
        # 测试工具设置
        cls.testtool_parameter_set(run_raw_num, cls.flist, cls.tool_para_dict)

        # 3 修改脚本末尾的内容
        run_raw_num = [x for x in range(45, len(cls.flist)) if 'run' in cls.flist[x]][0]
        cls.flist[run_raw_num] = '    {}.run()'.format(script_class_name)
        f = open(cls.target, 'w', encoding='UTF-8')
        f.writelines(cls.flist)
        f.close()
        os.rename("case_script", cls.script_name +'.py')    # 格式化

    @classmethod
    @abc.abstractmethod
    def testscene_parameter_set(cls, raw_num:int, flist:str, test_scene_info:str) -> None:
        """
        description: 测试场景的参数设置
        parameter：  raw_num:         起始行号
                     test_scene_dict: 测试场景信息
        """
        # 先确定target_list
        test_scene = test_scene_info.split('\n')
        target_list = []
        reference = ['JBOD', 'Raid1', 'Raid5']
        for i in range(len(reference)):
            if reference[i] in test_scene[2]:
                disk1 = reference[i]
            if reference[i] in test_scene[6]:
                disk2 = reference[i]
        target_list.append(disk1)
        target_list.append(disk2)
        # 为了正确适配基类，对target_list顺序调整一下
        if target_list[0] == 'JBOD' and 'Raid' in target_list[1]:
            target_list[0], target_list[1] = target_list[1], target_list[0]
        target_list_raw_num = [x for x in range(raw_num, len(cls.flist)) if 'target' in cls.flist[x]][0]
        cls.flist[target_list_raw_num] = '        cls.target_list = {}'.format(target_list)

        
        # 模板信息
        text_1_raid = """
        # raid盘 物理接口设置
        cls.phy_parameters_dict['the_first_pd_interface'] = 'SATA'
        # raid盘 物理介质设置
        cls.phy_parameters_dict['the_first_pd_medium'] = 'HDD'
        # raid盘 所用的磁盘数量
        cls.phy_parameters_dict['the_first_pd_count'] = {}
        # raid盘 条带大小
        cls.vd_parameters_dict['the_first_vd_strip'] = '{}'
        """
        
        text_2_raid = """
        # raid盘 物理接口设置
        cls.phy_parameters_dict['the_second_pd_interface'] = 'SATA'
        # raid盘 物理介质设置
        cls.phy_parameters_dict['the_second_pd_medium'] = 'HDD'
        # raid盘 所用的磁盘数量
        cls.phy_parameters_dict['the_second_pd_count'] = {}
        # raid盘 条带大小
        cls.vd_parameters_dict['the_second_vd_strip'] = '{}'
        """
        
        text_1_jbod = """
        # jbod盘 物理接口设置
        cls.phy_parameters_dict['jbod_interface'] = 'SATA'
        # jbod盘 物理介质设置
        cls.phy_parameters_dict['jbod_medium'] = 'HDD'
        # jbod盘 所用的磁盘数量
        cls.phy_parameters_dict['jbod_count'] = {}
        
        """
        raw_num = target_list_raw_num + 1
        # 确定disk1，disk2的count、stripe
        if target_list[0] == 'JBOD' and target_list[1] == 'JBOD':
            flist.insert(raw_num, text_1_jbod.format('2'))
        elif 'Raid1' == target_list[0] and 'Raid5' == target_list[1]:
            flist.insert(raw_num, text_2_raid.format('4', '64'))
            flist.insert(raw_num, text_1_raid.format('2', '256'))
            # raw_num += len(text_1_raid.split('\n'))
        elif 'Raid5' == target_list[0] and 'JBOD' == target_list[1]:
            flist.insert(raw_num, text_1_jbod.format('1'))
            flist.insert(raw_num, text_1_raid.format('4', '256'))
            # raw_num += len(text_1_raid.split('\n'))
        
        
    @classmethod
    def testtool_parameter_set(cls, raw_num:int, flist:str, tool_para_dict:dict) -> None:
        """
        description: 测试工具的参数设置
        parameter:  raw_num:  脚本内容中工具参数的第一行号
                    flist:    脚本内容
                    tool_para_didt:  测试工具相关参数字典
        return：None
        """
        if tool == 'v' or tool == 'vdbench':
            vdbench_cc = FuncSet.need_vdbench_cc(cls.case_title, cls.tool_para_dict['offset'], cls.tool_para_dict['align'])
            print('vdbench一致性校验：{}'.format(vdbench_cc))
            for i in range(raw_num, len(flist)):
                # if 'use' in flist[i]:
                #    flist[i] = "        cls.vdbench_parameters_dict['use_vdbench'] = {}\n".format(True)
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
                # if 'USE' in flist[i]:
                #     flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_USE.value] = {}\n".format(True)
                if 'RWMIXREAD' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_RWMIXREAD.value] = '{}'\n".format(tool_para_dict['rdpct'])
                elif 'RW' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_RW.value] = '{}'\n".format(fio_rw)
                elif 'BSSPLIT' in flist[i]:
                    flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_BSSPLIT.value] = '({})'\n".format(tool_para_dict['bssplit'])
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
        cls.case_excel_access(need_parameter)
        print(cls.tool_para_dict)
        cls.model_info_access(template)
        cls.script_content_compose()


if __name__ == "__main__":
    test = case_script_auto_create()
    wb = load_workbook('D:\\Sugon_Work\\openpyxl_script_create\\基础IO_0815_612.xlsx', read_only=True)
    ws = wb.active

    # 每次生成一类脚本前需要修改的信息 全局变量
    case_row_index = None
    temp  = input("input case raw number:")
    tool = input('输入测试工具: ')
    script_class_name = input("输入脚本类名：")
    template = 'case_template_vdb_raid&jbod.py'    # 目前工具都跟着模板走
    need_parameter = ['rdpct', 'seekpct', 'offset', 'align', 'range', 'xfersize']    # 测试盘信息、测试工具信息 两个是放一起还是分开 目前还没有想清楚

    if '-' in temp:
        row_range = [int(x) for x in temp.split('-')]
        for i in range(row_range[0], row_range[1]+1):
            case_row_index = i
            test.script_generate()
    else:
        case_row_index = temp
        test.script_generate()
