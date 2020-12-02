#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number:
case title:
test category:
check point:
test platform: 模拟平台&物理平台

author:
date:
description:

@steps:

@changelog:
"""

import add_syspath
from scripts.system_test.basic_io.script_base_basicio_multi_object import BasicioMultiObjectScriptBase
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs.enums import PdStateEnum, ControllerInterfaceEnum
from scripts.script_libs import constants
from scripts.script_libs import enums


class xxx(BasicioMultiObjectScriptBase):

    @classmethod
    def set_parameters(cls) -> None:

