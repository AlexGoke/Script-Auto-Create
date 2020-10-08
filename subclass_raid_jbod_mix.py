"""
description: 针对raid&jbod混组并行测试用例的脚本生成, 基类为：混组二级基类(by lihaoran)
author： alex goke
data: 2020.09.01

"""

import text_template
from script_create import case_script_auto_create
from expand_function import FuncSet


class RaidJbodMixParallel(case_script_auto_create):

    @classmethod
    def prepara(cls) -> None:
        """
        description:  准备部分，执行基础准备后，再执行针对本类型脚本的部分
        parametr：    None
        return：      None
        """
        super().prepara_base()
        # 该类脚本生成的参照模板文件
        cls.template = 'case_template_raid_jbod_mix.py'
        # 该类脚本生成需要查找的(测试工具）参数值
        cls.need_test_tool_para_list = ['rdpct', 'seekpct', 'offset', 'align',
                                        'range', 'xfersize']

    @classmethod
    def testscene_parameter_set(cls, flist: str, test_scene_info: str) -> None:
        """
        description:
        """
        # 先确定target_list ------------------------------------------------------------------
        test_scene = test_scene_info.split('\n')
        target_list = []
        reference = ['JBOD', 'Raid1', 'Raid5']

        for i in range(len(test_scene)):
            for y in reference:
                if y in test_scene[i]:
                    target_list.append(y)

        if target_list[0] == 'JBOD' and 'Raid' in target_list[1]:
            target_list[0], target_list[1] = target_list[1], target_list[0]

        # 找到target_list所在行号
        # target_list_raw_num = [x for x in range(
        #     run_raw_num, len(flist)) if 'target' in flist[x]][0]
        target_list_raw_num = len(flist)-1

        flist[target_list_raw_num] = '        cls.target_list = {}'.format(
            str(target_list))
        print(flist[target_list_raw_num])

        flist[target_list_raw_num] = flist[target_list_raw_num].replace(
            "'JBOD'", 'constants.CLI_KEYWORD_JBOD_UPPER')
        flist[target_list_raw_num] = flist[target_list_raw_num].replace(
            "'Raid1'", 'RaidLevelEnum.RAID1.value')
        flist[target_list_raw_num] = flist[target_list_raw_num].replace(
            "'Raid5'", 'RaidLevelEnum.RAID5.value')

        # 根据target_list声明字典信息 ---------------------------------------------------------
        text_raid_dict = """
        # 包含第%d个%s信息的字典
        cls.%s_info = {}
        """
        text_jbod_dict = """
        # 包含jbod信息的字典
        cls.jbod_info = {}
        """

        raw_num = target_list_raw_num + 1
        for i in range(len(target_list)):
            if 'raid' in target_list[i].lower():
                flist.append(text_raid_dict % (
                    i+1, target_list[i].lower(), target_list[i].lower()))
            if 'jbod' in target_list[i].lower():
                flist.append(text_jbod_dict)
                break

        # 根据target_list, 添加各个盘的信息 -------------------------------------------------------
        for i in range(len(target_list)):
            if 'raid1' in target_list[i].lower():
                flist.append(text_template.RAID_PARAMETER.format(
                    raid_type='raid1', pd_interface='SATA', pd_medium='HDD', pd_count='2', vd_strip='256'))
            elif 'raid5' in target_list[i].lower():
                flist.append(text_template.RAID_PARAMETER.format(
                    raid_type='raid5', pd_interface='SATA', pd_medium='HDD', pd_count='4', vd_strip='64'))
            elif 'jbod' in target_list[i].lower():
                if i == 0:
                    flist.append(text_template.JBOD_PARAMETER.format(
                        pd_interface='SATA', pd_medium='HDD', pd_count='2'))
                    break
                flist.append(text_template.JBOD_PARAMETER.format(
                    pd_interface='SATA', pd_medium='HDD', pd_count='1'))

    @classmethod
    def testtool_parameter_set(cls, flist: str, tool_para_dict: dict, tool: str) -> None:
        if tool.lower() == 'v':
            FuncSet.vdbench_parameter_add(flist, tool_para_dict)
        elif tool.lower() == 'f':
            FuncSet.fio_parameter_add(flist, tool_para_dict)


if __name__ == "__main__":
    RaidJbodMixParallel.run()
