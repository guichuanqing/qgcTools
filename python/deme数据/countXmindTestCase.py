# 模块名称（文件名为：parse_xmind.py）
import requests
import xmindparser

"""
@desc:   定义xmind中测试用例和质保平台对应的字段的类
@author: 
@date:   
"""


class SaveTestCaseParam(object):
    def __init__(self):
        self.case_name = ""
        self.test_case_level = ""
        self.pre_condition = ""
        self.step = ""
        self.expected_results = ""


"""
@desc:   读取整个测试用例的根节点和对应的子节点
@author: 
@date:   
"""


def xmind_parse_file(file_path):
    content_dict = xmindparser.xmind_to_dict(file_path)
    for index1 in content_dict:
        node_lists = index1['topic']['topics']
        case_list = []
        read_node(node_lists, case_list)
    return case_list


"""
@desc:   拼装xmind中的每一条测试用例
@author: 
@date:   
"""


def read_node(node_lists, case_list):
    if len(node_lists) >= 1:
        for node in node_lists:
            # 如何知道遍历的是最后一个节点
            # 当前的node的所有的key中没有topics，那就说明是最后一个节点了
            if not list(node.keys()).__contains__("topics"):
                for k, v in node.items():
                    case_list.append(v)
                # test_case_param = SaveTestCaseParam()
                # for key in node:
                #     if key == "title":
                #         setattr(test_case_param, 'case_name', node[key])
                #         setattr(test_case_param, 'step', node[key])
                #         setattr(test_case_param, 'expected_results', node[key])
                #         continue
                #     if key == "makers":
                #         setattr(test_case_param, 'test_case_level', node[key][0])

                # 添加到list中
                # case_list.append(node.keys)

            # 倒数第二个节点
            # else:
            #     if list(node.keys()).__contains__("makers"):
            #         test_case_param = SaveTestCaseParam()
            #         for key in node:
            #             if key == "title":
            #                 setattr(test_case_param, 'case_name', node[key])
            #                 continue
            #             if key == 'topics':
            #                 parent_node = node[key]
            #                 for sub_node_key in parent_node:
            #                     for key1 in sub_node_key:
            #                         if key1 == "title":
            #                             title_content = sub_node_key['title']
            #                             if "前置条件" in title_content:
            #                                 setattr(test_case_param, 'pre_condition', title_content)
            #                                 continue
            #                             if "用例步骤" in title_content:
            #                                 setattr(test_case_param, 'step', title_content)
            #                                 continue
            #                             if "预期结果" in title_content:
            #                                 setattr(test_case_param, 'expected_results', title_content)
            #                 continue
            #             if key == 'makers':
            #                 setattr(test_case_param, 'test_case_level', node[key][0])
            #         # 添加到list中
            #         case_list.append(test_case_param)
            else:
                for key in node:
                    if key == 'topics':
                        read_node(node[key], case_list)


"""
@desc:   主入口
@author: 
@date:   
"""

if __name__ == '__main__':
    # 文件路径
    file_path = 'C:/Users/qgc/Desktop/1.5.1扫码.xmind'
    case_list = xmind_parse_file(file_path)
    print("测试案例个数：", len(case_list))
