# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 11:19
# @File : contract_handler
# Description : 文件说明
"""
from web3.contract import Contract
from typing import Optional, Dict, Any


class ContractHandler:
    """专注合约交互，不处理实例化逻辑"""

    def __init__(self, contract: Optional[Contract] = None):

        # 初始化合约实例
        self.contract = contract

    def call(self, func_name:str, *args, **kwargs) -> Any:
        """只读调用（不消耗gas）"""
        func = getattr(self.contract.functions, func_name)(*args)
        return func.call(**kwargs)

    def transact(self, func_name: str, *args, **tx_params) -> dict:
        """交易发送"""
        func = getattr(self.contract.functions, func_name)(*args)
        # 必须包含from地址
        if "from" not in tx_params:
            raise ValueError("交易参数必须包含发送地址（from）")

        try:
            tx_hash = func.transact(tx_params)
            receipt = self.contract.web3.eth.wait_for_transaction_receipt(tx_hash)
            return {
                "tx_hash": tx_hash.hex(),
                "receipt": receipt
            }
        except TransactionNotFound as e:
            raise RuntimeError(f"交易未确认: {str(e)}") from e

        # 自动构建交易
        # tx_data = self.builder.build(func=func, sender=self.wallet.address, value=value, gas_strategy=gas_strategy)
        #
        # # 签名并发送
        # signed_tx = self.wallet.sign_transaction(tx_data)
        #
        # # 带重试机制的发送
        # for attempt in range(retries):
        #     try:
        #         receipt = self.sender.send_and_confirm(signed_tx)
        #         return {
        #             "status": "success",
        #             "receipt": receipt,
        #             "tx_hash": receipt.transactionHash.hex()
        #         }
        #     except Exception as e:
        #         if attempt == retries - 1:
        #             return {
        #                 "status": "failed",
        #                 "error": str(e)
        #             }
                # 失败时重建交易（更新nonce/gas）
                # tx_data = self.builder.build(...)  # 重新构建逻辑

    @property
    def functions(self):
        """直接访问原始合约方法（高级模式）"""
        return self.contract.functions

    def estimate_gas(self, func_name:str, *args) -> int:
        """快速估算gas消耗"""
        func = getattr(self.contract.functions, func_name)(*args)
        return func.estimate_gas({"from": self.wallet.address})

    def events(self, event_name:str, from_block=0):
        """监听合约事件"""
        event = getattr(self.contract.events, event_name)
        return event.get_logs(fromBlock=from_block)

    @property
    def address(self) -> str:
        return self.contract.address