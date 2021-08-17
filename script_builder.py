"""
description: 脚本生成器 <通用>
author： liuyuan
data: 2020.11.13

"""


import logging
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import text_template
from expand_function import FuncSet
from main_frame import case_script_auto_create


class ScriptBuilder(case_script_auto_create):

    pd_info = None
    vd_info = None

    @classmethod
    def __init__(cls):
        logger.info('生成器初始化')
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
        cls.excel_file = '基础IO可靠性-raid全级别-故障处理-v1.0'
        super().prepara_base()

        # 2. 输入作者名/时间
        cls.author = 'liu.yuan'
        cls.date = '2021.08.10'

        # 3. 选择 脚本注释信息、import 内容模板
        cls.template = 'case_template_sencode.py'

        # 4. 选择 物理盘参数 内容模板
        # [2021-05] 统一了脚本格式与公共库字典一致, 规范了excel, 未来都将不变, 适配以后多种pd的场景自动生成. pd信息采取自动筛选与填入并组合内容
        cls.pd_info = text_template.MULTI_KIND_PHYSICAL_DISK

        # 5. 选择 虚拟盘参数 内容模板
        cls.vd_info = text_template.ONE_VIRTUAL_DISK

        # 6. 选择 测试工具参数 内容模板
        cls.io_tool_info = text_template.VDBENCH_SET

        # 脚本生成需要查找的（测试工具）参数值
        cls.need_test_tool_para_list = [
            'rdpct', 'seekpct', 'offset', 'align', 'range', 'xfersize']
        # 脚本生成需要查找的（测试场景）参数值
        cls.need_test_scene_para_list = [
            'ctrl_interface', 'pd_interface', 'pd_medium', 'pd_count', 'vd_count', 'vd_type', 'vd_stripe']
        
    @classmethod
    def testscene_parameter_set(cls, flist: list, scene_para_dict: dict, pd_para_list: list, vd_para_dict: dict) -> None:
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
        # text_phy_disk_info = cls.pd_info.format(ctrl_interface='X4',
        #                                         pd_interface='SAS',
        #                                         pd_medium='HDD',
        #                                         pd_count='6')
        # text_phy_disk_info = cls.pd_info.format()
        # text_vir_disk_info = cls.vd_info.format(vd_count='1',
        #                                         vd_type='RAID50',
        #                                         vd_strip='64',
        #                                         vd_pdperarray='3')
        # flist.append(text_phy_disk_info)
        # flist.append(text_vir_disk_info)

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
        # pd
        if len(pd_para_list) == 1:
            pd_para_dict = dict(pd_para_list[0])
            print(pd_para_dict)
            flist.append(text_template.ONE_KIND_PHYSICAL_DISK.format(
                controller_id=scene_para_dict.get('ctrl_id'),
                controller_interface=scene_para_dict.get('ctrl_interface'),
                pd_interface=pd_para_dict.get('pd_interface'),
                pd_count=pd_para_dict.get('pd_count'),
                pd_medium=pd_para_dict.get('pd_medium')))
            flist.append(text_template.ONE_KIND_PHYSICAL_DISK_COMMIT)
        else:
            for i in range(len(pd_para_list)):
                pd_para_dict = dict(pd_para_list[i])
                print(pd_para_dict)
                flist.append(text_template.MULTI_KIND_PHYSICAL_DISK.format(
                    id=i, controller_id=scene_para_dict.get('ctrl_id'),
                    controller_interface=scene_para_dict.get('ctrl_interface'),
                    pd_interface=pd_para_dict.get('pd_interface'),
                    pd_count=pd_para_dict.get('pd_count'),
                    pd_medium=pd_para_dict.get('pd_medium')))
            flist.append(text_template.MULTI_KIND_PHYSICAL_DISK_COMMIT)

        # vd
        flist.append(text_template.ONE_VIRTUAL_DISK.format(
            vd_count=vd_para_dict.get('count', 1),
            vd_type=vd_para_dict.get('type'),
            vd_size=vd_para_dict.get('size', 'all'),
            vd_strip=vd_para_dict.get('strip'),
            vd_pdperarray=vd_para_dict.get('pdperarray')))

        # 之后删掉 临时用
        logger.info('***临时策略，之后删除***')
        if str(cls.case_title).find('降级读') != -1:
            cls.iotool_para_dict.update({'recovery_data_read': 'True'})
        else:
            cls.iotool_para_dict.update({'recovery_data_read': 'False'})

        left_parenthesis_index = str(cls.case_title).find('(')
        right_parenthesis_index = str(cls.case_title).find(')')
        error_code_info = str(cls.case_title)[left_parenthesis_index+1:right_parenthesis_index]
        if error_code_info.find(',') != -1:
            error_code_info = error_code_info.split(',')
            sense_code = error_code_info[0]
            asc = error_code_info[1]
            ascq = error_code_info[2]
        else:
            sense_code = error_code_info
            asc = '0xff'
            ascq = '0xff'

        if str(cls.case_title).find('后端处理成功') != -1 or str(cls.case_title).find('后端直接反错'):
            between = 1000
        elif str(cls.case_title).find('后端处理失败') != -1:
            between = 0

        text = """
        # 故障参数
        cls.sense_code = '{sense_code}'
        cls.asc = '{asc}'
        cls.ascq = '{ascq}'
        cls.error_between = {between}
"""
        flist.append(text.format(sense_code=sense_code, asc=asc, ascq=ascq, between=between))

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
                prefix='global_var',
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

        else:
            logger.warning('本次生成脚本未选择具体的IO测试工具，尝试使用默认统一的IO信息')
            iotool_text = text_template.IO_DEFAULT_CONFIG.format(
                r_or_w=cls.iotool_para_dict.get('read_or_write'),
                recovery_data_read=cls.iotool_para_dict.get('recovery_data_read'))
            flist.append(iotool_text)
 
if __name__ == "__main__":
    x = ScriptBuilder()
    x.run()
