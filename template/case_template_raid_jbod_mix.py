#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number:
case title:
test category:
check point:
test platform: 模拟平台&物理平台

author: yuan.liu
date: 2020.08.22
description:

@steps:

@changelog:
"""

import add_syspath
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs import constants
from scripts.script_libs import enums
from scripts.system_test.basic_io.basicio_multiple_object_script_base import BasicioMultipleObjectScriptBase


class xxx(BasicioMultipleObjectScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()
        # # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        # 脚本所需raid或jbod
        cls.target_list = []
