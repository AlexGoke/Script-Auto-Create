"""
description: 脚本生成器 <通用>
author： liuyuan
data: 2020.11.13

"""

import text_template
from expand_function import FuncSet
from main_frame import case_script_auto_create


class ScriptBuilder(case_script_auto_create):

    pd_info = None
    vd_info = None

    @classmethod
    def __init__(cls):
        print('生成器初始化')
        # 1. 选择测试用例excel
        # cls.excel_file = '基础IO复杂场景-raid0-在线修改控制器参数-v1.1'  ( 这里好像没用了)

    @classmethod
    def prepare(cls) -> None:
        """
        description:  准备部分，执行基础准备后，再执行针对本类型脚本的部分
        parametr：    None
        return：      None
        """
        # 1. 选择测试用例excel
        cls.excel_file = '基础IO复杂场景-raid0-在线修改控制器参数-v1.1'
        super().prepara_base()

        # 2. 输入作者名/时间
        cls.author = 'liu.yuan'
        cls.date = '2021.5.14'

        # 3. 选择 脚本注释信息、import 内容模板
        cls.template = 'case_template_raid.py'

        # 4. 选择 物理盘参数 内容模板
        # [2021-05] 统一了脚本格式与公共库字典一致, 规范了excel, 未来都将不变, 适配以后多种pd的场景自动生成. pd信息采取自动筛选与填入并组合内容
        cls.pd_info = text_template.ONE_KIND_PHYSICAL_DISK

        # 5. 选择 虚拟盘参数 内容模板
        cls.vd_info = text_template.COMPLEX_VIRTUAL_DISK_PARAMETER

        # 6. 选择 测试工具参数 内容模板
        cls.io_tool_info = text_template.VDBENCH_SET

        # 脚本生成需要查找的（测试工具）参数值
        cls.need_test_tool_para_list = [
            'rdpct', 'seekpct', 'offset', 'align', 'range', 'xfersize']
        # 脚本生成需要查找的（测试场景）参数值
        cls.need_test_scene_para_list = [
            'ctrl_interface', 'pd_interface', 'pd_medium', 'pd_count', 'vd_count', 'vd_type', 'vd_stripe']

    @classmethod
    def testscene_parameter_set(cls, flist: str, scene_para_dict: dict, pd_para_list: list, vd_para_dict: dict) -> None:
        """
        description:  测试场景的参数设置(抽象)——————具体实现, 手动填充参数内容(2021-05开始, 改为自动填充, 需要excel相应的书写格式)
        parametr：    flist：最终生成的脚本内容
                      scene_para_dict : 测试场景信息字典
                      pd_para_list: 所有需要的pd信息列表(元素为dict)
                      vd_para_dict: 测试用例vd信息字典
        return：      None
        """
        """混组"""
        # parameter = text_template.PARAMETER.format(disk1_type='RAID1',
        #                                            disk2_type='RAID5')
        # parameter = text_template.PARAMETER_JBOD
        # flist.append(parameter)
        # flist.append(text_template.RAID_PARAMETER.format(
        #     raid_type='raid1', pd_interface='SAS', pd_medium='HDD', pd_count='2', vd_strip='256'))
        # flist.append(text_template.RAID_PARAMETER.format(
        #     raid_type='raid5', pd_interface='SAS', pd_medium='HDD', pd_count='4', vd_strip='64'))
        # flist.append(text_template.JBOD_PARAMETER.format(
        #     pd_interface='SAS', pd_medium='HDD', pd_count='2'))
        # flist.append('        super().set_parameters()\n')

        """vd"""
        # text_phy_disk_info = cls.pd_info.format(ctrl_interface='X4',
        #                                          pd_interface='SAS',
        #                                          pd_medium='HDD',
        #                                          pd_count='3')
        # text_vir_disk_info=cls.vd_info.format(vd_count='1',
        #                                         vd_type='RAID0',
        #                                         vd_strip='512')
        # flist.append(text_phy_disk_info)
        # flist.append(text_vir_disk_info)

        """complex vd"""
        text_phy_disk_info = cls.pd_info.format(ctrl_interface='X4',
                                                pd_interface='SAS',
                                                pd_medium='HDD',
                                                pd_count='6')
        text_phy_disk_info = cls.pd_info.format()
        text_vir_disk_info = cls.vd_info.format(vd_count='1',
                                                vd_type='RAID50',
                                                vd_strip='64',
                                                vd_pdperarray='3')
        flist.append(text_phy_disk_info)
        flist.append(text_vir_disk_info)

        """同dg"""
        # flist.append(text_template.SAME_DG_MULTI_VD)

        """jbod"""
        # flist.append(text_template.PHYSICAL_DISK_PARAMETER_JBOD.format(ctrl_interface='x2',
        #                                                                pd_interface='SAS',
        #                                                                pd_medium='HDD',
        #                                                                pd_count='1',
        #                                                                passthrough=False,
        #                                                                passthrough_switch=False))

        """rebuild"""
        # flist.append(text_template.CREATE_VD.format(
        #     pd_count='7', vd_type='RAID10'))
        # flist.append(text_template.VD_DROP_COUNT)
        # flist.append(text_template.HOTSPARE_COUNT)

        """2021.05 格式统一、自动填充内容"""
        for i in range(len(pd_para_list)):


    @classmethod
    def testtool_parameter_set(cls, flist: str, tool_para_dict: dict, tool: str) -> None:
        """
        description:  测试工具的参数设置(抽象)———————具体实现
        parameter:  flist:           脚本内容缓存
                    tool_para_didt:  测试工具相关参数字典
                    tool:            测试工具名称
        return：    None
        """
        if tool.lower() == 'v':
            # vdbench格式不统一，在这里自己增删需要的参数
            vdb_text = cls.io_tool_info.format(
                vdbench_cc=tool_para_dict['vdbench_cc'],
                vdb_xfersize="'{}'".format(tool_para_dict['xfersize']),
                vdb_rdpct="'{}'".format(
                    tool_para_dict['rdpct']) if tool_para_dict['rdpct'] != None else None,
                vdb_align="'{}K'".format(
                    tool_para_dict['align']) if tool_para_dict['align'] != None else None,
                vdb_seekpct="'{}'".format(
                    tool_para_dict['seekpct']) if tool_para_dict['seekpct'] != None else None,
                vdb_range="'{}'".format(
                    tool_para_dict['range']) if tool_para_dict['range'] != None else None,
                vdb_offset="'{}'".format(
                    tool_para_dict['offset']) if tool_para_dict['offset'] != None else None)
            flist.append(vdb_text)

        elif tool.lower() == 'f':
            FuncSet.fio_parameter_add(flist, tool_para_dict)


if __name__ == "__main__":
    x = ScriptBuilder()
    x.run()
