#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io-f-001-009
case title: 基础IO-JBOD-多种小IO-随机写
test category: JBOD-基础IO
check point: 基础IO-JBOD-多种小IO-随机写
test platform: 模拟平台/物理平台/模拟平台&物理平台

author: liuyuan
date: 2020.08.24
description:
@steps: 1、组建JBOD
        2、进行IO的vdbench配置：测试时间 elapse=2min，IO并发thread=32，随机比例seekpct=50，
        读写比例rdpct=0，xfersize=（2K，16K，32K，64K）测试并发随机写，
        3、清理环境
        

@changelog:
"""

import add_syspath

from scripts.system_test.basic_io.basicio_jbod_script_base import BasicioJBODScriptBase
from scripts.script_libs.enum_variable import FioEnum

class 2(BasicioJBODScriptBase):

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
        cls.fio_parameters_dict[FioEnum.FIO_USE.value] = True
        # 测试时长设置
        cls.fio_parameters_dict[FioEnum.FIO_RUNTIME.value] = '120'
        # fio读写模式设置
        cls.fio_parameters_dict[FioEnum.FIO_RW.value] = 'randwrite'
        # 测试数据块大小及分配设置
        cls.fio_parameters_dict[FioEnum.FIO_BSSPLIT.value] = '(2K，16K，32K，64K)'
        # 测试数据的随机比
        cls.fio_parameters_dict[FioEnum.FIO_SEEKPCT.value] = 50
        # 读写比例
        cls.fio_parameters_dict[FioEnum.FIO_RWMIXREAD.value] = '0'
        # 偏移量
        cls.fio_parameters_dict[FioEnum.FIO_OFFSET.value] = None
        # 对齐
        cls.fio_parameters_dict[FioEnum.FIO_BLOCKALIGN.value] = None

def main() -> None:
    2.run()

if __name__ == '__main__':
    main()
