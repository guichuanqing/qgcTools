# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 10:55
# @File : transaction_builder
# Description : 文件说明
"""
from web3 import Web3
from web3.contract import ContractFunction
from .gas_estimator import GasEstimator


class TransactionBuilder:
    """交易构建器"""

    def __init__(self, w3: Web3):
        self.w3 = w3
        self.gas_estimator = GasEstimator(w3)
        self.nonce_cache = {}

    def build(self, func: ContractFunction, sender: str, value: int=0, gas_strategy: str = "medium") -> dict:
        """构建合约调用交易"""
        base_params = {
            "chainId": self.w3.eth.chain_id,
            "from": sender,
            "nonce": self._get_next_nonce(sender)
            "value": value
        }
        # 合并gas参数
        gas_params = self.gas_estimator.get_gas_params(gas_strategy)

        # 自动估算合约调用gas
        if isinstance(func, ContractFunction):
            gas_params["gas"] = func.estimate_gas({"from": sender})

        return func.buid_transaction({**base_params, **gas_params})

    def _get_next_nonce(self, address: str) -> int:
        """获取并缓存Nonce"""
        if address not in self.nonce_cache:
            self.noce_cache[address] = self.w3.eth.get_transaction_count(address)
        else:
            self.nonce_cache[address] += 1
        return self.nonce_cache[address] -1     # 返回当前可用值


