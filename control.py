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
        index = step_content.find(parameter)
        num_str = ''
        for i in range(index+len(parameter)+1, index+len(parameter)+5):
            if step_content[i].isdigit():
                num_str += step_content[i]
        return int(num_str)

    # 获取vdbench/fio 数据块参数
    @staticmethod
    def find_vdbench_xfersize(step_content:str, tool:str) -> str:
        index1 = step_content.find('（')
        index2 = step_content.find('）')
        res = step_content[index1+1:index2]
        if tool == 'vdbench' or tool == 'v':
            res = res.replace('，', ',25,')
            return res+',25'
        return res

    # 获取vdbench是否需要一致性校验
    @staticmethod
    def find_vdbench_cc(case_title:str) -> bool:
        vdbench_cc = False
        if '写' in case_title:
            vdbench_cc = True
        return vdbench_cc

    # 获取fio的 读写模式(rw) 设置参数
    @staticmethod
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
