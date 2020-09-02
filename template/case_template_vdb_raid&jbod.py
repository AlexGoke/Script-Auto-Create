#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: raid & jbod 混合 并行读/写/读写 vdbench 测试用例模板
case title:
test category:
check point:
test platform: 模拟平台&物理平台

author: liuyuan
date: 2020.08.29
description:
@steps:

@changelog:
"""

import add_syspath
from scripts.system_test.basic_io.basicio_multiple_raid_script_base import BasicioMultipleRaidScriptBase


class xxx(BasicioMultipleRaidScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
        # 物理盘参数设置
        # x2或x4
        cls.phy_parameters_dict['controller_interface'] = 'x4'

        # 测试盘种类列表
        cls.target_list = ['', '']

        # 测试工具参数设置
        # 测试工具选择vdbench
        cls.vdbench_parameters_dict['use_vdbench'] = True
        # 测试时长设置
        cls.vdbench_parameters_dict['elapsed'] = '120'
        # 测试数据读写比例设置
        cls.vdbench_parameters_dict['rdpct'] = ''
        # 测试数据随即比例设置
        cls.vdbench_parameters_dict['seekpct'] = ''
        # 测试数据块大小及分配设置
        cls.vdbench_parameters_dict['xfersize'] = ''
        # vdbench一致性校验
        cls.vdbench_parameters_dict['consistency_check'] = False
        # 偏移量
        cls.vdbench_parameters_dict['offset'] = None
        # 对齐
        cls.vdbench_parameters_dict['align'] = None
        # 测试区间
        cls.vdbench_parameters_dict['range'] = None


def main() -> None:
    xxx.run()


if __name__ == '__main__':
    main()
