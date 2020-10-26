#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
case number:
case title:
test category:
check point:
test platform: 物理平台 & 模拟平台

author: yuan.liu
date: 2020.10.26
@steps:

@changelog:
"""

import add_syspath
from scripts.script_libs import constants
from scripts.script_libs.enums import ControllerInterfaceEnum, PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, \
    VDStripSizeEnum
from scripts.system_test.basic_io.script_base_basicio_raid_jbod import BasicioRaidJbodScriptBase


class xxx(BasicioRaidJbodScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()
