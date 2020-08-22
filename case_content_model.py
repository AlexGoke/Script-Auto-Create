#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: 
case title: 
test category: 
check point: 
test platform: 模拟平台/物理平台/模拟平台&物理平台

author: liuyuan
date: 2020.08.21
description: 
@steps: 1、
        2、
        3、
@changelog:
"""

import add_syspath

from scripts.system_test.basic_io.basicio_jbod_script_base import BasicioJBODScriptBase


class BasicioJbodRandomRead(BasicioJBODScriptBase):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()
        cls.vdbench_parameters_dict['elapsed'] = '30'
        cls.vdbench_parameters_dict['threads'] = '32'
        cls.vdbench_parameters_dict['seekpct'] = '50'
        cls.vdbench_parameters_dict['rdpct'] = '100'
        cls.vdbench_parameters_dict['xfersize'] = '(1k,25,15k,25,31k,25,64k,25)'
        cls.vdbench_parameters_dict['consistency_check'] = False


def main() -> None:
    BasicioJbodRandomRead.run()


if __name__ == '__main__':
    main()
