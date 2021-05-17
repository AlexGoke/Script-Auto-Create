#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
case number: basic_io_f_12_42_001_006
case title: 基础IO复杂场景-x4口-raid0-单线程切换多种控制器配置项-游戏/数据库类数据流-小IO随机读写测试
test category: 复杂场景的基础IO测试
check point: raid0基本读写任务成功，数据一致性校验通过
test platform: 模拟平台&物理平台

author: liu.yuan
date: 2021.5.14
description:

@steps:
1. 检查环境是否有符合条件的盘
2. 创建raid
3. 设置passthrough开关为off
4. 进行IO测试工具的配置：测试时间为20min，IO并发线程数1，seekpct=为100，rdpct=为50，xfersize=设为(1K,9K,33K,64K)，测试小IO随机读写
5. 下发IO任务
6. IO过程中，单线程切换寄存器配置、foreignautoimport开关、修改回迁开关及类型、切换巡读模式、切换热备开关、切换JBOD开关，等待测试结果
7. 删除raid，将passthrough开关恢复到默认状态

@changelog:
"""

import add_syspath
from scripts.script_libs import constants
from scripts.script_libs.enums import PdInterfaceTypeEnum, PdMediumTypeEnum, RaidLevelEnum, \
    VDStripSizeEnum, ControllerInterfaceEnum, WriteCacheTypeEnum
from scripts.system_test.basic_io.raid_hba_card.raid0 import basicio_global_var as global_var
from scripts.system_test.basic_io.raid_hba_card.raid0.basicio_function.basicio_function_base_class.\
    basicio_controller_config_random_switch import ScriptBaseControllerParameterChange


class sadfadsf(ScriptBaseControllerParameterChange):

    @classmethod
    def set_parameters(cls):
        super().set_parameters()

        physical_params_dict0 = {
                constants.CONTROLLER_ID: '0',
                constants.CONTROLLER_INTERFACE: ControllerInterfaceEnum.X4.value,
                constants.PD_COUNT: 1,
                constants.PD_INTERFACE: PdInterfaceTypeEnum.SATA.value,
                constants.PD_MEDIUM: PdMediumTypeEnum.SSD.value}
        global_var.physical_parameters_list.append(physical_params_dict0)

        physical_params_dict1 = {
                constants.CONTROLLER_ID: '0',
                constants.CONTROLLER_INTERFACE: ControllerInterfaceEnum.X4.value,
                constants.PD_COUNT: 1,
                constants.PD_INTERFACE: PdInterfaceTypeEnum.SAS.value,
                constants.PD_MEDIUM: PdMediumTypeEnum.SSD.value}
        global_var.physical_parameters_list.append(physical_params_dict1)

        physical_params_dict2 = {
                constants.CONTROLLER_ID: '0',
                constants.CONTROLLER_INTERFACE: ControllerInterfaceEnum.X4.value,
                constants.PD_COUNT: 1,
                constants.PD_INTERFACE: PdInterfaceTypeEnum.SATA.value,
                constants.PD_MEDIUM: PdMediumTypeEnum.HDD.value}
        global_var.physical_parameters_list.append(physical_params_dict2)

        physical_params_dict3 = {
                constants.CONTROLLER_ID: '0',
                constants.CONTROLLER_INTERFACE: ControllerInterfaceEnum.X4.value,
                constants.PD_COUNT: 1,
                constants.PD_INTERFACE: PdInterfaceTypeEnum.SATA.value,
                constants.PD_MEDIUM: PdMediumTypeEnum.SSD.value}
        global_var.physical_parameters_list.append(physical_params_dict3)

        physical_params_dict4 = {
                constants.CONTROLLER_ID: '0',
                constants.CONTROLLER_INTERFACE: ControllerInterfaceEnum.X4.value,
                constants.PD_COUNT: 1,
                constants.PD_INTERFACE: PdInterfaceTypeEnum.NVME.value,
                constants.PD_MEDIUM: PdMediumTypeEnum.SSD.value}
        global_var.physical_parameters_list.append(physical_params_dict4)

        cls.physical_params_list = global_var.physical_parameters_list

        # 测试目标盘类型 raid
        global_var.target_disk_raid = True
        vd_params_dict = {
                constants.VD_COUNT: 1,
                constants.VD_TYPE: RaidLevelEnum.RAID0.value,
                constants.VD_STRIP: VDStripSizeEnum.SIZE_512.value,
                constants.VD_PD_PER_ARRAY: 0}
        global_var.vd_parameters_dict = vd_params_dict

        # fio参数设置
        # 使用fio
        global_var.fio_parameters_dict[constants.FIO_USE] = True
        # 执行时间
        global_var.fio_parameters_dict[constants.FIO_RUNTIME] = '120'
        # 读写模式
        global_var.fio_parameters_dict[constants.FIO_RW] = 'randrw'
        # 数据块大小及比例
        global_var.fio_parameters_dict[constants.FIO_BSSPLIT] = '1K:9K:33K:64K'
        # 读写比例
        global_var.fio_parameters_dict[constants.FIO_RWMIXREAD] = '50'
        # 测试数据的随机比
        global_var.fio_parameters_dict[constants.FIO_SEEKPCT] = 100
        # 偏移量 [不常用]
        global_var.fio_parameters_dict[constants.FIO_OFFSET] = None
        # 对齐 [不常用]
        global_var.fio_parameters_dict[constants.FIO_BLOCKALIGN] = None


def main() -> None:
    sadfadsf.run()


if __name__ == '__main__':
    main()
