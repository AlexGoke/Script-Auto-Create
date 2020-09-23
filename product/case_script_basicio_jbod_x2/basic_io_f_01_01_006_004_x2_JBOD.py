#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io_f-01-01-006-004
case title: 基础IO-JBOD-非对齐模式-顺序混合读写
test category: x2口JBOD
check point: x2口-JBOD顺序混合读写正常
test platform: 模拟平台&物理平台

author: liuyuan
date: 2020.08.24
description:

@steps:
1、组建JBOD
2、进行IO的vdbench配置：偏移量offset=2048，测试时间 elapse=5min，IO并发thread=32，
随机比例seekpct=0，读写比例rdpct=70，xfersize=（1K，64K，128M，256M）测试并发随机读，
3、清理环境

@changelog:
"""

import add_syspath

from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum
from scripts.script_libs import constants
from scripts.script_libs import enums
from scripts.system_test.basic_io.basicio_jbod_script_base import BasicioJBODScriptBase


class BasicioSequenceReadWrite(BasicioJBODScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
        # 物理盘参数设置
        # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.X2.value
        # 物理盘接口
        cls.physical_params_dict[constants.PD_INTERFACE] = enums.PdInterfaceTypeEnum.SATA.value
        # 物理盘介质
        cls.physical_params_dict[constants.PD_MEDIUM] = enums.PdMediumTypeEnum.HDD.value

        # 测试工具参数设置
        # 是否使用vdbench工具
        cls.vdbench_parameters_dict[constants.VDB_USE] = True
        # 是否进行一致性校验
        cls.vdbench_parameters_dict[constants.VDB_CONSISTENCY_CHECK] = False
        # vdbench运行时间
        cls.vdbench_parameters_dict[constants.VDB_ELAPSED] = '120'
        # vdbench数据块大小
        cls.vdbench_parameters_dict[constants.VDB_XFERSIZE] = '(1K,25,64K,25,128M,25,256M,25)'
        # 读写比例 读：100；写：0
        cls.vdbench_parameters_dict[constants.VDB_RDPCT] = '70'
        # LBA地址对齐
        cls.vdbench_parameters_dict[constants.VDB_ALIGN] = None
        # 随机率
        cls.vdbench_parameters_dict[constants.VDB_SEEKPCT] = '0'
        # 范围
        cls.vdbench_parameters_dict[constants.VDB_RANGE] = None
        # 偏移量
        cls.vdbench_parameters_dict[constants.VDB_OFFSET] = '2048'


def main() -> None:
    BasicioSequenceReadWrite.run()


if __name__ == '__main__':
    main()
