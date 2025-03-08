# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 11:19
# @File : contract_handler
# Description : 文件说明
"""
from web3 import Web3
from web3.contract import Contract
from typing import Optional, Dict, Any
from ..transaction.transaction_builder import TransactionBuilder
from ..transaction.transaction_sender import TransactionSender
from ..account.wallet import Wallet
from .abi_loader import ABILoader


class ContractHandler():
    """合约交互核心类
            w3 = Web3(Web3.HTTPProvider(RPC_URL))
            wallet = Wallet.from_private_key("0x...")
            # 加载合约
            erc20 = w3.eth.contract(
                address="0x...",
                abi=ERC20_ABI
            )
            # 创建处理器
            handler = ContractHandler(
                w3=w3,
                wallet=wallet,
                contract=erc20
            )
    """

    def __init__(self, w3: Web3, wallet: Wallet, project: str, contract_name: str, contract: Contract, builder: Optional[TransactionBuilder] = None,
                 sender: Optional[TransactionSender] = None, abi_loader: ABILoader = None):
        self.w3 = w3
        self.wallet = wallet
        self.abi_loader = abi_loader or ABILoader()

        # 初始化合约实例
        abi = self.abi_loader.load_abi(project=project, concept_name=contract_name)
        self.contract = w3.eth.contract(address=contract_address, abi=abi)

        self.builder = builder or TransactionBuilder(w3)
        self.sender = sender or TransactionSender(w3)

        # 缓存常用属性
        self.address = contract.address
        self.abi = contract.abi

    def call(self, func_name:str, *args, **kwargs) -> Any:
        """只读调用（不消耗gas）"""
        func = getattr(self.contract.functions, func_name)(*args)
        return func.call(**kwargs)

    def transact(self, func_name: str, *args, gas_strategy: str = "medium", value: int = 0, retries: int = 3,
                 **kwargs) -> Dict:
        """执行合约交易（自动构建+发送）"""
        func = getattr(self.contract.functions, func_name)(*args)

        # 自动构建交易
        tx_data = self.builder.build(func=func, sender=self.wallet.address, value=value, gas_strategy=gas_strategy)

        # 签名并发送
        signed_tx = self.wallet.sign_transaction(tx_data)

        # 带重试机制的发送
        for attempt in range(retries):
            try:
                receipt = self.sender.send_and_confirm(signed_tx)
                return {
                    "status": "success",
                    "receipt": receipt,
                    "tx_hash": receipt.transactionHash.hex()
                }
            except Exception as e:
                if attempts == retries - 1:
                    return {
                        "status": "failed",
                        "error": str(e)
                    }
                # 失败时重建交易（更新nonce/gas）
                tx_data = self.builder.build(...)  # 重新构建逻辑

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