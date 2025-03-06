# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/6 10:00
# @File : wallet
# Description : 文件说明
"""
import json
from eth_account import Account
from web3 import Web3
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Wallet:
    address: str
    private_key: str
    alias: Optional[str] = None

    def __post_init__(self):
        if not Web3.is_address(self.address):
            raise ValueError(f"Invalid address: {self.address}")

    @classmethod
    def generate(cls) -> "Wallet":
        """生成随机钱包"""
        acct = Account.create()
        return cls(address=acct.address, private_key=acct.key.hex(), alias="random_account")

    @classmethod
    def from_private_key(cls, priv_key: str) -> "Wallet":
        """从私钥导入"""
        acct = Account.from_key(priv_key)
        return cls(
            address=acct.address,
            private_key=priv_key,
            alias="private_account"
        )
