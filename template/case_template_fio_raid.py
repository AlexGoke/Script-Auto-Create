#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: raid 测试用例模板 fio
case title:
test category:
check point:
test platform: 模拟平台&物理平台

author: haoran.li
date: 2020.08.24
description:

@steps:

@changelog:
"""

import add_syspath

from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs import constants
from scripts.script_libs import enums
from scripts.system_test.basic_io.basicio_multi_vd_in_DG_script_base import BasicioMultiVDScriptBase


class xxx(BasicioMultiVDScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()
        # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        # 物理盘接口
        cls.physical_params_dict[constants.PD_INTERFACE] = PdInterfaceTypeEnum.SATA.value
        # 物理盘介质
        cls.physical_params_dict[constants.PD_MEDIUM] = PdMediumTypeEnum.SSD.value
        # 组raid所用的磁盘数量
        cls.physical_params_dict[constants.PD_COUNT] = 4

        # 要组建的raid虚拟盘数量
        cls.vd_parameters_dict[constants.VD_COUNT] = 1
        # raid级别
        cls.vd_parameters_dict[constants.VD_TYPE] = RaidLevelEnum.RAID5.value
        # 条带大小
        cls.vd_parameters_dict[constants.VD_STRIP] = VDStripSizeEnum.SIZE_128.value
        # 选择使用fio作为测试工具
        cls.fio_parameters_dict[constants.FIO_USE] = True
        # 执行时间
        cls.fio_parameters_dict[constants.FIO_RUNTIME] = '120'
        # 顺序读read 随机读randread 顺序写write
        cls.fio_parameters_dict[constants.FIO_RW] = None
        # 数据块大小及比例
        cls.fio_parameters_dict[constants.FIO_BSSPLIT] = None
        # 读写比  读所占比例 设置该参数时 rw应为混合模式
        cls.fio_parameters_dict[constants.FIO_RWMIXREAD] = None


def main() -> None:
    xxx.run()


if __name__ == '__main__':
    main()
