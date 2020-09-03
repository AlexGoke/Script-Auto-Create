"""
description: 针对raid jbod混组并行测试用例的脚本生成 , 基类为：混组二级基类(by lihaoran)
author： alex goke
data: 2020.09.01

"""


from script_create import case_script_auto_create


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
        cls.template = 'case_template_vdb_raid&jbod.py'
        # 该类脚本生成需要查找的(测试工具）参数值
        cls.need_parameter = ['rdpct', 'seekpct', 'offset', 'align',
                              'range', 'xfersize']

    @classmethod
    def testscene_parameter_set(cls, run_raw_num: int, flist: str, test_scene_info: str) -> None:
        """
        description:
        """
        # 先确定target_list
        test_scene = test_scene_info.split('\n')
        target_list = []
        reference = ['JBOD', 'Raid1', 'Raid5']
        for i in range(len(reference)):
            if reference[i] in test_scene[2]:
                disk1 = reference[i]
            if reference[i] in test_scene[6]:
                disk2 = reference[i]
        target_list.append(disk1)
        target_list.append(disk2)
        # 为了正确适配基类，对target_list顺序调整一下
        if target_list[0] == 'JBOD' and 'Raid' in target_list[1]:
            target_list[0], target_list[1] = target_list[1], target_list[0]

        target_list_raw_num = [x for x in range(
            run_raw_num, len(cls.flist)) if 'target' in cls.flist[x]][0]
        cls.flist[target_list_raw_num] = '        cls.target_list = {}'.format(
            target_list)

        # 模板信息
        text_1_raid = """
        # raid盘 物理接口设置
        cls.phy_parameters_dict['the_first_pd_interface'] = 'SATA'
        # raid盘 物理介质设置
        cls.phy_parameters_dict['the_first_pd_medium'] = 'HDD'
        # raid盘 所用的磁盘数量
        cls.phy_parameters_dict['the_first_pd_count'] = {}
        # raid盘 条带大小
        cls.vd_parameters_dict['the_first_vd_strip'] = '{}'
        """

        text_2_raid = """
        # raid盘 物理接口设置
        cls.phy_parameters_dict['the_second_pd_interface'] = 'SATA'
        # raid盘 物理介质设置
        cls.phy_parameters_dict['the_second_pd_medium'] = 'HDD'
        # raid盘 所用的磁盘数量
        cls.phy_parameters_dict['the_second_pd_count'] = {}
        # raid盘 条带大小
        cls.vd_parameters_dict['the_second_vd_strip'] = '{}'
        """

        text_1_jbod = """
        # jbod盘 物理接口设置
        cls.phy_parameters_dict['jbod_interface'] = 'SATA'
        # jbod盘 物理介质设置
        cls.phy_parameters_dict['jbod_medium'] = 'HDD'
        # jbod盘 所用的磁盘数量
        cls.phy_parameters_dict['jbod_count'] = {}

        """
        raw_num = target_list_raw_num + 1
        # 确定disk1，disk2的count、stripe
        if target_list[0] == 'JBOD' and target_list[1] == 'JBOD':
            flist.insert(raw_num, text_1_jbod.format('2'))
        elif 'Raid1' == target_list[0] and 'Raid5' == target_list[1]:
            flist.insert(raw_num, text_2_raid.format('4', '64'))
            flist.insert(raw_num, text_1_raid.format('2', '256'))
            # raw_num += len(text_1_raid.split('\n'))
        elif 'Raid5' == target_list[0] and 'JBOD' == target_list[1]:
            flist.insert(raw_num, text_1_jbod.format('1'))
            flist.insert(raw_num, text_1_raid.format('4', '256'))
            # raw_num += len(text_1_raid.split('\n'))


if __name__ == "__main__":
    RaidJbodMixParallel.run()
