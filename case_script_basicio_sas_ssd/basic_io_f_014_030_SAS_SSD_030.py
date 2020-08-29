#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io-f-014-030
case title: 基础IO-SAS-SSD-多种大IO-随机写
test category: SAS-SSD-基础IO
check point: 基础IO-SAS-SSD-多种大IO-随机写
test platform: 模拟平台/物理平台/模拟平台&物理平台

author: lihaoran
date: 2020.08.29
description:
@steps: 1、组建符合条件的VD后进行快速初始化
        2、进行IO的vdbench配置：测试时间 elapse=2min，IO并发thread=32，随机比例seekpct=50，
        读写比例rdpct=0，xfersize=（10M，64M，128M，256M）测试并发随机写，
        3、进行数据一致性校验
        4、清理环境
        

@changelog:
"""

import add_syspath
from scripts.system_test.basic_io.basicio_multi_vd_in_DG_script_base import BasicioMultiVDScriptBase

class BasicioSasSsdRandomWrite(BasicioMultiVDScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
        # 物理盘参数设置
        # x2或x4
        cls.phy_parameters_dict['controller_interface'] = 'x4'
        # 测试盘的接口设置
        cls.phy_parameters_dict['pd_interface'] = 'SATA'
        # 测试盘的介质设置
        cls.phy_parameters_dict['pd_medium'] = 'HDD'

        # 虚拟盘参数设置
        # 组raid所用的磁盘数量
        cls.phy_parameters_dict['pd_count'] = 4
        # 要组建的raid虚拟盘数量
        cls.vd_parameters_dict['vd_count'] = 1
        # raid级别
        cls.vd_parameters_dict['vd_type'] = 'Raid5'
        # 条带大小
        cls.vd_parameters_dict['vd_strip'] = '128'

        # 测试工具参数设置
        # 测试工具选择vdbench
        cls.vdbench_parameters_dict['use_vdbench'] = True
        # 测试时长设置
        cls.vdbench_parameters_dict['elapsed'] = '120'
        # 测试数据读写比例设置
        cls.vdbench_parameters_dict['rdpct'] = '0'
        # 测试数据随即比例设置
        cls.vdbench_parameters_dict['seekpct'] = '50'
        # 测试数据块大小及分配设置
        cls.vdbench_parameters_dict['xfersize'] = '(10M,25,64M,25,128M,25,256M,25)'
        # vdbench一致性校验
        cls.vdbench_parameters_dict['consistency_check'] = True
        # 偏移量
        cls.vdbench_parameters_dict['offset'] = None
        # 对齐
        cls.vdbench_parameters_dict['align'] = None
        # 测试区间
        cls.vdbench_parameters_dict['range'] = None


def main() -> None:
    BasicioSasSsdRandomWrite.run()

if __name__ == '__main__':
    main()
