"""
description: 针对"raid"测试用例的脚本生成 , 基类为：多vd基类（by liuyuan）
author： alex goke
data: 2020.09.01

"""

import text_template
from script_create import case_script_auto_create


class SingleRaid(case_script_auto_create):

    @classmethod
    def prepara(cls) -> None:
        """
        description:  准备部分，执行基础准备后，再执行针对本类型脚本的部分
        parametr：    None
        return：      None
        """
        super().prepara_base()
        # 该类脚本生成的参照模板文件————选择模板
        # if cls.tool == 'v' or cls.tool == 'vdbench':
        #     cls.template = 'case_template_vdb_raid.py'
        # elif cls.tool == 'f' or cls.tool == 'fio':
        #     cls.template = 'case_template_fio_raid.py'
        cls.template = 'case_template_vdb_raid.py'

        # 该类脚本生成需要查找的（测试工具）参数值
        cls.need_parameter = ['rdpct', 'seekpct', 'offset', 'align',
                              'range', 'xfersize']

    @classmethod
    def testscene_parameter_set(cls, flist: str, test_scene_info: str) -> None:
        text_phy_disk_info = text_template.PHYSICAL_DISK_PARAMETER.format(ctrl_interface='X2',
                                                                          pd_interface='SATA',
                                                                          pd_medium='HDD',
                                                                          pd_count='4')
        text_vir_disk_info = text_template.VIRTUAL_DISK_PARAMETER.format(vd_count='1',
                                                                         vd_type='RAID5',
                                                                         vd_strip='128')
        flist.append(text_phy_disk_info)
        flist.append(text_vir_disk_info)

    @classmethod
    def testtool_parameter_set(cls, flist: str, tool_para_dict: dict, tool: str) -> None:
        if tool.lower() == 'v':
            if ',' in tool_para_dict['xfersize']:
                xfersize = "(%s)" % tool_para_dict['xfersize']
            else:
                xfersize = tool_para_dict['xfersize']
            vdbench_text = text_template.RAID_VDBENCH.format(vdbench_cc=tool_para_dict['vdbench_cc'],
                                                             vdb_xfersize="'{}'".format(
                                                                 xfersize),
                                                             vdb_rdpct="'{}'".format(
                                                                 tool_para_dict['rdpct']) if tool_para_dict['rdpct'] else None,
                                                             vdb_align="'{}K'".format(
                                                                 tool_para_dict['align']) if tool_para_dict['align'] else None,
                                                             vdb_seekpct="'{}'".format(
                                                                 tool_para_dict['seekpct']) if tool_para_dict['seekpct'] else None,
                                                             vdb_range="'{}'".format(
                                                                 tool_para_dict['range']) if tool_para_dict['range'] else None,
                                                             vdb_offset="'{}'".format(tool_para_dict['offset']) if tool_para_dict['offset'] else None)
            flist.append(vdbench_text)
        elif tool.lower() == 'f':
            print('请补全功能，还没添加fio的函数')


if __name__ == "__main__":
    SingleRaid.run()
