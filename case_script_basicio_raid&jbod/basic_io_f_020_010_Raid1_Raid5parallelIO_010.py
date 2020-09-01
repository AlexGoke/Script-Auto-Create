#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io-f-020-010
case title: 基础IO-Raid1-Raid5-并行小IO-顺序写
test category: 两个VD并行IO
check point: 基础IO-Raid1-Raid5-并行小IO-顺序写
test platform: 模拟平台&物理平台

author: liuyuan
date: 2020.08.29
description:
@steps: 1、组建符合条件的VD后进行快速初始化
        2、进行IO的vdbench配置：测试时间 elapse=2min，IO并发thread=32，随机比例seekpct=0，
        读写比例rdpct=0，xfersize=（2K，128K， 256K， 512K）测试并发顺序写，
        3、进行数据一致性校验
        4、清理环境


@changelog:
"""

import add_syspath
from scripts.system_test.basic_io.basicio_multiple_raid_script_base import BasicioMultipleRaidScriptBase


class BasicioRaid1Raid5parallelSequentialWrite(BasicioMultipleRaidScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
        # 物理盘参数设置
        # x2或x4
        cls.phy_parameters_dict['controller_interface'] = 'x4'

        # 测试盘种类列表
        cls.target_list = ['Raid1', 'Raid5']
        # raid盘 物理接口设置
        cls.phy_parameters_dict['the_first_pd_interface'] = 'SATA'
        # raid盘 物理介质设置
        cls.phy_parameters_dict['the_first_pd_medium'] = 'HDD'
        # raid盘 所用的磁盘数量
        cls.phy_parameters_dict['the_first_pd_count'] = 2
        # raid盘 条带大小
        cls.vd_parameters_dict['the_first_vd_strip'] = '256'

        # raid盘 物理接口设置
        cls.phy_parameters_dict['the_second_pd_interface'] = 'SATA'
        # raid盘 物理介质设置
        cls.phy_parameters_dict['the_second_pd_medium'] = 'HDD'
        # raid盘 所用的磁盘数量
        cls.phy_parameters_dict['the_second_pd_count'] = 4
        # raid盘 条带大小
        cls.vd_parameters_dict['the_second_vd_strip'] = '64'

        # 测试工具参数设置
        # 测试工具选择vdbench
        cls.vdbench_parameters_dict['use_vdbench'] = True
        # 测试时长设置
        cls.vdbench_parameters_dict['elapsed'] = '120'
        # 测试数据读写比例设置
        cls.vdbench_parameters_dict['rdpct'] = '0'
        # 测试数据随即比例设置
        cls.vdbench_parameters_dict['seekpct'] = '0'
        # 测试数据块大小及分配设置
        cls.vdbench_parameters_dict['xfersize'] = '(2K,25,128K,25,256K,25,512K,25)'
        # vdbench一致性校验
        cls.vdbench_parameters_dict['consistency_check'] = True
        # 偏移量
        cls.vdbench_parameters_dict['offset'] = None
        # 对齐
        cls.vdbench_parameters_dict['align'] = None
        # 测试区间
        cls.vdbench_parameters_dict['range'] = None


def main() -> None:
    BasicioRaid1Raid5parallelSequentialWrite.run()


if __name__ == '__main__':
    main()
