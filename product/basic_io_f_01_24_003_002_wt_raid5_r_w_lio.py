#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io_f-01-24-003-002
case title: 基础IO-设置WT-随机写-Raid5-多种大IO
test category: 写策略
check point: WT-随机写正常
test platfrom: 模拟平台&物理平台

author: yuan.liu
date: 2020.11.14
description:

@steps:
1. 清理及准备环境
2. 组建符合条件的VD，VD的写策略为WT：用4块物理盘组raid5
3. 进行IO测试工具的配置：测试时间 2min，IO并发线程数32，数据随即比例seekpct为50，读写比例rdpct为0
数据块大小xfersize设为(1M，4M，10M，256M)测试并发随机写
4. 进行数据一致性校验
5. 清理环境

@changelog
"""

import add_syspath
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, \
    VDStripSizeEnum, ControllerInterfaceEnum, WriteCacheTypeEnum
from scripts.script_libs import constants
from scripts.system_test.basic_io.script_base_basicio_vd import BasicioMultiVDScriptBase
from scripts.system_test.basic_io.script_base_basicio_utils import BasicioUtils


class s(BasicioMultiVDScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()

        # x2或x4
        cls.physical_params_dict[constants.CONTROLLER_INTERFACE] = ControllerInterfaceEnum.X4.value
        # 物理盘接口
        cls.physical_params_dict[constants.PD_INTERFACE] = PdInterfaceTypeEnum.SAS.value
        # 物理盘介质
        cls.physical_params_dict[constants.PD_MEDIUM] = PdMediumTypeEnum.HDD.value
        # 组raid所用的磁盘数量
        cls.physical_params_dict[constants.PD_COUNT] = 2

        # 要组建的raid虚拟盘数量
        cls.vd_parameters_dict[constants.VD_COUNT] = 1
        # raid级别
        cls.vd_parameters_dict[constants.VD_TYPE] = RaidLevelEnum.RAID0.value
        # 条带大小
        cls.vd_parameters_dict[constants.VD_STRIP] = VDStripSizeEnum.SIZE_128.value
        # 写策略
        cls.vd_parameters_dict[constants.VD_WRITE_CACHE] = WriteCacheTypeEnum.WRITE_THROUGH.value

        # fio参数设置
        # 使用fio
        cls.fio_parameters_dict[constants.FIO_USE] = True
        # 执行时间
        cls.fio_parameters_dict[constants.FIO_RUNTIME] = '120'
        # 读写模式
        cls.fio_parameters_dict[constants.FIO_RW] = 'randwrite'
        # 数据块大小及比例
        cls.fio_parameters_dict[constants.FIO_BSSPLIT] = '1M:4M:10M:256M'
        # 读写比例
        cls.fio_parameters_dict[constants.FIO_RWMIXREAD] = '0'
        # 测试数据的随机比
        cls.fio_parameters_dict[constants.FIO_SEEKPCT] = 50
        # 偏移量 [不常用]
        cls.fio_parameters_dict[constants.FIO_OFFSET] = None
        # 对齐 [不常用]
        cls.fio_parameters_dict[constants.FIO_BLOCKALIGN] = None


def main() -> None:
    s.run()


if __name__ == '__main__':
    main()
