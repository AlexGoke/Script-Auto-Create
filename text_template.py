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


# ----------------------------------------- 单盘 raid 测试用例 --------------------------------------
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

# vdbench信息
RAID_VDBENCH = """
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
