"""
测试脚本的各部分模板内容
"""
# ----------------------------------------- 框架 公共部分信息 字段 ---------------------------------------
# 脚本结尾内容
SCRIPT_END = """

def main() -> None:
    {class_name}.run()


if __name__ == '__main__':
    main()
"""

# ----------------------------------------- 测试工具 字段 【common】-----------------------------------------------
# vdbench信息
VDBENCH_SET = """
        # 是否使用vdbench工具
        cls.vdbench_parameters_dict[constants.VDB_USE] = True
        # 是否进行一致性校验
        cls.vdbench_parameters_dict[constants.VDB_CONSISTENCY_CHECK] = {vdbench_cc}
        # vdbench运行时间
        cls.vdbench_parameters_dict[constants.VDB_ELAPSED] = '120'
        # 线程
        cls.vdbench_parameters_dict[constants.VDB_THREADS] = '32'
        # vdbench数据块大小
        cls.vdbench_parameters_dict[constants.VDB_XFERSIZE] = {vdb_xfersize}
        # 读写比例
        cls.vdbench_parameters_dict[constants.VDB_RDPCT] = {vdb_rdpct}
        # 随机率
        cls.vdbench_parameters_dict[constants.VDB_SEEKPCT] = {vdb_seekpct}
        # LBA地址对齐
        cls.vdbench_parameters_dict[constants.VDB_ALIGN] = {vdb_align}
        # 范围
        cls.vdbench_parameters_dict[constants.VDB_RANGE] = {vdb_range}
        # 偏移量
        cls.vdbench_parameters_dict[constants.VDB_OFFSET] = {vdb_offset}
"""

# fio信息(旧版：模式 + 读写比、随机比)
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

# fio信息(新版：模式 + 读写比、随机比) (目前没用)
FIO_NEW_SET = """
        # fio参数设置
        # 使用fio
        cls.fio_parameters_dict[constants.FIO_USE] = True
        # 执行时间
        cls.fio_parameters_dict[constants.FIO_RUNTIME] = '120'
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

# ----------------------------------------- 单盘 vd 属性信息 【通用，以前的格式】--------------------------------------
# 物理盘信息
PHYSICAL_DISK_PARAMETER_RAID = """
        # x2或x4
        cls.physical_params_dict[constants.CONTROLLER_INTERFACE] = ControllerInterfaceEnum.{ctrl_interface}.value
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
# 写策略
# cls.vd_parameters_dict[constants.VD_WRITE_CACHE] = WriteCacheTypeEnum.WRITE_THROUGH.value


# ---------------------------------------- JBOD 属性信息 【通用，以前的格式】-------------------------------------------
# 同 PHYSICAL_DISK_PARAMETER, 除了多了 passthrough
PHYSICAL_DISK_PARAMETER_JBOD = """
        # x2或x4
        cls.physical_params_dict[constants.CONTROLLER_INTERFACE] = ControllerInterfaceEnum.{ctrl_interface}.value
        # 物理盘接口
        cls.physical_params_dict[constants.PD_INTERFACE] = PdInterfaceTypeEnum.{pd_interface}.value
        # 物理盘介质
        cls.physical_params_dict[constants.PD_MEDIUM] = PdMediumTypeEnum.{pd_medium}.value
        # 组raid所用的磁盘数量
        cls.physical_params_dict[constants.PD_COUNT] = {pd_count}
        # 直通开关
        cls.passthrough = {passthrough}
        # 需要在io过程中改变passthrough的状态
        cls.passthrough_io_switch = {passthrough_switch}
"""

# -------------------------------------------- 物理盘的信息字典 【通用，最新匹配公共库的格式, 规范了excel的书写格式 2021-05 】 --------------------------------------------------
ONE_KIND_PHYSICAL_DISK = """
        physical_params_dict = {
                constants.CONTROLLER_ID: {controller_id}
                constants.CONTROLLER_INTERFACE: {pd_interface}
                constants.PD_COUNT: {pd_count}
                constants.PD_MEDIUM: {pd_medium}}
        global.var.physical_parameters_dict = physical_params_dict
"""
ONE_KIND_PHYSICAL_DISK_COMMIT = """
        cls.physical_params_dict = global.physical_parameters_dict
"""

