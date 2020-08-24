#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io-f-001-002
case title: 基础IO-JBOD-多种大IO-随机读
test category: JBOD-基础IO
check point: 基础IO-JBOD-多种大IO-随机读
test platform: 模拟平台/物理平台/模拟平台&物理平台

author: liuyuan
date: 2020.08.24
description: 
    1、组建JBOD
    2、进行IO的vdbench配置：测试时间 elapse=5min，IO并发thread=32，随机比例seekpct=50，读写比例rdpct=100，xfersize=（10M，64M，128M，256M）测试并发随机读
    3、清理环境
@changelog:
"""

import add_syspath

from scripts.system_test.basic_io.basicio_jbod_script_base import BasicioJBODScriptBase


class BasicioJbodRandomRead(BasicioJBODScriptBase):

class BasicIORandomRead(BasicioJBODScriptBase):
    def set_parameters(cls):
        super().set_parameters()
        cls.vdbench_parameters_dict['use_vdbench'] = True
        cls.vdbench_parameters_dict['elapsed'] = '30'
        cls.vdbench_parameters_dict['seekpct'] = '50'
        cls.vdbench_parameters_dict['rdpct'] = '100'
        cls.vdbench_parameters_dict['xfersize'] = '(10M，64M，128M，256M)'
        cls.vdbench_parameters_dict['consistency_check'] = False


def main() -> None:
    BasicIORandomRead.run()

if __name__ == '__main__':
    main()
