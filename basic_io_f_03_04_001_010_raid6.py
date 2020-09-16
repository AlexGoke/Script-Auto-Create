#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io_f-03-04-002-010
case title: 基础IO-raid6-条带对齐模式-顺序读
test category: Raid6
check point: Raid6顺序读正常
test platfrom: 模拟平台&物理平台

author: haoran.li
date: 2020.08.28
description:

@steps:
1、组建符合条件的VD后进行快速初始化
2、进行IO的vdbench配置：对齐align = 128K  测试时间 elapse=5min，IO并发thread=32，
随机比例seekpct=0，读写比例rdpct=100，xfersize=（128K，1024K，4096K，8192K）测试并发顺序读，
3、清理环境
@changelog
"""

import add_syspath

from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs import constants
from scripts.script_libs import enums
from scripts.system_test.basic_io.basicio_multi_vd_in_DG_script_base import BasicioMultiVDScriptBase


class BasicioRaid6SequenceRead(BasicioMultiVDScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()

        # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        # 物理盘接口
        cls.physical_params_dict[constants.PD_INTERFACE] = PdInterfaceTypeEnum.SATA.value
        # 物理盘介质
        cls.physical_params_dict[constants.PD_MEDIUM] = PdMediumTypeEnum.HDD.value
        # 组raid所用的磁盘数量
        cls.physical_params_dict[constants.PD_COUNT] = 4

        # 要组建的raid虚拟盘数量
        cls.vd_parameters_dict[constants.VD_COUNT] = 1
        # raid级别
        cls.vd_parameters_dict[constants.VD_TYPE] = RaidLevelEnum.RAID6.value
        # 条带大小
        cls.vd_parameters_dict[constants.VD_STRIP] = VDStripSizeEnum.SIZE_64.value

        # 是否使用vdbench工具
        cls.vdbench_parameters_dict[constants.VDB_USE] = True
        # 是否进行一致性校验
        cls.vdbench_parameters_dict[constants.VDB_CONSISTENCY_CHECK] = False
        # vdbench运行时间
        cls.vdbench_parameters_dict[constants.VDB_ELAPSED] = '120'
        # vdbench数据块大小
        cls.vdbench_parameters_dict[constants.VDB_XFERSIZE] = '(128K,25,1024K,25,4096K,25,8192K,25)'
        # 读写比例
        cls.vdbench_parameters_dict[constants.VDB_RDPCT] = '100'
        # LBA地址对齐
        cls.vdbench_parameters_dict[constants.VDB_ALIGN] = '128K'
        # 随机率
        cls.vdbench_parameters_dict[constants.VDB_SEEKPCT] = None
        # 范围
        cls.vdbench_parameters_dict[constants.VDB_RANGE] = None
        # 偏移量
        cls.vdbench_parameters_dict[constants.VDB_OFFSET] = None


def main() -> None:
    BasicioRaid6SequenceRead.run()


if __name__ == '__main__':
    main()
