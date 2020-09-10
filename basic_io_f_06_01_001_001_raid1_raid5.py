#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io_f-06-01-001-001
case title: 基础IO-Raid1-Raid5-并行小IO-随机读
test category: Raid1和Raid5并行IO
check point: Raid1-Raid5-并行随机读正常
test platform: 模拟平台&物理平台

author: yuan.liu
date: 2020.09.10
description:
@steps:

1、组建符合条件的VD后进行快速初始化
2、进行IO的vdbench配置：测试时间 elapse=5min，IO并发thread=32，随机比例seekpct=50，
读写比例rdpct=100，xfersize=（1K，127K， 256K， 512K）测试并发随机读，
3、清理环境
@changelog:
"""

import add_syspath
from scripts.system_test.basic_io.basicio_multiple_raid_script_base import BasicioMultipleRaidScriptBase
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum, PdStateEnum
from scripts.script_libs import constants
from scripts.script_libs import enums


class BasicioRaid1_Raid5RandomRead(BasicioMultipleRaidScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
        # 物理盘参数设置
        # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        cls.physical_params_dict['the_same_pd_interface'] = True
        # 测试盘种类列表
        cls.target_list = [
            'RaidLevelEnum.RAID1.value',
            'RaidLevelEnum.RAID5.value']
        # raid盘 物理接口设置
        cls.phy_parameters_dict['the_first_pd_interface'] = PdInterfaceTypeEnum.SATA.value
        # raid盘 物理介质设置
        cls.phy_parameters_dict['the_first_pd_medium'] = PdMediumTypeEnum.HDD.value
        # raid盘 所用的磁盘数量
        cls.phy_parameters_dict['the_first_pd_count'] = 2
        # raid盘 条带大小
        cls.vd_parameters_dict['the_first_vd_strip'] = VDStripSizeEnum.SIZE_256.value

        # raid盘 物理接口设置
        cls.phy_parameters_dict['the_second_pd_interface'] = PdInterfaceTypeEnum.SATA.value
        # raid盘 物理介质设置
        cls.phy_parameters_dict['the_second_pd_medium'] = PdMediumTypeEnum.HDD.value
        # raid盘 所用的磁盘数量
        cls.phy_parameters_dict['the_second_pd_count'] = 4
        # raid盘 条带大小
        cls.vd_parameters_dict['the_second_vd_strip'] = VDStripSizeEnum.SIZE_64.value
        # 测试工具参数设置
        # 是否使用vdbench工具
        cls.vdbench_parameters_dict[constants.VDB_USE] = True
        # 是否进行一致性校验
        cls.vdbench_parameters_dict[constants.VDB_CONSISTENCY_CHECK] = False
        # vdbench运行时间
        cls.vdbench_parameters_dict[constants.VDB_ELAPSED] = '120'
        # vdbench数据块大小
        cls.vdbench_parameters_dict[constants.VDB_XFERSIZE] = '(1K,25,127K,25,256K,25,512K,25)'
        # 读写比例 读：100；写：0
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
    BasicioRaid1_Raid5RandomRead.run()


if __name__ == '__main__':
    main()
