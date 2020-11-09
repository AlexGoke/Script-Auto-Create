"""
description: 针对“nvme”测试用例的脚本生成，基类为：script_base_basicio_raid_jbod （by zanzan)
author: liuyuan
date: 2020.10.26
"""

import text_template
from expand_function import FuncSet
from script_create import case_script_auto_create


class NVME(case_script_auto_create):

    @classmethod
    def prepara(cls) -> None:
        """
        """
        super().prepara_base()
        # 该类脚本生成的参照模板文件————选择模板
        cls.template = 'case_template_nvme.py'

        # 该类脚本生成需要查找的（测试工具）参数值
        cls.need_test_tool_para_list = ['rdpct', 'seekpct', 'offset', 'align',
                                        'range', 'xfersize']

    @classmethod
    def testscene_parameter_set(cls, flist: str, test_scene_info: str) -> None:
        text_phy_disk_info = text_template.PHYSICAL_DISK_PARAMETER.format(ctrl_interface='X4',
                                                                          pd_interface='SATA',
                                                                          pd_medium='SSD',
                                                                          pd_count='2')
        text_vir_disk_info = text_template.VIRTUAL_DISK_PARAMETER.format(vd_count='1',
                                                                         vd_type='RAID0',
                                                                         vd_strip='512')
        flist.append(text_phy_disk_info)
        flist.append(text_vir_disk_info)

    @classmethod
    def testtool_parameter_set(cls, flist: str, tool_para_dict: dict, tool: str) -> None:
        if tool.lower() == 'v':
            # 整理格式
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
    NVME.run()