#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number:
case title:
test category:
check point:
test platform: 模拟平台&物理平台

author: yuan.liu
date:
description:

@steps:

@changelog:
"""

import add_syspath

from scripts.script_libs import constants
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, \
    VDStripSizeEnum, ControllerInterfaceEnum, WriteCacheTypeEnum
from scripts.system_test.basic_io.basicio_libs import basicio_base_function_global_var as global_var
from scripts.system_test.basic_io.basicio_utils.script_bases.sense_code.script_base_sensecode_stragedy \
    import ScriptBaseSensecodeStragedy


class xxx(ScriptBaseSensecodeStragedy):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
