#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
case number: ps3-v1.0.0-basic_io-f-04-02-001-001
case title: 基础IO-SAS-HDD-单一IO满单条带-随机读
test category: SAS-HDD-基础IO
check point: 基础IO-SAS-HDD-单一IO满单条带-随机读
test platform: 模拟平台&物理平台

author: haoran.li
date: 2020.08.22
description:

@steps:
1、组建符合条件的VD后进行快速初始化
2、进行IO的vdbench配置：测试时间 elapse=2min，IO并发thread=32，随机比例seekpct=50，
读写比例rdpct=100，xfersize=192K测试并发随机读
3、清理环境

@changelog:
"""

import add_syspath
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs import constants
from scripts.script_libs import enums
from scripts.system_test.basic_io.basicio_multiple_object_script_base import BasicioMultipleObjectScriptBase


class BasicioSASHDDrandread(BasicioMultipleObjectScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()
        # # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        # 脚本所需raid或jbod
        cls.target_list = [RaidLevelEnum.RAID1.value,
                           RaidLevelEnum.RAID5.value, 'jbod']
        # 包含第1个raid信息的字典
        cls.raid1_info = {}
        # 包含第2个raid信息的字典
        cls.raid5_info = {}
        # 包含jbod信息的字典
        cls.jbod_info = {}

        # 第1个raid的物理盘接口
        cls.raid1_info['pd_interface'] = PdInterfaceTypeEnum.SATA.value
        # 第1个raid的物理盘介质
        cls.raid1_info['pd_medium'] = PdMediumTypeEnum.HDD.value
        # 第1个raid的物理盘数
        cls.raid1_info['pd_count'] = 2
        # 第1个raid的条带大小
        cls.raid1_info['vd_strip'] = VDStripSizeEnum.SIZE_64.value
        # 第1个raid的虚拟盘大小
        cls.raid1_info['vd_size'] = 'all'
        cls.disk_list.append(cls.raid1_info)

        # 第2个raid的物理盘接口
        cls.raid5_info['pd_interface'] = PdInterfaceTypeEnum.SATA.value
        # 第2个raid的物理盘介质
        cls.raid5_info['pd_medium'] = PdMediumTypeEnum.HDD.value
        # 第1个raid的物理盘数
        cls.raid5_info['pd_count'] = 4
        # 第1个raid的条带大小
        cls.raid5_info['vd_strip'] = VDStripSizeEnum.SIZE_64.value
        # 第1个raid的虚拟盘大小
        cls.raid5_info['vd_size'] = 'all'
        cls.disk_list.append(cls.raid5_info)

        jbod的物理盘接口
        cls.jbod_info['pd_interface'] = PdInterfaceTypeEnum.SATA.value
        jbod的物理盘介质
        cls.jbod_info['pd_medium'] = PdMediumTypeEnum.HDD.value
        所需的jbod数量
        cls.jbod_info['pd_count'] = 2
        cls.disk_list.append(cls.jbod_info)

        # 是否使用vdbench工具
        cls.vdb_use = True
        # 是否进行一致性校验
        cls.vdb_consistency_check = None
        # vdbench运行时间
        cls.vdb_elapsed = '120'
        # vdbench数据块大小
        cls.vdb_xfersize = '128K'
        # 读写比例 读：100；写：0
        cls.vdb_rdpct = '100'
        # 随机率
        cls.vdb_seekpct = '50'


def main() -> None:
    BasicioSASHDDrandread.run()


if __name__ == '__main__':
    main()
