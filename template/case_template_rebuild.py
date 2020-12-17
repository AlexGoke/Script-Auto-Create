#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io_f-01-02-001-001
case title: 基础IO-IO过程中-局部热备-重建-Raid5-随机读
test category: IO过程中盘重建
check point: IO过程中局部热备盘进入重建状态，Raid5读写正常
test platfrom: 模拟平台&物理平台

author: panpan.du
date: 2020.12.11
description:

@steps:

@changelog
"""

import sys
import add_syspath

from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, \
    VDStripSizeEnum
from scripts.script_libs import constants
from scripts.system_test.basic_io.module_interaction.rebuild.basic_io_module_interaction_rebuild import BasicIORebuild
from scripts.system_test.basic_io.module_interaction.libs import basic_io_module_interaction_constants as bio_constants


class BasicIoRebuildRaid5RandRead(BasicIORebuild):
    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()
