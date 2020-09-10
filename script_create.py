"""
author: liuyuan
description: 根据测试用例excel自动脚本生成工具
             主体框架，根据需要在子类中实现 testscene 针对性的具体特殊功能
version: 1.0 / 2020.08.25 / basicio-jbod-vdbench/fio 自动生成

"""

import shutil
import os
import abc
import subprocess

from openpyxl import Workbook
from openpyxl import load_workbook
from expand_function import FuncSet


class case_script_auto_create(metaclass=abc.ABCMeta):

    excel = None
    # 每次生成一类脚本前需要修改的信息 全局变量
    # 键盘输入
    case_row_index = None     # 该用例的excel行号
    tool = ''                 # 该用例使用的测试工具
    script_class_name = ''    # 该用例的脚本类名
    # 子类传入
    template = ''
    need_parameter = []       # 测试盘信息、测试工具信息 两个是放一起还是分开 目前还没有想清楚

    flist = []                  # 该用例的脚本内容
    run_raw_num = 0             # 脚本内容行号
    target = None               # 最终生成的脚本对象

    # 脚本头部注释内容
    script_name = None
    case_number = None
    case_title = None
    description = None
    test_category = None
    check_point = None
    test_scene_info = None
    step_raw_info = ''
    step_info = ''

    tool_para_dict = {}    # 该类测试用例参数信息

    def __init__(self):
        pass

    @abc.abstractclassmethod
    def prepara(cls) -> None:
        """
        description:  脚本开始自动生成前完成获取相关信息准备工作，打开用例文件及输入必要的用例信息
        parametr：    None
        return：      None
        """
        pass

    @classmethod
    def prepara_base(cls) -> None:
        """
        description:  生成器的基础准备工作，所有脚本类型需准备的相同的部分
        parametr：    None
        return：      None
        """
        wb = load_workbook(
            'D:\\Sugon_Work\\openpyxl_script_create\\基础IO20200907.xlsx', read_only=True)
        cls.excel = wb.active

        # 每次生成一类脚本前需要修改的信息 全局变量
        cls.tool = input('输入测试工具: ')
        cls.script_class_name = input("输入脚本类名：")
        # cls.template = 'case_template_vdb_raid&jbod.py'    # 子类给值
        # 测试盘信息、测试工具信息 两个是放一起还是分开 目前还没有想清楚
        # cls.need_parameter = ['rdpct', 'seekpct', 'offset', 'align', 'range', 'xfersize']

    @classmethod
    def case_excel_access(cls, need_parameter: list, case_row_index: int) -> None:
        """
        description: 测试用例的excel中各种信息获取
        parameter:   need_parameter: 想要在测试用例的excel中获取到的参数名称列表
                     case_row_index: 测试用例所在excel的行号
        return：     None
        """
        ws = cls.excel
        cls.case_number = ws['A{}'.format(case_row_index)].value
        cls.script_name = ws['D{}'.format(case_row_index)].value
        cls.case_title = ws['G{}'.format(case_row_index)].value
        cls.description = cls.case_title
        cls.test_category = ws['L{}'.format(case_row_index)].value
        cls.check_point = ws['M{}'.format(case_row_index)].value
        cls.test_scene_info = ws['O{}'.format(case_row_index)].value
        cls.step_raw_info = ws['P{}'.format(
            case_row_index)].value    # steps原始信息，需处理
        cls.step_info = cls.step_raw_info.split('\n')
        # 抽取测试用例中 vdbench/fio common-parameters
        cls.tool_para_dict = FuncSet.find_tool_parameter(
            cls.step_raw_info, need_parameter, cls.tool)
        # if cls.tool_para_dict['xfersize']:
        #     print('{} 块大小设置为：{}'.format(tool, cls.tool_para_dict['xfersize']))

    @classmethod
    def model_info_access(cls, template: str) -> None:
        """
        description ： 复制获取用例的模板内容
        parameter:     template 模板文件名称
        return:        None
        """
        script_path = os.getcwd()    # 获取当前路径
        source = script_path + '\\template\\' + template
        cls.target = script_path+'\case_script'
        shutil.copy(source, cls.target)    # 之后改为新建一个txt
        f_model = open(source, 'r', encoding='UTF-8')
        cls.flist = f_model.readlines()

    @classmethod
    def script_content_compose(cls) -> int:
        """
        @description : 组合完成脚本内容
        """
        # 1 修改脚本的注释描述内容
        cls.flist[3] = 'case number: {}\n'.format(cls.case_number)
        cls.flist[4] = 'case title: {}\n'.format(cls.case_title)
        cls.flist[5] = 'test category: {}\n'.format(cls.test_category)
        cls.flist[6] = 'check point: {}\n'.format(cls.check_point)

        # 2 步骤内容需要特殊处理
        #cls.flist[12] = '@steps: {}\n'.format(cls.step_info[0])
        raw_num = 14
        temp_str = ''
        i = 0
        for i in range(len(cls.step_info)):
            if len(cls.step_info[i]) > 70:    # 需要加行
                temp = ''
                step_long_raw = cls.step_info[i].split('，')
                for x in range(len(step_long_raw)):
                    if len(temp) + len(step_long_raw[x]) < 70:
                        temp += (step_long_raw[x] + '，')
                    elif len(temp) + len(step_long_raw[x]) >= 70:
                        cls.flist.insert(raw_num, '{}\n'.format(temp))
                        temp = step_long_raw[x]+'，'
                        raw_num += 1
                cls.flist.insert(raw_num, '{}\n'.format(temp))
            elif len(cls.step_info)-1 == i:
                cls.flist.insert(raw_num, '{}'.format(cls.step_info[i]))
            else:
                cls.flist.insert(
                    raw_num, '{}\n'.format(cls.step_info[i]))
            i += 1
            raw_num += 1

        # 2 修改脚本类名
        for i in range(raw_num, len(cls.flist)):
            if 'class' in cls.flist[i]:
                cls.run_raw_num = i
                break
        cls.flist[cls.run_raw_num] = cls.flist[cls.run_raw_num].replace(
            'xxx', cls.script_class_name)

    @classmethod
    @abc.abstractmethod
    def testscene_parameter_set(cls, raw_num: int, flist: str, test_scene_info: str) -> None:
        """
        description: 测试场景的参数设置——————由各类脚本生成器子类实现
        parameter：  raw_num:         起始行号
                     flist:           脚本内容缓存
                     test_scene_dict: 测试场景信息
        """
        pass

    @classmethod
    def script_content_end(cls) -> None:
        """
        description: 修改脚本末尾的内容
        """
        for i in range(len(cls.flist)-1, -1, -1):
            if 'run' in cls.flist[i]:
                cls.run_raw_num = i
        cls.flist[cls.run_raw_num] = cls.flist[cls.run_raw_num].replace(
            'xxx', cls.script_class_name)
        f = open(cls.target, 'w', encoding='UTF-8')
        f.writelines(cls.flist)
        f.close()
        os.rename("case_script", cls.script_name + '.py')    # 格式化
        cmd = "autopep8 --in-place --aggressive --aggressive {}.py".format(
            cls.script_name)
        # subprocess.getoutput(cmd)

    @classmethod
    def testtool_parameter_set(cls, raw_num: int, flist: str, tool_para_dict: dict, tool: str) -> None:
        """
        description: 测试工具的参数设置
        parameter:  raw_num:  脚本内容中工具参数的第一行号
                    flist:    脚本内容
                    tool_para_didt:  测试工具相关参数字典
        return：None
        """
        if tool == 'v' or tool == 'vdbench':
            vdbench_cc = FuncSet.need_vdbench_cc(
                cls.case_title, cls.tool_para_dict['offset'], cls.tool_para_dict['align'])
            tool_para_dict['vdbench_cc'] = vdbench_cc
            print('vdbench一致性校验：{}'.format(vdbench_cc))
            FuncSet.vdbench_parameter_set(
                raw_num, flist, tool_para_dict, vdbench_cc)
        elif tool == 'f' or tool == 'fio':
            fio_rw = FuncSet.find_fio_rw(cls.case_title)
            FuncSet.fio_parameter_set(raw_num, flist, tool_para_dict, fio_rw)
        else:
            print('别闹，没这工具...')

    @classmethod
    def script_generate(cls):
        """
        @description  : 生成脚本——主流程
        """
        cls.case_excel_access(cls.need_parameter, cls.case_row_index)
        print(cls.tool_para_dict)
        print(cls.template)
        cls.model_info_access(cls.template)
        cls.script_content_compose()
        # 测试场景设置 ———— 根据excel种测试场景信息，获取设置相应参数
        # 先针对raid&jbod部分 添加这个函数，之后重构[各类脚本定制化]
        cls.testscene_parameter_set(
            cls.run_raw_num, cls.flist, cls.test_scene_info)
        # 测试工具设置
        cls.testtool_parameter_set(
            cls.run_raw_num, cls.flist, cls.tool_para_dict, cls.tool)
        cls.script_content_end()

    @classmethod
    def run(cls) -> None:
        """
        description:    负责循环运行逻辑
        """
        cls.prepara()
        temp = input("input case raw number:")
        if '-' in temp:
            row_range = [int(x) for x in temp.split('-')]
            for i in range(row_range[0], row_range[1]+1):
                cls.case_row_index = i
                cls.script_generate()
        else:
            cls.case_row_index = temp
            cls.script_generate()


if __name__ == "__main__":
    print('目前基类已经不作为程序入口了，请创建针对脚本类型的子类脚本')
    pass
