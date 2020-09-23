#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io_f-13-01-001-001
case title: 基础IO-硬盘粒度为512N-随机读-Raid5小IO
test category: 硬盘为512N粒度
check point: 随机读正常
test platfrom: 模拟平台&物理平台

author: yuan.liu
date: 2020.09.16
description:

@steps:
1、组建符合条件的VD后进行快速初始化
2、进行IO的vdbench配置：测试时间 elapse=5min，IO并发thread=32，随机比例seekpct=50，
读写比例rdpct=100，xfersize=（1K，127K， 256K， 512K）测试并发随机读，
3、清理环境


@changelog
"""

import add_syspath

from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs import constants
from scripts.script_libs import enums
from scripts.system_test.basic_io.basicio_vd_script_base import BasicioMultiVDScriptBase


class qqq(BasicioMultiVDScriptBase):

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
        cls.vd_parameters_dict[constants.VD_STRIP] = VDStripSizeEnum.SIZE_128.value

        # 是否使用vdbench工具
        cls.vdbench_parameters_dict[constants.VDB_USE] = True
        # 是否进行一致性校验
        cls.vdbench_parameters_dict[constants.VDB_CONSISTENCY_CHECK] = False
        # vdbench运行时间
        cls.vdbench_parameters_dict[constants.VDB_ELAPSED] = '120'
        # vdbench数据块大小
        cls.vdbench_parameters_dict[constants.VDB_XFERSIZE] = '(1K,127K,256K,512K,25)'
        # 读写比例
        cls.vdbench_parameters_dict[constants.VDB_RDPCT] = '100'
        # LBA地址对齐
        cls.vdbench_parameters_dict[constants.VDB_ALIGN] = None
        # 随机率
        cls.vdbench_parameters_dict[constants.VDB_SEEKPCT] = '50'
        # 范围
        cls.vdbench_parameters_dict[constants.VDB_RANGE] = None
        # 偏移量
        cls.vdbench_parameters_dict[constants.VDB_OFFSET] = None


def main() -> None:
    qqq.run()


if __name__ == '__main__':
    main()