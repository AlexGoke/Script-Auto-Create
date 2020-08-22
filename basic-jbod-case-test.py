#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-base_io-f-001-001    [column: A]
case title: 基础IO-JBOD-多种小IO-随机读        [column: D]
test category: SAS-SSD-基础IO                 [column: J]
check point: 基础IO-JBOD-多种小IO-随机读       [column: K]
test platform: 模拟平台&物理平台
author: liuyuan
date: 2020.08.21
description:基础IO-JBOD-多种小IO-随机读        [column: D]
@steps: 1、组建符合条件的VD后进行快速初始化      [column: N]
        2、进行FIO配置：数据块大小384K，读写比例100，测试并发随机读
        3、清理环境
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
