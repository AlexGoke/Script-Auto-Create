"""
测试脚本的各部分模板内容
"""
# ----------------------------------------- 框架 公共部分信息 ---------------------------------------
# 脚本结尾内容
SCRIPT_END = """
def main() -> None:
    {class_name}.run()
if __name__ == '__main__':
    main()
"""

# ----------------------------------------- 测试工具 -----------------------------------------------
# vdbench信息
VDBENCH_SET = """
        # 是否使用vdbench工具
        cls.vdbench_parameters_dict[constants.VDB_USE] = True
        # 是否进行一致性校验
        cls.vdbench_parameters_dict[constants.VDB_CONSISTENCY_CHECK] = {vdbench_cc}
        # vdbench运行时间
        cls.vdbench_parameters_dict[constants.VDB_ELAPSED] = '120'
        # vdbench数据块大小
        cls.vdbench_parameters_dict[constants.VDB_XFERSIZE] = {vdb_xfersize}
        # 读写比例
        cls.vdbench_parameters_dict[constants.VDB_RDPCT] = {vdb_rdpct}
        # LBA地址对齐
        cls.vdbench_parameters_dict[constants.VDB_ALIGN] = {vdb_align}
        # 随机率
        cls.vdbench_parameters_dict[constants.VDB_SEEKPCT] = {vdb_seekpct}
        # 范围
        cls.vdbench_parameters_dict[constants.VDB_RANGE] = {vdb_range}
        # 偏移量
        cls.vdbench_parameters_dict[constants.VDB_OFFSET] = {vdb_offset}
"""

# fio信息
FIO_SET = """
        # fio参数设置
        # 使用fio
        cls.fio_parameters_dict[constants.FIO_USE] = True
        # 执行时间
        cls.fio_parameters_dict[constants.FIO_RUNTIME] = '120'
        # 读写模式
        cls.fio_parameters_dict[constants.FIO_RW] = {fio_rw}
        # 数据块大小及比例
        cls.fio_parameters_dict[constants.FIO_BSSPLIT] = {fio_bssplit}
        # 读写比例
        cls.fio_parameters_dict[constants.FIO_RWMIXREAD] = {fio_rwmixread}
        # 测试数据的随机比
        cls.fio_parameters_dict[constants.FIO_SEEKPCT] = {fio_seekpct}
        # 偏移量 [不常用]
        cls.fio_parameters_dict[constants.FIO_OFFSET] = {fio_offset}
        # 对齐 [不常用]
        cls.fio_parameters_dict[constants.FIO_BLOCKALIGN] = {fio_align}
"""


# ----------------------------------------- 单盘 raid 属性信息 --------------------------------------
# 物理盘信息
PHYSICAL_DISK_PARAMETER = """
        # x2或x4
        cls.physical_params_dict[constants.CTRL_INTERFACE] = enums.ControllerInterfaceEnum.{ctrl_interface}.value
        # 物理盘接口
        cls.physical_params_dict[constants.PD_INTERFACE] = PdInterfaceTypeEnum.{pd_interface}.value
        # 物理盘介质
        cls.physical_params_dict[constants.PD_MEDIUM] = PdMediumTypeEnum.{pd_medium}.value
        # 组raid所用的磁盘数量
        cls.physical_params_dict[constants.PD_COUNT] = {pd_count}
"""

# 虚拟盘信息
VIRTUAL_DISK_PARAMETER = """
        # 要组建的raid虚拟盘数量
        cls.vd_parameters_dict[constants.VD_COUNT] = {vd_count}
        # raid级别
        cls.vd_parameters_dict[constants.VD_TYPE] = RaidLevelEnum.{vd_type}.value
        # 条带大小
        cls.vd_parameters_dict[constants.VD_STRIP] = VDStripSizeEnum.SIZE_{vd_strip}.value
"""


# ---------------------------------------- JBOD 属性信息 -------------------------------------------
# 同 PHYSICAL_DISK_PARAMETER

# ---------------------------------------- 复合raid 属性信息 -------------------------------------------
# 虚拟盘信息
COMPLEX_VIRTUAL_DISK_PARAMETER = """
        # 要组建的raid虚拟盘数量
        cls.vd_parameters_dict[constants.VD_COUNT] = {vd_count}
        # raid级别
        cls.vd_parameters_dict[constants.VD_TYPE] = RaidLevelEnum.{vd_type}.value
        # 条带大小
        cls.vd_parameters_dict[constants.VD_STRIP] = VDStripSizeEnum.SIZE_{vd_strip}.value
        # 子组的盘数
        cls.vd_parameters_dict[constants.VD_PD_PER_ARRAY] = {vd_pdperarray}
"""

# ---------------------------------------- Raid & Jbod混组 测试用例 ---------------------------------
# raid info
RAID_PARAMETER = """
        # {raid_type}的物理盘接口
        cls.{raid_type}_info['pd_interface'] = PdInterfaceTypeEnum.{pd_interface}.value
        # {raid_type}的物理盘介质
        cls.{raid_type}_info['pd_medium'] = PdMediumTypeEnum.{pd_medium}.value
        # {raid_type}的物理盘数
        cls.{raid_type}_info['pd_count'] = {pd_count}
        # {raid_type}的条带大小
        cls.{raid_type}_info['vd_strip'] = VDStripSizeEnum.SIZE_{vd_strip}.value
        # {raid_type}的虚拟盘大小
        cls.{raid_type}_info['vd_size'] = 'all'
        cls.disk_list.append(cls.{raid_type}_info)
"""

# jbod info
JBOD_PARAMETER = """
        # jbod的物理盘接口
        cls.jbod_info['pd_interface'] = PdInterfaceTypeEnum.{pd_interface}.value
        # jbod的物理盘介质
        cls.jbod_info['pd_medium'] = PdMediumTypeEnum.{pd_medium}.value
        # 所需的jbod数量
        cls.jbod_info['pd_count'] = {pd_count}
        cls.disk_list.append(cls.jbod_info)
"""

# vdbench info
RAID_JBOD_MIX_VDBENCH = """
        # 是否使用vdbench工具
        cls.vdb_use = True
        # 是否进行一致性校验
        cls.vdb_consistency_check = {check}
        # vdbench运行时间
        cls.vdb_elapsed = '120'
        # vdbench数据块大小
        cls.vdb_xfersize = '{xfersize}'
        # 读写比例
        cls.vdb_rdpct = '{rdpct}'
        # 随机率
        cls.vdb_seekpct = '{seekpct}'
"""


# --------------------------------------- 工具---------------------------------
