"""
author: liuyuan
date: 2020.08.25
description: 自动脚本生成工具 扩展功能类
"""

import enum
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import subprocess
import text_template


class FuncSet(object):

    def __init__(self):
        pass

    # 从用例的 测试场景test_scene 获取测试用例要求的 pd/vd 参数信息
    # [2021.11.14] 当前格式太乱了，没法写，单盘的还行，多盘的简直了。。。。
    # [2021.05.14] 开始实现这一块逻辑, 已将excel的格式做出规范
    @classmethod
    def find_scene_parameter(cls, test_scene_content: str, parameter: list) -> dict:
        """
        @description  : 从用例的测试场景信息中获取用例要求的 测试盘 参数信息, 装入一个字典
                        # 1. 筛选环境信息：控制器id、X2/4口
                        # 2. 筛选物理盘的种类、个数
                        # 3. 筛选raid的type、count、size、strip
                        # 4. [待实现] IO参数可能以后也挪到这里。
        ---------
        @param  :    test_scene_content: 按行切分侯的测试场景信息
                     parameter:   需要查找的参数名称列表（生成器子类传入） 可能用不到了。。。。
        -------
        @Returns  :  环境信息dict、物理盘信息list、虚拟盘信息dict、IO信息dict
        -------
        """
        # 1. 筛选环境信息：控制器id、X2/4口
        scene_info_dict_res = {}
        environment_info = test_scene_content[0]
        scene_info_dict_res['ctrl_id'] = "'0'"    # excel中没有设置的话，默认为0
        if 'X2' in environment_info or 'x2' in environment_info:
            scene_info_dict_res['ctrl_interface'] = 'X2'
        elif 'X4' in environment_info or 'x4' in environment_info:
            scene_info_dict_res['ctrl_interface'] = 'X4'

        # 2. 筛选物理盘的种类、个数
        pd_info_dict_list = []
        pd_info = test_scene_content[1].replace('X', 'x').split('.')[1].split(';')
        logger.info(pd_info)
        for one_kind_pd in pd_info:
            pd_info_dict_res = {}
            one_kind_pd = one_kind_pd.strip()
            pd_info_dict_res['pd_interface'] = one_kind_pd.split('x')[0].split('_')[0].upper()
            pd_info_dict_res['pd_medium'] = one_kind_pd.split('x')[0].split('_')[1].upper()
            pd_info_dict_res['pd_count'] = one_kind_pd.split('x')[1]
            logger.info(pd_info_dict_res)
            pd_info_dict_list.append(pd_info_dict_res)
        logger.info(pd_info_dict_list)

        # 3. 筛选raid的type、count、size、strip
        vd_info_dict_res = {}
        vd_search_parameters_list = ['type', 'count', 'size', 'strip', 'pdperarray']
        vd_info = test_scene_content[2].split(' ')
        logger.info(vd_info)
        for unit in vd_info:
            equal_symbol_index = unit.find('=')
            key = unit[:equal_symbol_index]
            value = unit[equal_symbol_index+1:]
            if key == 'strip':    # strip在excel中有单位k, 这里去掉只留数字
                value = value.split('k')[0]
            if key == 'type':
                value = value.upper()
            if key in vd_search_parameters_list:
                vd_info_dict_res.update({key: value})
        logger.info(vd_info_dict_res)

        # 4. [待实现] IO参数可能以后也挪到这里。
        io_info = test_scene_content[3]
        io_info_dict = {}
        # logger.info(io_info+' 暂时没有将IO参数信息放在这里做自动获取')
        if '读' in io_info:
            io_info_dict.update({'read_or_write': 'read'})
        elif '写' in io_info:
            io_info_dict.update({'read_or_write': 'write'})

        return (scene_info_dict_res, pd_info_dict_list, vd_info_dict_res, io_info_dict)

    # 从用例的 操作步骤step_content 获取测试用例要求的 vdbench/fio 参数信息
    @classmethod
    def find_tool_parameter(cls, step_content: str, parameter: list, tool: str, case_title: str) -> dict:
        """
        @description  : 从测试用例的操作步骤信息中，获取测试工具需要设置的参数的数值
        ---------
        @param  ：  step_content： 按行切分后的操作步骤信息
                       parameter:  需要查找的参数名称列表(生成器子类传入)
                            tool:  测试工具名称
                      case_title:  测试用例标题
        -------
        @Returns  : 想要查找的参数 对应的的名称-值字典
        -------
        """
        res = {}
        # 因为测试用例excel中都是用的vdbench及其相关名词，所以搜索信息还是用vdbench的相关名词
        for x in range(len(parameter)):
            # 由于当前测试用例excel中测试工具都写的是vdbench，所以数据块都用的xfersize
            # 统一都用xfersize代表测试数据块大小
            if parameter[x] == 'xfersize' or parameter[x] == '块大小':    # xfersize 特殊处理
                index = step_content.find('xfersize')
                res[parameter[x]] = cls.find_test_data_block(
                    step_content[index:], tool)
                continue
            if parameter[x] == 'range':     # range 特殊处理
                index = step_content.find('range')
                res[parameter[x]] = cls.find_test_range(
                    step_content[index:index+20])
                continue
            parameter_index = step_content.find(parameter[x])    # 其他参数 统一处理
            num_str = ''
            if parameter_index != -1:
                for i in range(parameter_index+len(parameter), parameter_index+len(parameter)+6):
                    if step_content[i].isdigit():
                        num_str += step_content[i]
                res[parameter[x]] = int(num_str)
            else:
                res[parameter[x]] = None

        # 根据不同的测试工具，改变tool_para_dict中的部分参数值的格式
        if tool == 'v' or tool == 'vdbench':
            vdbench_cc = FuncSet.need_vdbench_cc(
                case_title, res['offset'], res['align'])
            res['vdbench_cc'] = vdbench_cc
            logger.info('vdbench一致性校验：{}'.format(vdbench_cc))
            # if ',' in res['xfersize']:
            #     res['xfersize'] = "(%s)" % res['xfersize']
            # else:
            #     res['xfersize'] = res['xfersize']
            res['xfersize'] = "(%s)" % res['xfersize'] if ',' in res['xfersize'] else res['xfersize']
        elif tool == 'f' or tool == 'fio':
            fio_rw = FuncSet.find_fio_rw(case_title)
            res['fio_rw'] = fio_rw
            # FuncSet.fio_parameter_set(raw_num, flist, tool_para_dict, fio_rw)
        return res

    # 获取vdbench/fio 数据块参数
    @staticmethod
    def find_test_data_block(step_content: str, tool: str) -> str:
        """
        @description  : 在测试用例的操作步骤信息中，获取vdbench/fio的测试数据块数值。测试用例中写的都是
                        vdbench及xfersize，所以搜索方法只需要搜索xfersize就可以
                        根据不同tool，调整为xfersize/bssplit不同格式
        ---------
        @param  :   step_content: 按行切分后的操作步骤信息
                    tool: 该测试用例 选用的测试工具名称
        -------
        @Returns : 该测试工具设置的数据块值
        -------
        """
        step_content = step_content.replace('（', '(')
        step_content = step_content.replace('）', ')')
        index1 = step_content.find('(')
        index2 = step_content.find(')')
        res = None
        # 数据块是多个值的情况
        if index1 != -1 and index2 != -1:
            res = step_content[index1+1:index2]
            res = res.replace(' ', '')
            if '，' in res:
                res = res.replace('，', ',')
            if tool == 'vdbench' or tool == 'v':
                res = res.replace(',', ',25,')
                return res+',25'
            elif tool == 'fio' or tool == 'f':
                res = res.replace(',', ':')
        # 数据块是单一值的情况
        else:
            xfersize_index = step_content.find('xfersize')
            if xfersize_index == -1:
                xfersize_index = step_content.find('块大小')
            num_str = ''
            if xfersize_index != -1:
                for i in range(xfersize_index+len('xfersize')+1, xfersize_index+len('xfersize')+7):
                    if step_content[i].isdigit():
                        num_str += step_content[i]
                res = num_str+'k'
        return res

    # 获取vdbench/fio 数据块参数
    @staticmethod
    def find_test_range(step_content: str) -> str:
        """
        @description  : 在测试用例的操作步骤信息中，获取vdbench的测试范围数值。
                        测试用例中写为range
        ---------
        @param  :   step_content: 按行切分后的操作步骤信息
        -------
        @Returns : 该测试工具设置的数据块值
        -------
        """
        step_content = step_content.replace('（', '(')
        step_content = step_content.replace('）', ')')
        index1 = step_content.find('(')
        index2 = step_content.find(')')
        res = None
        if index1 != -1 and index2 != -1:
            res = step_content[index1:index2+1]
            res = res.replace(' ', '')
            if '，' in res:
                res = res.replace('，', ',')
        return res

    # 获取vdbench是否需要一致性校验
    @staticmethod
    def need_vdbench_cc(case_title: str, offset: int, align: int) -> bool:
        """
        @description  : 该测试用例vdbench是否需要一致性校验
        ---------
        @param  : case_title: 测试用例标题
        -------
        @Returns  : true需要cc；false不需要cc
        -------
        """
        vdbench_cc = False
        if '写' in case_title and not offset and not align:
            vdbench_cc = True
        return vdbench_cc

    # 获取fio的 读写模式(rw) 设置参数
    @staticmethod
    def find_fio_rw(case_title: str) -> str:
        """
        @description  : fio工具需要设置的读写模式
        ---------
        @param  : case_title: 测试用例标题
        -------
        @Returns  : 读写模式的参数值
        -------
        """
        if '顺序' in case_title and '读写' in case_title:
            return 'rw'
        elif '随机' in case_title and '读写' in case_title:
            return 'randrw'
        elif '顺序读' in case_title:
            return 'read'
        elif '随机读' in case_title:
            return 'randread'
        elif '顺序写' in case_title:
            return 'write'
        elif '随机写' in case_title:
            return 'randwrite'
        else:
            pass

    # vdbench工具参数设置————内容中替换[脚本字段] 【弃用】
    @staticmethod
    def vdbench_parameter_set(raw_num: int, flist: str, tool_para_dict: dict, vdbench_cc: bool) -> None:
        """
        @description  : 测试用例脚本中vdbench参数设置字段填充
        ---------
        @param  : raw_num: 起始行号
                flist： 脚本内容字段缓存
                tool_para_dict: 参数字典
                vdbench_cc: vdbench是否需要一致性判断
        -------
        @Returns  : 空
        -------
        """
        for i in range(raw_num, len(flist)):
            # if 'use' in flist[i]:
            #    flist[i] = "        cls.vdbench_parameters_dict['use_vdbench'] = {}\n".format(True)
            if 'RDPCT' in flist[i]:
                flist[i] = flist[i].replace('None', "'{}'".format(
                    tool_para_dict['rdpct']))
                # flist[i] = "        cls.vdbench_parameters_dict['rdpct'] = '{}'\n".format(
                #     tool_para_dict['rdpct'])
            elif 'SEEKPCT' in flist[i]:
                flist[i] = flist[i].replace('None', "'{}'".format(
                    tool_para_dict['seekpct']))
                # flist[i] = "        cls.vdbench_parameters_dict['seekpct'] = '{}'\n".format(
                #     tool_para_dict['seekpct'])
            elif 'XFERSIZE' in flist[i]:
                if ',' in tool_para_dict['xfersize']:
                    flist[i] = flist[i].replace('None', "'({})'".format(
                        tool_para_dict['xfersize']))
                    # flist[i] = "        cls.vdbench_parameters_dict['xfersize'] = '({})'\n".format(
                    #     tool_para_dict['xfersize'])
                else:
                    flist[i] = flist[i].replace('None', "'{}'".format(
                        tool_para_dict['xfersize']))
                    # flist[i] = "        cls.vdbench_parameters_dict['xfersize'] = '{}'\n".format(
                    #     tool_para_dict['xfersize'])
            elif 'CHECK' in flist[i]:
                flist[i] = flist[i].replace('None', "{}".format(vdbench_cc))
                # flist[i] = "        cls.vdbench_parameters_dict['consistency_check'] = {}\n".format(
                #     vdbench_cc)
            elif tool_para_dict['offset'] and 'OFFSET' in flist[i]:
                flist[i] = flist[i].replace('None', "'{}'".format(
                    tool_para_dict['offset']))
                # flist[i] = "        cls.vdbench_parameters_dict['offset'] = '{}'\n".format(
                #     tool_para_dict['offset'])
            elif tool_para_dict['align'] and 'ALIGN' in flist[i]:
                flist[i] = flist[i].replace('None', "'{}K'".format(
                    tool_para_dict['align']))
                # flist[i] = "        cls.vdbench_parameters_dict['align'] = '{}K'\n".format(
                #     tool_para_dict['align'])

    @staticmethod
    # fio工具参数设置————内容中替换[脚本字段] 【弃用】
    def fio_parameter_set(raw_num: int, flist: str, tool_para_dict: dict, fio_rw: str) -> None:
        """
        @description  : 测试用例脚本中fio参数设置字段填充
        ---------
        @param  : raw_num: 起始行号
                flist： 脚本内容字段缓存
                tool_para_dict: 参数字典
                fio_rw: fio读写模式
        -------
        @Returns  : 空
        -------
        """
        for i in range(raw_num, len(flist)):
            # if 'USE' in flist[i]:
            #     flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_USE.value] = {}\n".format(True)
            if 'RWMIXREAD' in flist[i]:
                flist[i] = flist[i].replace('None', "'{}'".format(
                    tool_para_dict['rdpct']))
            elif 'RW' in flist[i]:
                flist[i] = flist[i].replace('None', "'{}'".format(fio_rw))
                # flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_RW.value] = '{}'\n".format(
                #     fio_rw)
            elif 'BSSPLIT' in flist[i]:
                if ':' in tool_para_dict['xfersize']:
                    flist[i] = flist[i].replace('None', "'{}'".format(
                        tool_para_dict['xfersize']))
                    # flist[i] = "        cls.vdbench_parameters_dict['xfersize'] = '({})'\n".format(
                    #     tool_para_dict['xfersize'])
                else:
                    flist[i] = flist[i].replace('None', "'{}'".format(
                        tool_para_dict['xfersize']))
                # flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_BSSPLIT.value] = '({})'\n".format(
                #     tool_para_dict['bssplit'])
            elif 'SEEKPCT' in flist[i]:
                pass
                # flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_SEEKPCT.value] = {}\n".format(
                #     tool_para_dict['seekpct'])
            elif tool_para_dict['offset'] and 'OFFSET' in flist[i]:
                flist[i] = flist[i].replace('None', "'{}'".format(
                    tool_para_dict['offset']))
                # flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_OFFSET.value] = {}\n".format(
                #     tool_para_dict['offset'])
            elif tool_para_dict['align'] and 'ALIGN' in flist[i]:
                flist[i] = flist[i].replace('None', "'{}K'".format(
                    tool_para_dict['align']))
                # flist[i] = "        cls.fio_parameters_dict[FioEnum.FIO_BLOCKALIGN.value] = {}\n".format(
                #     tool_para_dict['align'])


    # vdbench工具参数设置————内容追加[脚本字段]
    # attention!!!: 由于当前vdbench的书写格式不同于fio那么统一，所以当前这个方法不是很通用。
    #               仍需要各自脚本生成器子类自己写相应的vdbench部分
    @staticmethod
    def vdbench_parameter_add(flist: str, tool_para_dict: dict) -> None:
        """
        @description  : 测试用例脚本中vdbench参数设置字段填充————追加
        ---------
        @param  : flist： 脚本内容字段缓存
                  tool_para_dict: 参数字典
                  vdbench_cc: vdbench是否需要一致性判断
        -------
        @Returns  : 空
        -------
        """
        vdbench_text = text_template.RAID_JBOD_MIX_VDBENCH.format(check=tool_para_dict['vdbench_cc'],
                                                                  xfersize=tool_para_dict['xfersize'],
                                                                  rdpct=tool_para_dict['rdpct'],
                                                                  seekpct=tool_para_dict['seekpct'])
        flist.append(vdbench_text)

    # fio工具参数设置————内容追加[脚本字段]
    @staticmethod
    def fio_parameter_add(flist: str, tool_para_dict: dict) -> None:
        """
        @description  : 测试用例脚本中fio参数设置字段填充————追加
        ---------
        @param  : flist： 脚本内容字段缓存
                  tool_para_dict: 参数字典
        -------
        @Returns  : None
        ----
        """
        fio_text = text_template.FIO_SET.format(
            prefix='global_var',
            fio_rw="'{}'".format(
                tool_para_dict['fio_rw']) if tool_para_dict['fio_rw'] else None,
            fio_bssplit="'{}'".format(tool_para_dict['xfersize']),
            fio_rwmixread="'{}'".format(
                tool_para_dict['rdpct']) if tool_para_dict['rdpct'] is not None else None,
            fio_seekpct="{}".format(
                tool_para_dict['seekpct']) if tool_para_dict['seekpct'] is not None else None,
            fio_offset="'{}'".format(
                tool_para_dict['offset']) if tool_para_dict['offset'] is not None else None,
            fio_align="'{}K'".format(
                tool_para_dict['align']) if tool_para_dict['align'] is not None else None,
            # fio_thread="{}".format(
            #     tool_para_dict['thread']) if tool_para_dict['thread'] != None else None
            )
        flist.append(fio_text)
