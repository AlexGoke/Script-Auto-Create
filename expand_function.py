"""
author: liuyuan
date: 2020.08.25
description: 自动脚本生成工具 扩展功能类
"""

import subprocess
import text_template


class FuncSet(object):

    def __init__(self):
        pass

    @staticmethod
    def find_scene_parameter(test_scene_info: str) -> dict:
        """
        @description  : 从用例的测试场景信息中获取用例要求的 测试盘 参数信息
        ---------
        @param  :
        -------
        @Returns  :
        -------
        """
        res = {}

    # 从用例的操作步骤信息中获取测试用例要求的 vdbench/fio 参数信息

    @classmethod
    def find_tool_parameter(cls, step_content: str, parameter: list, tool: str, case_title: str) -> dict:
        """
        @description  : 从测试用例的操作步骤信息中，获取测试工具需要设置的参数的数值
        ---------
        @param  ：  step_content： 按行切分后的操作步骤信息
                    parameter:  需要查找的参数名称列表
        -------
        @Returns  : 想要查找的参数 对应的的名称-值字典
        -------
        """
        res = {}
        # 因为测试用例excel中都是用的vdbench及其相关名词，所以搜索信息还是用vdbench的相关名词
        for x in range(len(parameter)):
            # if parameter[x] == 'xfersize' or parameter[x] == 'bssplit':
            # 由于当前测试用例excel中测试工具都写的是vdbench，所以数据块都用的xfersize
            if parameter[x] == 'xfersize' or parameter[x] == '块大小':
                res[parameter[x]] = cls.find_test_data_block(
                    step_content, tool)
                continue
            parameter_index = step_content.find(parameter[x])
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
            print('vdbench一致性校验：{}'.format(vdbench_cc))
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
        index1 = step_content.find('(')
        index2 = step_content.find(')')
        # 数据块是多个值的情况
        if index1 != -1 and index2 != -1:
            res = step_content[index1+1:index2]
            res = res.replace(' ', '')
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
                                                                  xfersize=xfersize,
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
            fio_rw="'{}'".format(
                tool_para_dict['fio_rw']) if tool_para_dict['fio_rw'] else None,
            fio_bssplit="'{}'".format(tool_para_dict['xfersize']),
            fio_rwmixread="'{}'".format(
                tool_para_dict['rdpct']) if tool_para_dict['rdpct'] != None else None,
            fio_seekpct="{}".format(
                tool_para_dict['seekpct']) if tool_para_dict['seekpct'] != None else None,
            fio_offset="'{}'".format(
                tool_para_dict['offset']) if tool_para_dict['offset'] != None else None,
            fio_align="'{}K'".format(
                tool_para_dict['align']) if tool_para_dict['align'] != None else None
        )
        flist.append(fio_text)
