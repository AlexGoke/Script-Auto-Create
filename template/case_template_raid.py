#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case num: raid 测试用例模板
case title:
test category:
check point:
test platfrom: 模拟平台&物理平台

author: haoran.li
date: 2020.08.28
description:

@steps:

@changelog
"""

import add_syspath

from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, VDStripSizeEnum
from scripts.script_libs import constants
from scripts.script_libs import enums
from scripts.system_test.basic_io.basicio_multi_vd_in_DG_script_base import BasicioMultiVDScriptBase


class xxx(BasicioMultiVDScriptBase):

    @classmethod
    def set_parameters(cls) -> None:
        super().set_parameters()


def main() -> None:
    xxx.run()


if __name__ == '__main__':
    main()
