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
        cls.template = 'basic_io_f_04_02_001_001_sas_abc.py'
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
        for i in range(len(test_scene)):
            for y in reference:
                if y in test_scene[i]:
                    target_list.append(y)
            # if reference[i] in test_scene[2]:
            #     disk1 = reference[i]
            # if reference[i] in test_scene[7]:
            #     disk2 = reference[i]
        # target_list.append(disk1)
        # target_list.append(disk2)
        # 为了正确适配基类，对target_list顺序调整一下
        if target_list[0] == 'JBOD' and 'Raid' in target_list[1]:
            target_list[0], target_list[1] = target_list[1], target_list[0]

        # 找到target_list所在行号
        target_list_raw_num = [x for x in range(
            run_raw_num, len(flist)) if 'target' in flist[x]][0]

        flist[target_list_raw_num] = '        cls.target_list = {}'.format(
            str(target_list))
        print(flist[target_list_raw_num])

        flist[target_list_raw_num] = flist[target_list_raw_num].replace(
            "'JBOD'", 'constants.CLI_KEYWORD_JBOD_UPPER')
        flist[target_list_raw_num] = flist[target_list_raw_num].replace(
            "'Raid1'", 'RaidLevelEnum.RAID1.value')
        flist[target_list_raw_num] = flist[target_list_raw_num].replace(
            "'Raid5'", 'RaidLevelEnum.RAID5.value')

        # 根据target_list声明字典信息
        text_raid_dict = """        # 包含第{}个raid信息的字典
        cls.{}_info = {}
        """
        text_jbod_dict = """        # 包含jbod信息的字典
        cls.jbod_info = {}
        """

        raw_num = target_list_raw_num + 1
        for i in target_list():
            if 'raid' in i.lower():
                flist.insert(raw_num, text_raid_dict.format(
                    i+1, target_list[i].lower()))
            if 'jbod' in i.lower():
                flist.insert(raw_num, text_jbod_dict)
            raw_num += 2

        # 根据target_list, 添加各个盘的信息
        text_raid1_parameter = """
        # raid1的物理盘接口
        cls.raid1_info['pd_interface'] = PdInterfaceTypeEnum.SATA.value
        # raid1的物理盘介质
        cls.raid1_info['pd_medium'] = PdMediumTypeEnum.HDD.value
        # raid1的物理盘数
        cls.raid1_info['pd_count'] = {}
        # raid1的条带大小
        cls.raid1_info['vd_strip'] = VDStripSizeEnum.SIZE_{}.value
        # raid1的虚拟盘大小
        cls.raid1_info['vd_size'] = 'all'
        cls.disk_list.append(cls.raid1_info)
        """

        text_raid5_parameter = """
        # raid5的物理盘接口
        cls.raid5_info['pd_interface'] = PdInterfaceTypeEnum.SATA.value
        # raid5的物理盘介质
        cls.raid5_info['pd_medium'] = PdMediumTypeEnum.HDD.value
        # raid1的物理盘数
        cls.raid5_info['pd_count'] = {}
        # raid5的条带大小
        cls.raid5_info['vd_strip'] = VDStripSizeEnum.SIZE_{}.value
        # raid5的虚拟盘大小
        cls.raid5_info['vd_size'] = 'all'
        cls.disk_list.append(cls.raid5_info)
        """

        text_jbod_parameter = """
        jbod的物理盘接口
        cls.jbod_info['pd_interface'] = PdInterfaceTypeEnum.SATA.value
        jbod的物理盘介质
        cls.jbod_info['pd_medium'] = PdMediumTypeEnum.HDD.value
        所需的jbod数量
        cls.jbod_info['pd_count'] = {}
        cls.disk_list.append(cls.jbod_info)
        """
        raw_num = target_list_raw_num + 3    # 盘属性部分的起始行号

        for i in range(len(target_list)):
            if 'raid1' in target_list[i].lower():
                flist.insert(raw_num, text_raid1_parameter.format('2', '256'))
                raw_num += len(text_raid_parameter)
            elif 'raid5' in target_list[i].lower():
                flist.insert(raw_num, text_raid5_parameter.format('4', '64'))
                raw_num += len(text_raid5_parameter)
            elif 'jbod' in target_list[i].lower():
                flist.insert(raw_num, text_jbod_parameter('2'))
                raw_num += len(text_jbod_parameter)

        # # 确定disk1，disk2的count、stripe
        # if target_list[0] == 'JBOD' and target_list[1] == 'JBOD':
        #     flist.insert(raw_num, text_1_jbod.format('2'))
        # elif 'Raid1' == target_list[0] and 'Raid5' == target_list[1]:
        #     flist.insert(raw_num, text_2_raid.format('4', '64'))
        #     flist.insert(raw_num, text_1_raid.format('2', '256'))
        #     # raw_num += len(text_1_raid.split('\n'))
        # elif 'Raid5' == target_list[0] and 'JBOD' == target_list[1]:
        #     flist.insert(raw_num, text_1_jbod.format('1'))
        #     flist.insert(raw_num, text_1_raid.format('4', '256'))
        #     # raw_num += len(text_1_raid.split('\n'))


if __name__ == "__main__":
    RaidJbodMixParallel.run()
