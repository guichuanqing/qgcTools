# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/5 18:29
# @File : validator
# Description : 文件说明
"""
# src/config/validator.py
from pydantic import BaseModel

class NetworkConfigSchema(BaseModel):
    rpc: str
    chain_id: int
    explorer: str
    gas_config: dict