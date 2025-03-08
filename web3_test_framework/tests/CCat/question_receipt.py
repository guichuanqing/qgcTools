# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 10:13
# @File : question_receipt
# Description : 文件说明
"""
from dataclasses import dataclass


@dataclass
class QuestionReceipt:
    tx_hash: str
    block_number: int
    fee: int
    status: str