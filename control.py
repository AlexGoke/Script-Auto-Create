"""
author: liuyuan
date: 2020.08.25
description: 自动脚本生成工具 功能集合类
"""

class FuncSet(object):
    def __init__():
      pass

    # 获取vdbench
    @staticmethod
    def find_vdbench_parameter(step_content:str, parameter:str) -> int:
        """
        @description  : 在测试用例的操作步骤信息中，获取传入的参数的数值
        ---------
        @param  ：step_content： 按行切分后的操作步骤信息
                     parameter： 要获取的参数名称
        -------
        @Returns  : 该参数的目标数值
        -------
        """
        index = step_content.find(parameter)
        num_str = ''
        for i in range(index+len(parameter)+1, index+len(parameter)+5):
            if step_content[i].isdigit():
                num_str += step_content[i]
        return int(num_str)

    # 获取vdbench/fio 数据块参数
    @staticmethod
    def find_vdbench_xfersize(step_content:str, tool:str) -> str:
        """
        @description  : 在测试用例的操作步骤信息中，获取vdbench/fio的测试数据块数值
        ---------
        @param  : step_content: 按行切分后的操作步骤信息
                          tool: 该测试用例 选用的测试工具名称
        -------
        @Returns  : 该测试工具设置的数据块值
        -------
        """
        index1 = step_content.find('（')
        index2 = step_content.find('）')
        res = step_content[index1+1:index2]
        if tool == 'vdbench' or tool == 'v':
            res = res.replace('，', ',25,')
            return res+',25'
        return res

    # 获取vdbench是否需要一致性校验
    """
    @description  : 该测试用例vdbench是否需要一致性校验
    ---------
    @param  : case_title: 测试用例标题
    -------
    @Returns  : true需要cc；false不需要cc
    -------
    """
    @staticmethod
    def find_vdbench_cc(case_title:str) -> bool:
        vdbench_cc = False
        if '写' in case_title:
            vdbench_cc = True
        return vdbench_cc

    # 获取fio的 读写模式(rw) 设置参数
    @staticmethod
    """
    @description  : fio工具需要设置的读写模式
    ---------
    @param  : case_title: 测试用例标题
    -------
    @Returns  : 读写模式的参数值
    -------
    """
    def find_fio_rw(case_title:str) -> str:
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
