"""
description: 针对"jbod 单盘"测试用例的脚本生成 , 基类为：jbod基类（by liuyuan）
author： alex goke
data: 2020.09.01

"""

from script_create import case_script_auto_create


class SingleJbod(case_script_auto_create):

    @classmethod
    def prepara(cls) -> None:
        """
        description:  准备部分，执行基础准备后，再执行针对本类型脚本的部分
        parametr：    None
        return：      None
        """
        super().prepara_base()
        # 该类脚本生成的参照模板文件
        cls.template = 'case_template_vdb_jbod.py'
        # 该类脚本生成需要查找的（测试工具）参数值
        cls.need_parameter = ['rdpct', 'seekpct', 'offset', 'align',
                              'range', 'xfersize']

    @classmethod
    def testscene_parameter_set(cls, run_raw_num: int, flist: str, test_scene_info: str) -> None:
        pass


if __name__ == "__main__":
    SingleJbod.run()
