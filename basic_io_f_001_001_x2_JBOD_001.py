#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: ps3-v1.0.0-basic_io-f-001-001
case title: 基础IO-JBOD-多种小IO-随机读
test category: JBOD-基础IO
check point: 基础IO-JBOD-多种小IO-随机读
test platform: 模拟平台/物理平台/模拟平台&物理平台

author: liuyuan
date: 2020.08.24
description: 
        1、组建JBOD
        
        2、进行IO的vdbench配置：测试时间 elapse=5min，IO并发thread=32，随机比例seekpct=50，读写比例rdpct=100，xfersize=（1K，15K，31K，64K）测试并发随机读
        3、清理环境
        
@changelog:
"""
class BasicioJbodRandomRead(BasicioJBODScriptBase):

class 2(BasicioJBODScriptBase):
    def set_parameters(cls):
        super().set_parameters()
        cls.vdbench_parameters_dict['use_vdbench'] = True
        cls.vdbench_parameters_dict['elapsed'] = '30'
        cls.vdbench_parameters_dict['seekpct'] = '50'
        cls.vdbench_parameters_dict['rdpct'] = '100'
        cls.vdbench_parameters_dict['xfersize'] = '(1K，15K，31K，64K)'
        cls.vdbench_parameters_dict['consistency_check'] = False
        # 测试工具选择
        cls.vdbench_parameters_dict['use_vdbench'] = True
        # 测试时长设置
        cls.vdbench_parameters_dict['elapsed'] = '30'
        # 测试数据读写比例设置
        cls.vdbench_parameters_dict['rdpct'] = '100'
        # 测试数据随即比例设置
        cls.vdbench_parameters_dict['seekpct'] = '50'
        # 测试数据块大小及分配设置
        cls.vdbench_parameters_dict['xfersize'] = '(1k,25,15k,25,31k,25,64k,25)'



def main() -> None:
    2.run()

if __name__ == '__main__':
    main()
