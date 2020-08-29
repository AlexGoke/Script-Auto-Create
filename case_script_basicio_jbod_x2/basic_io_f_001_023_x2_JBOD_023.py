#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io-f-001-023
case title: 基础IO-JBOD-多种大小IO混合-顺序混合读写
test category: JBOD-基础IO
check point: 基础IO-JBOD-多种大小IO混合-顺序混合读写
test platform: 模拟平台/物理平台/模拟平台&物理平台

author: liuyuan
date: 2020.08.24
description:
@steps: 1、组建JBOD
        2、进行IO的vdbench配置：测试时间 elapse=2min，IO并发thread=32，随机比例seekpct=0，
        读写比例rdpct=70，xfersize=（2K，64K，128M，256M）测试并发顺序混合读写，
        3、清理环境
        

@changelog:
"""

import add_syspath

from scripts.system_test.basic_io.basicio_jbod_script_base import BasicioJBODScriptBase
from scripts.script_libs.enum_variable import FioEnum

class BasicIOJbodSequentialReadWrite(BasicioJBODScriptBase):

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
        cls.vdbench_parameters_dict['rdpct'] = '70'
        # 测试数据随即比例设置
        cls.vdbench_parameters_dict['seekpct'] = '0'
        # 测试数据块大小及分配设置
        cls.vdbench_parameters_dict['xfersize'] = '(2K,25,64K,25,128M,25,256M,25)'
        # vdbench一致性校验
        cls.vdbench_parameters_dict['consistency_check'] = True
        # 偏移量
        cls.vdbench_parameters_dict['offset'] = None
        # 对齐
        cls.vdbench_parameters_dict['align'] = None
        # 测试区间
        cls.vdbench_parameters_dict['range'] = None


def main() -> None:
    BasicIOJbodSequentialReadWrite.run()

if __name__ == '__main__':
    main()
