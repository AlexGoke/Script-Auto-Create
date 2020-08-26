#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: jbod脚本模板
case title: 
test category: 
check point: 
test platform: 模拟平台/物理平台/模拟平台&物理平台

author: liuyuan
date: 2020.08.24
description: 
@steps:

@changelog:
"""

import add_syspath

from scripts.system_test.basic_io.basicio_jbod_script_base import BasicioJBODScriptBase
from scripts.script_libs.enum_variable import FioEnum

class BasicioJbodRandomRead(BasicioJBODScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
        # 物理盘参数设置
        # 测试盘的接口设置
        cls.phy_parameters_dict['pd_interface'] = 'SATA'
        # 测试盘的介质设置
        cls.phy_parameters_dict['pd_medium'] = 'HDD'
        
        # 测试工具参数设置
        # 测试工具选择vdbench
        cls.vdbench_parameters_dict['use_vdbench'] = True
        # 测试时长设置
        cls.vdbench_parameters_dict['elapsed'] = '120'
        # 测试数据读写比例设置
        cls.vdbench_parameters_dict['rdpct'] = '100'
        # 测试数据随即比例设置
        cls.vdbench_parameters_dict['seekpct'] = '50'
        # 测试数据块大小及分配设置
        cls.vdbench_parameters_dict['xfersize'] = '(1k,25,15k,25,31k,25,64k,25)'
        # vdbench一致性校验
        cls.vdbench_parameters_dict['consistency_check'] = False


def main() -> None:
    BasicioJbodRandomRead.run()


if __name__ == '__main__':
    main()