MULTI_KIND_PHYSICAL_DISK = """
        physical_params_dict{id} = {
                constants.CONTROLLER_ID: {controller_id}
                constants.CONTROLLER_INTERFACE: {pd_interface}
                constants.PD_COUNT: {pd_count}
                constants.PD_MEDIUM: {pd_medium}}
        global.physical_parameters_list.append(physical_params_dict{id}
"""
MULTI_KIND_PHYSICAL_DISK_COMMIT = """
        cls.physical_params_list = global.physical_parameters_list
"""

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
# 混组的参数设置
PARAMETER_RAID = """
        # 物理盘参数设置
        # x2或x4
        cls.physical_params_dict[constants.CONTROLLER_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        cls.the_same_pd_interface = True
        # 测试盘种类列表
        cls.target_list = [
            RaidLevelEnum.{disk1_type}.value,
            RaidLevelEnum.{disk2_type}.value]
        # 包含第1个raid信息的字典
        cls.raid1_info = {{}}
        # 包含第2个raid信息的字典
        cls.raid5_info = {{}}

"""

PARAMETER_JBOD = """
        # x2或x4
        cls.physical_params_dict[constants.CONTROLLER_INTERFACE] = enums.ControllerInterfaceEnum.X4.value
        cls.the_same_pd_interface = True
        # 测试盘种类列表
        cls.target_list = [
            constants.CLI_SHOW_KEYWORD_JBOD,
            constants.CLI_SHOW_KEYWORD_JBOD]
        # 包含jbod信息的字典
        cls.jbod_info = {}
"""

# raid info
RAID_PARAMETER = """
        # {raid_type}的物理盘接口
        cls.{raid_type}_info[constants.PD_INTERFACE] = PdInterfaceTypeEnum.{pd_interface}.value
        # {raid_type}的物理盘介质
        cls.{raid_type}_info[constants.PD_MEDIUM] = PdMediumTypeEnum.{pd_medium}.value
        # {raid_type}的物理盘数
        cls.{raid_type}_info[constants.PD_COUNT] = {pd_count}
        # {raid_type}的条带大小
        cls.{raid_type}_info[constants.VD_STRIP] = VDStripSizeEnum.SIZE_{vd_strip}.value
        # {raid_type}的虚拟盘大小
        cls.{raid_type}_info[constants.VD_SIZE] = 'all'
        cls.disk_list.append(cls.{raid_type}_info)
"""

# jbod info
JBOD_PARAMETER = """
        # jbod的物理盘接口
        cls.jbod_info[constants.PD_INTERFACE] = PdInterfaceTypeEnum.{pd_interface}.value
        # jbod的物理盘介质
        cls.jbod_info[constants.PD_MEDIUM] = PdMediumTypeEnum.{pd_medium}.value
        # 所需的jbod数量
        cls.jbod_info[constants.PD_COUNT] = {pd_count}
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


# --------------------------------------- NVME 测试用例 by zanzan---------------------------------
# 物理盘信息
NVME_PHY_INFO = """
        # 配置pd物理盘参数
        # CTRL_INTERFACE: 端口数量 x4
        # CTRL_ID: 选择控制器的num
        # PD_INTERFACE: 接口类型
        # PD_MEDIUM: 磁盘介质类型
        # PD_COUNT： 配置物理盘数
        cls.physical_params_dict.update({
                constants.CONTROLLER_INTERFACE: ControllerInterfaceEnum.{ctrl_interface}.value,
                constants.CONTROLLER_ID: '0',
                constants.PD_INTERFACE: PdInterfaceTypeEnum.{pd_interface}}.value,
                constants.PD_MEDIUM: PdMediumTypeEnum.{pd_medium}}.value,
                constants.PD_COUNT: {pd_count} })
"""


# 虚拟盘信息
NVME_VIR_INFO = """
        # 配置vd虚拟盘参数
        # VD_COUNT: 要组建的raid虚拟盘数量
        # VD_TYPE: raid模式为{vd_type}
        # VD_STRIP: 条带大小为{vd_strip}k
        cls.vd_parameters_dict.update({
            constants.VD_COUNT: {vd_count},
            constants.VD_TYPE: RaidLevelEnum.{vd_type}}.value,
            constants.VD_STRIP: VDStripSizeEnum.{vd_strip}.value})
"""

# NVME的测试工具 当时赞赞都用了vdbench 先不改了
NVME_TEST_TOOL_INFO = """
        # 配置vdbench参数
        # VDB_RDPCT: 读写比例
        # VDB_RDPCT: 随机比例
        # VDB_XFERSIZE: vdbench数据块大小
        # VDB_USE: 启用vdbench进行测试
        cls.vdbench_parameters_dict.update({constants.VDB_RDPCT: '{rdpct}',
                                            constants.VDB_SEEKPCT: '{seekpct}',
                                            constants.VDB_XFERSIZE: '{xfersize}',
                                            constants.VDB_
                                            constants.VDB_USE: True})
