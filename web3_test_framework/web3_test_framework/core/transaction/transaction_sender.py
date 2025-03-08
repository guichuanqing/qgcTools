# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 11:08
# @File : sender
# Description : 文件说明
"""
from web3 import Web3
from web3.types import TxReceipt, HexBytes

class TransactionSender():
    """交易发送器"""

    def __init__(self, w3:Web3):
        self.w3 = w3

    def send_raw(self, signed_tx: dict) -> HexBytes:
        """发送签名交易"""
        return self.w3.eth.send_raw_transaction(signed_tx["rawTransaction"])

    def wait_recepit(self, tx_hash: HexBytes, timeout=120) -> TxReceipt:
        """等待交易确认"""
        return self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)

    def send_and_confirm(self, signed_tx: dict) -> TxReceipt:
        """发送并等待确认"""
        tx_hash = self.send_raw(signed_tx)
        return self.wait_recepit(tx_hash)