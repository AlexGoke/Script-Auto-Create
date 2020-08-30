"""
author: liuyuan
date: 2020.08.25
description: 自动脚本生成工具 扩展功能类
"""


class FuncSet(object):

    def __init__(self):
      pass

    # 获取测试用例要求的 vdbench/fio 参数信息
    @classmethod
    def find_tool_parameter(cls, step_content:str, parameter:list) -> dict:
        """
        @description  : 从测试用例的操作步骤信息中，获取测试工具需要设置的参数的数值
        ---------
        @param  ：
        step_content： 按行切分后的操作步骤信息
        parameter:  需要查找的参数名称列表
        -------
        @Returns  : 想要查找的参数 对应的的名称-值字典
        -------
        """
        res = {}
        for x in range(len(parameter)):
            if parameter[x] == 'xfersize' or parameter[x] == 'bssplit':
                res[parameter[x]] = cls.find_vdbench_xfersize(step_content, 'vdbench')
                continue
            parameter_index = step_content.find(parameter[x])
            num_str = ''
            if parameter_index != -1:
                for i in range(parameter_index+len(parameter)+1, parameter_index+len(parameter)+7):
                    if step_content[i].isdigit():
                        num_str += step_content[i]
                res[parameter[x]] = int(num_str)
            else:
                res[parameter[x]] = None
        return res


    # 获取vdbench/fio 数据块参数
    @staticmethod
    def find_vdbench_xfersize(step_content:str, tool:str) -> str:
        """
        @description  : 在测试用例的操作步骤信息中，获取vdbench/fio的测试数据块数值。测试用例中写的都是
        vdbench及xfersize，所以搜索方法只需要搜索xfersize就可以
        ---------
        @param  :
        step_content: 按行切分后的操作步骤信息
        tool: 该测试用例 选用的测试工具名称
        -------
        @Returns  : 该测试工具设置的数据块值
        -------
        """
        index1 = step_content.find('（')
        index2 = step_content.find('）')
        # 数据块是多个值的情况
        if index1 != -1 and index2 != -1:
            res = step_content[index1+1:index2]
            # if tool == 'vdbench' or tool == 'v':
            res = res.replace('，', ',25,')
            res = res.replace(' ', '')
            return res+',25'
        # 数据块是单一值的情况
        else:
            xfersize_index = step_content.find('xfersize')
            num_str = ''
            if xfersize_index != -1:
                for i in range(xfersize_index+len('xfersize')+1, xfersize_index+len('xfersize')+7):
                    if step_content[i].isdigit():
                        num_str += step_content[i]
                res = num_str+'k'
        return res


    # 获取vdbench是否需要一致性校验
    @staticmethod
    def need_vdbench_cc(case_title:str, offset:int, align:int) -> bool:
        """
        @description  : 该测试用例vdbench是否需要一致性校验
        ---------
        @param  : case_title: 测试用例标题
        -------
        @Returns  : true需要cc；false不需要cc
        -------
        """
        vdbench_cc = False
        if '写' in case_title and not offset and not align:
            vdbench_cc = True
        return vdbench_cc


    # 获取fio的 读写模式(rw) 设置参数
    @staticmethod
    def find_fio_rw(case_title:str) -> str:
        """
        @description  : fio工具需要设置的读写模式
        ---------
        @param  : case_title: 测试用例标题
        -------
        @Returns  : 读写模式的参数值
        -------
        """
        if '顺序读写' in case_title:
            return 'rw'
        elif '随机读写' in case_title:
            return 'randrw'
        elif '顺序读' in case_title:
            return 'read'
        elif '随机读' in case_title:
            return 'randread'
        elif '顺序写' in case_title:
            return 'write'
        elif '随机写' in case_title:
            return 'randwrite'
        else:
            pass