"""

# FIO
NVME_TEST_TOOL_FIO_INFO = """
        # 配置fio参数
        # FIO_USE: 使用FIO进行测试
        # FIO_RUNTIME: FIO进行测试时间
        # FIO_RW: 顺序读read 随机读randread 顺序写write 随机写 randwrite 随机读写 randrw 顺序读写 readwrite,rw
        # FIO_IODEPTH: FIO队列深度
        # FIO_BSSPLIT 数据块大小
        cls.fio_parameters_dict.update({constants.FIO_USE: True,
                                        constants.FIO_RUNTIME: '120',
                                        constants.FIO_RW: '{fio_rw}',
                                        constants.FIO_BSSPLIT: {fio_bssplit}})
"""

# ------------------------------------------------同DG下多VD---------------------------------------------
SAME_DG_MULTI_VD = """
        # x2或x4
        cls.physical_params_dict[
            constants.CONTROLLER_INTERFACE] = ControllerInterfaceEnum.X4.value
        # 物理盘接口
        cls.physical_params_dict[
            constants.PD_INTERFACE] = PdInterfaceTypeEnum.SAS.value
        # 物理盘介质
        cls.physical_params_dict[
            constants.PD_MEDIUM] = PdMediumTypeEnum.HDD.value
        # 组raid所用的物理盘数量
        cls.physical_params_dict[constants.PD_COUNT] = 4
        # 要组建的虚拟盘数量
        cls.vd_parameters_dict[constants.VD_COUNT] = 2
        # 虚拟盘级别
        cls.vd_parameters_dict[constants.VD_TYPE] = RaidLevelEnum.RAID5.value
        # 虚拟盘容量
        cls.vd_parameters_dict[constants.VD_SIZE] = '600GB'
        # 虚拟盘条带大小
        cls.vd_parameters_dict[
            constants.VD_STRIP] = VDStripSizeEnum.SIZE_256.value

"""

# -------------------------------------------- rebuild ----------------------------------------------
# 组建vd
CREATE_VD = """
        # 组建VD使用的物理盘接口
        cls.physical_params_dict[constants.PD_INTERFACE] = PdInterfaceTypeEnum.SAS.value
        # 组建VD使用的物理盘介质
        cls.physical_params_dict[constants.PD_MEDIUM] = PdMediumTypeEnum.HDD.value
        # 组建VD所使用的物理盘数量
        cls.physical_params_dict[constants.PD_COUNT] = {pd_count}
        # 组建VD的数量
        cls.vd_params_dict[constants.VD_COUNT] = 1
        # 组建VD的容量
        cls.vd_params_dict[constants.VD_SIZE] = '10GB'
        # 组建VD的类型
        cls.vd_params_dict[constants.VD_TYPE] = RaidLevelEnum.{vd_type}.value
        # 组建VD的条带块大小
        cls.vd_params_dict[constants.VD_STRIP] = VDStripSizeEnum.SIZE_512.value
"""

VD_DROP_COUNT = """
        # VD掉盘的数量
        cls.vd_params_dict[bio_constants.DROP_PD_COUNT] = 1
        # VD掉盘手段
        cls.vd_params_dict[bio_constants.DROP_PD_MEANS] = bio_constants.DROP_PD_MEANS_SET_OFFLINE
"""

HOTSPARE_COUNT = """
        # 热备盘数量
        cls.spares_params_dict[bio_constants.SPARES_COUNT] = 1
        # 热备盘类型
        cls.spares_params_dict[bio_constants.SPARES_TYPE] = bio_constants.SPARES_TYPE_DHS
        # 热备盘接口
        cls.spares_params_dict[constants.PD_INTERFACE] = PdInterfaceTypeEnum.SAS.value
        # 热备盘介质
        cls.spares_params_dict[constants.PD_MEDIUM] = PdMediumTypeEnum.HDD.value
"""

REBUILD_VDBENCH = """
        # 使用Vdbench工具
        cls.vdbench_params_dict[constants.VDB_USE] = True
        # 随机率
        cls.vdbench_params_dict[constants.VDB_SEEKPCT] = {vdb_seekpct}
        # 读写比例 读：100;写：0
        cls.vdbench_params_dict[constants.VDB_RDPCT] = {vdb_rdpct}
        # 线程
        cls.vdbench_params_dict[constants.VDB_THREADS] = '32'
        # vdbench数据块大小
        cls.vdbench_params_dict[constants.VDB_XFERSIZE] = {vdb_xfersize}
        # vdbench运行时间
        cls.vdbench_params_dict[constants.VDB_ELAPSED] = '120'
        # IO范围
        cls.vdbench_params_dict[constants.VDB_RANGE] = {vdb_range}
        # 不进行一致性校验
        cls.vdbench_params_dict[constants.VDB_CONSISTENCY_CHECK] = {vdbench_cc}
"""
