#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number:
case title:
test category:
check point:
test platform: 模拟平台&物理平台

author: yuan.liu
date: 2020.08.28
description:

@steps:

@changelog:
"""

import add_syspath
from scripts.system_test.basic_io.script_base_basicio_multi_object import BasicioMultipleObjectScriptBase
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs.enums import PdStateEnum
from scripts.script_libs import constants
from scripts.script_libs import enums


class xxx(BasicioMultipleObjectScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()
        # # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = ControllerInterfaceEnum.X4.value
        # 脚本所需raid或jbod
        cls.target_list = []
