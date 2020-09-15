"""
测试脚本的各部分模板内容
"""
# ----------------------------------------- 框架 公共部分信息 ---------------------------------------
SCRIPT_END = """
def main() -> None:
    {class_name}.run()
if __name__ == '__main__':
    main()
"""
# ----------------------------------------- 单盘 raid 测试用例 --------------------------------------
# ---------------------------------------- Raid & Jbod混组 测试用例 ---------------------------------
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

JBOD_PARAMETER = """
        # jbod的物理盘接口
        cls.jbod_info['pd_interface'] = PdInterfaceTypeEnum.{pd_interface}.value
        # jbod的物理盘介质
        cls.jbod_info['pd_medium'] = PdMediumTypeEnum.{pd_medium}.value
        # 所需的jbod数量
        cls.jbod_info['pd_count'] = {pd_count}
        cls.disk_list.append(cls.jbod_info)
"""
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
