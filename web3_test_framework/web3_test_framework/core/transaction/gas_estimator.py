# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 10:49
# @File : gas_estimator
# Description : 文件说明
"""
from web3 import Web3
from web3.types import Wei, GasPriceStrategy


class GasEstimator():
    """gas计算"""
    def __init__(self, w3: Web3):
        self.w3 = w3

    def get_gas_params(self, strategy: GasPriceStrategy= 'medium') -> dict:
        """获取推荐gas参数"""
        current_gas = self.w3.eth.gas_price

        # 内置策略
        strategies = {
            'low': current_gas * 0.9,
            'medium': current_gas,
            'high': current_gas * 1.2,
            'aggressive': current_gas * 1.5
        }

        return {
            "gasPrice": strategies[strategy],
            "gas" : 21000   # 默认简单转账Gas
        }