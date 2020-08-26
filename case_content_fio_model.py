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
        # 测试工具选择fio
        cls.fio_parameters_dict[FioEnum.FIO_USE.value] = False
        # 测试时长设置
        cls.fio_parameters_dict[FioEnum.FIO_RUNTIME.value] = '120'
        # fio读写模式设置
        cls.fio_parameters_dict[FioEnum.FIO_RW.value] = None
        # 测试数据块大小及分配设置
        cls.fio_parameters_dict[FioEnum.FIO_BSSPLIT.value] = None
        # 测试数据的随机比
        cls.fio_parameters_dict[FioEnum.FIO_SEEKPCT.value] = 0
        # 读写比例
        cls.fio_parameters_dict[FioEnum.FIO_RWMIXREAD.value] = None


def main() -> None:
    BasicioJbodRandomRead.run()


if __name__ == '__main__':
    main()
