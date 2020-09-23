#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io_f-06-02-006-001
case title: 基础IO-JBOD-JBOD-小IO-顺序混合读写
test category: 两个JBOD并行IO
check point: JBOD-JBOD并行顺序混合读写正常
test platform: 模拟平台&物理平台

author: yuan.liu
date: 2020.08.22
description:

@steps:
1、组建符合条件的VD后进行快速初始化
2、进行IO的vdbench配置：测试时间 elapse=5min，IO并发thread=32，随机比例seekpct=0，
读写比例rdpct=60，xfersize=（1K，127K， 256K， 512K）测试并发顺序混合读写，
3、进行数据一致性校验
4、清理环境

@changelog:
"""

import add_syspath
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs import constants
from scripts.script_libs import enums
from scripts.system_test.basic_io.basicio_multiple_object_script_base import BasicioMultipleObjectScriptBase


class BasicioJbodJbodSequenceReadWrite(BasicioMultipleObjectScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()
        # # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        # 脚本所需raid或jbod
        cls.target_list = [
            constants.CLI_KEYWORD_JBOD_UPPER,
            constants.CLI_KEYWORD_JBOD_UPPER]
        # 包含jbod信息的字典
        cls.jbod_info = {}

        # 包含jbod信息的字典
        cls.jbod_info = {}

        # jbod的物理盘接口
        cls.jbod_info['pd_interface'] = PdInterfaceTypeEnum.SATA.value
        # jbod的物理盘介质
        cls.jbod_info['pd_medium'] = PdMediumTypeEnum.HDD.value
        # 所需的jbod数量
        cls.jbod_info['pd_count'] = 2
        cls.disk_list.append(cls.jbod_info)

        # 是否使用vdbench工具
        cls.vdb_use = True
        # 是否进行一致性校验
        cls.vdb_consistency_check = True
        # vdbench运行时间
        cls.vdb_elapsed = '120'
        # vdbench数据块大小
        cls.vdb_xfersize = '(1K,25,127K,25,256K,25,512K,25)'
        # 读写比例
        cls.vdb_rdpct = '60'
        # 随机率
        cls.vdb_seekpct = '0'


def main() -> None:
    BasicioJbodJbodSequenceReadWrite.run()


if __name__ == '__main__':
    main()
