#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case num: raid 测试用例模板
case title:
test category:
check point:
test platfrom: 模拟平台&物理平台

author:
date:
description:

@steps:

@changelog
"""

import add_syspath
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, \
    VDStripSizeEnum, ControllerInterfaceEnum, WriteCacheTypeEnum
from scripts.script_libs import constants
from scripts.system_test.basic_io.script_base_basicio_vd import BasicioMultiVDScriptBase
from scripts.system_test.basic_io.script_base_basicio_utils import BasicioUtils


class xxx(BasicioMultiVDScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()
