#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: raid & jbod 混合 并行读/写/读写 vdbench 测试用例模板
case title:
test category:
check point:
test platform: 模拟平台&物理平台

author: liuyuan
date: 2020.09.10
description:
@steps:

@changelog:
"""

import add_syspath
from scripts.system_test.basic_io.basicio_multiple_raid_script_base import BasicioMultipleRaidScriptBase
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum, PdStateEnum
from scripts.script_libs import constants
from scripts.script_libs import enums


class xxx(BasicioMultipleRaidScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
        # 物理盘参数设置
        # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        cls.physical_params_dict['the_same_pd_interface'] = True
        # 测试盘种类列表
        cls.target_list = []
        # 测试工具参数设置
        # 是否使用vdbench工具
        cls.vdbench_parameters_dict[constants.VDB_USE] = True
        # 是否进行一致性校验
        cls.vdbench_parameters_dict[constants.VDB_CONSISTENCY_CHECK] = None
        # vdbench运行时间
        cls.vdbench_parameters_dict[constants.VDB_ELAPSED] = '120'
        # vdbench数据块大小
        cls.vdbench_parameters_dict[constants.VDB_XFERSIZE] = None
        # 读写比例 读：100；写：0
        cls.vdbench_parameters_dict[constants.VDB_RDPCT] = None
        # LBA地址对齐
        cls.vdbench_parameters_dict[constants.VDB_ALIGN] = None
        # 随机率
        cls.vdbench_parameters_dict[constants.VDB_SEEKPCT] = None
        # 范围
        cls.vdbench_parameters_dict[constants.VDB_RANGE] = None
        # 偏移量
        cls.vdbench_parameters_dict[constants.VDB_OFFSET] = None


def main() -> None:
    xxx.run()


if __name__ == '__main__':
    main()
