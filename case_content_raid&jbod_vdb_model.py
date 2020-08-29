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


class 自定义(BasicioMultiVDScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
        # 物理盘参数设置
        # x2或x4
        cls.phy_parameters_dict['controller_interface'] = 'x4'

        # 测试盘种类列表
        cls.target_list = ['jbod', 'jbod']
        # raid盘1 物理接口设置
        cls.phy_parameters_dict['the_first_pd_interface'] = 'SATA'
        # raid盘1 物理介质设置
        cls.phy_parameters_dict['the_first_pd_medium'] = 'HDD'
        # raid盘1 所用的磁盘数量
        cls.phy_parameters_dict['the_first_pd_count'] = 4
        # raid盘1 条带大小
        cls.vd_parameters_dict['the_first_vd_strip'] = '256'

        # raid盘2 物理接口设置
        cls.phy_parameters_dict['the_second_pd_interface'] = 'SATA'
        # raid盘2 物理介质设置
        cls.phy_parameters_dict['the_second_pd_medium'] = 'HDD'
        # raid盘2 所用的磁盘数量
        cls.phy_parameters_dict['the_second_pd_count'] = 4
        # raid盘2 条带大小
        cls.vd_parameters_dict['the_second_vd_strip'] = '256'

        # jbod盘 物理接口设置
        cls.phy_parameters_dict['jbod_interface'] = 'SATA'
        # jbod盘 物理介质设置
        cls.phy_parameters_dict['jbod_medium'] = 'SSD'
        # jbod盘 所用的磁盘数量
        cls.phy_parameters_dict['jbod_count'] = 2

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
    自定义.run()


if __name__ == '__main__':
    main()
