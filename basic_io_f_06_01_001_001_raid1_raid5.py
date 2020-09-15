#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io_f-06-01-001-001
case title: 基础IO-Raid1-Raid5-并行小IO-随机读
test category: Raid1和Raid5并行IO
check point: Raid1-Raid5-并行随机读正常
test platform: 模拟平台&物理平台

author: yuan.liu
date: 2020.08.22
description:

@steps:
1、组建符合条件的VD后进行快速初始化
2、进行IO的vdbench配置：测试时间 elapse=5min，IO并发thread=32，随机比例seekpct=50，
读写比例rdpct=100，xfersize=（1K，127K， 256K， 512K）测试并发随机读，
3、清理环境

@changelog:
"""

import add_syspath
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs import constants
from scripts.script_libs import enums
from scripts.system_test.basic_io.basicio_multiple_object_script_base import BasicioMultipleObjectScriptBase


class aaa(BasicioMultipleObjectScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()
        # # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        # 脚本所需raid或jbod
        cls.target_list = [
            RaidLevelEnum.RAID1.value,
            RaidLevelEnum.RAID5.value]
        # 包含第1个raid1信息的字典
        cls.raid1_info = {}

        # 包含第2个raid5信息的字典
        cls.raid5_info = {}

        # raid1的物理盘接口
        cls.raid1_info['pd_interface'] = PdInterfaceTypeEnum.SATA.value
        # raid1的物理盘介质
        cls.raid1_info['pd_medium'] = PdMediumTypeEnum.HDD.value
        # raid1的物理盘数
        cls.raid1_info['pd_count'] = 2
        # raid1的条带大小
        cls.raid1_info['vd_strip'] = VDStripSizeEnum.SIZE_256.value
        # raid1的虚拟盘大小
        cls.raid1_info['vd_size'] = 'all'
        cls.disk_list.append(cls.raid1_info)

        # raid5的物理盘接口
        cls.raid5_info['pd_interface'] = PdInterfaceTypeEnum.SATA.value
        # raid5的物理盘介质
        cls.raid5_info['pd_medium'] = PdMediumTypeEnum.HDD.value
        # raid5的物理盘数
        cls.raid5_info['pd_count'] = 4
        # raid5的条带大小
        cls.raid5_info['vd_strip'] = VDStripSizeEnum.SIZE_64.value
        # raid5的虚拟盘大小
        cls.raid5_info['vd_size'] = 'all'
        cls.disk_list.append(cls.raid5_info)

        # 是否使用vdbench工具
        cls.vdb_use = True
        # 是否进行一致性校验
        cls.vdb_consistency_check = False
        # vdbench运行时间
        cls.vdb_elapsed = '120'
        # vdbench数据块大小
        cls.vdb_xfersize = '(1K,25,127K,25,256K,25,512K,25)'
        # 读写比例
        cls.vdb_rdpct = '100'
        # 随机率
        cls.vdb_seekpct = '50'


def main() -> None:
    aaa.run()


if __name__ == '__main__':
    main()
