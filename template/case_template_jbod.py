#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: jbod脚本模板
case title:
test category:
check point:
test platform: 模拟平台&物理平台

author: yuan.liu
date: 2020.09.15
description:

@steps:

@changelog:
"""

import add_syspath
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, ControllerInterfaceEnum
from scripts.script_libs import constants
from scripts.system_test.basic_io.script_base_basicio_jbod import BasicioJBODScriptBase


class xxx(BasicioJBODScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
