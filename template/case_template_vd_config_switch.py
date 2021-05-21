#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: raid-hba-card 控制器开关/vd开关切换 复杂场景
case title:
test category:
check point:
test platform: 模拟平台&物理平台

author: yuan.liu
date: 2020.11.09
description:

@steps:

@changelog:
"""

import add_syspath
from scripts.script_libs import constants
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, \
    VDStripSizeEnum, ControllerInterfaceEnum, WriteCacheTypeEnum
from scripts.system_test.basic_io.raid_hba_card.raid0 import basicio_global_var as global_var
from scripts.system_test.basic_io.raid_hba_card.raid0.basicio_function.basicio_function_base_class.\
    basicio_vd_parameters_concurrence_switch_reverse import ScriptBaseVDParameterChange


class xxx(ScriptBaseVDParameterChange):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
