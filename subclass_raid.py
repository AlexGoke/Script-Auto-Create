"""
description: 针对"raid"测试用例的脚本生成 , 基类为：多vd基类（by liuyuan）
author： alex goke
data: 2020.09.01

"""

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
    def testscene_parameter_set(cls, run_raw_num: int, flist: str, test_scene_info: str) -> None:
        pass


if __name__ == "__main__":
    SingleRaid.run()
