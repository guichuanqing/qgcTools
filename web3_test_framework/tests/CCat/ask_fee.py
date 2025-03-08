# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 16:46
# @File : ask_fee
# Description : 文件说明
"""
import math


def compute_purchase_cost(P0, a, Q, V, VA, ThreeHasNew=False):
    """
    计算总的购买费用 P，公式为：P = P0 * (1 + a * H)

    参数:
    - P0: 基础费用常量
    - a: 系数常量
    - Q: 变量 Q
    - V: 变量 V
    - VA: 变量 VA
    - ThreeHasNew: 布尔值参数，如果为 True，则热度系数 H 乘以 0.9

    其中热度系数 H 的计算公式为：
    H = ln(Q + 1) / ln(100) * (V / VA)

    同时 P 的绝对上限为 P0 * 3。
    """
    # 计算热度系数 H
    H = math.log(Q + 1) / math.log(100) * (V / VA)

    # 如果 ThreeHasNew 为 True，则 H 乘以 0.9
    if ThreeHasNew:
        H *= 0.9

    # 计算费用 P
    P = P0 * (1 + a * H)

    # 费用的绝对上限为 P0 * 3
    if P > P0 * 3:
        P = P0 * 3

    return P

def calc_P0(num):
    if num < 30000:
        return 0.01
    elif 30000<=num and num <50000:
        return 0.03
    elif 50000 <= num and num < 100000:
        return 0.06
    elif 100000 <= num and num < 300000:
        return 0.1
    elif 300000 <= num and num < 500000:
        return 0.15
    elif 500000 <= num and num < 1000000:
        return 0.3
    elif 100000 < num:
        return 0.5

# 示例测试
if __name__ == '__main__':
    # 定义常量和测试数据
    fans = 10000
    P0 = calc_P0(fans)
    print(P0)
    a = 0.5
    Q = 1
    V = 0
    VA = 10
    ThreeHasNew = True

    cost = compute_purchase_cost(P0, a, Q, V, VA, ThreeHasNew)
    print("计算得到的购买费用为:", cost)
