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
    def prepara(cls) -> None:
        """
        description:  准备部分，执行基础准备后，再执行针对本类型脚本的部分
        parametr：    None
        return：      None
        """
        super().prepara_base()

        # 1. 输入作者名/时间
        cls.author = 'yuan.liu'
        cls.date = '2020.11.14'
        # 2. 选择 脚本注释信息、import 内容模板
        cls.template = 'case_template_raid.py'
        # 3. 选择 物理盘参数 内容模板
        cls.pd_info = text_template.PHYSICAL_DISK_PARAMETER_RAID
        # 4. 选择 虚拟盘参数 内容模板
        cls.vd_info = text_template.VIRTUAL_DISK_PARAMETER

        # 脚本生成需要查找的（测试工具）参数值
        cls.need_test_tool_para_list = [
            'rdpct', 'seekpct', 'offset', 'align', 'range', 'xfersize']
        # 脚本生成需要查找的（测试场景）参数值
        cls.need_test_scene_para_list = [
            'ctrl_interface', 'pd_interface', 'pd_medium', 'pd_count', 'vd_count', 'vd_type', 'vd_stripe']

    @classmethod
    def testscene_parameter_set(cls, flist: str, test_scene_info: str) -> None:
        text_phy_disk_info = cls.pd_info.format(ctrl_interface='X4',
                                                pd_interface='SAS',
                                                pd_medium='HDD',
                                                pd_count='2')
        text_vir_disk_info = cls.vd_info.format(vd_count='1',
                                                vd_type='RAID0',
                                                vd_strip='128')
        flist.append(text_phy_disk_info)
        flist.append(text_vir_disk_info)

    @classmethod
    def testtool_parameter_set(cls, flist: str, tool_para_dict: dict, tool: str) -> None:
        if tool.lower() == 'v':
            # vdbench格式不统一，在这里自己增删需要的参数
            vdb_text = text_template.VDBENCH_SET.format(
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
    ScriptBuilder.run()
