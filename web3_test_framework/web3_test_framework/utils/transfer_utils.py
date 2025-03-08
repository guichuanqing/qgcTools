# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 14:15
# @File : transfer_utils
# Description : 文件说明
"""
from typing import Dict, Union
from web3 import Web3
from eth_typing import HexStr
from web3.types import TxReceipt
from ..core.account.wallet import Wallet
from ..core.transaction.transaction_builder import TransactionBuilder
from ..core.transaction.transaction_sender import TransactionSender
from ..core.contract.contract_handler import ContractHandler


class TransferUtils:
    """区块链资产转账工具集"""

    def __init__(self, w3: Web3):
        self.w3 = w3
        self.chain_id = w3.eth.chain_id
        self._builder = TransactionBuilder(w3)
        self._sender = TransactionSender(w3)

    def send_eth(self, sender: Wallet, to_address: str, amount_wei: int, gas_strategy: str = "medium",
                 priority_fee: int = None) -> Dict[str, Union[HexStr, TxReceipt]]:
        """
        ETH转账（原生代币）
        :param sender: 发送方钱包实例
        :param to_address: 接收地址
        :param amount_wei: 转账金额（wei单位）
        :param gas_strategy: Gas策略选择
        :param priority_fee: 自定义优先费（可选）
        :return: 包含交易哈希和收据的字典
        """
        # 构建基础交易参数
        tx_params = {
            "chainId": self.chain_id,
            "to": to_address,
            "value": amount_wei,
            "nonce": self._builder._get_next_nonce(sender.address)
        }
        # 处理gas参数
        gas_params = self._builder.gas_estimator.get_gas_params(gas_strategy)
        if priority_fee:
            gas_params["maxPriorityFeePerGas"] = priority_fee
        # 合并参数签名
        full_tx = {**tx_params, **gas_params}
        signed_tx = sender.sign_transaction(full_tx)
        # 发送交易并等待确认
        tx_hash = self._sender.send_raw(signed_tx)
        receipt = self._sender.wait_recepit(tx_hash)

        return {
            "tx_hash": tx_hash.hex(),
            "receipt": receipt
        }

    def send_rec721(self, sender: Wallet, contract_address: str, receiver: str, token_id: int,
                    project: str = 'nft_project', gas_strategy: str = "medium") -> Dict[str, Union[HexStr, TxReceipt]]:
        """
        ERC721 NFT转账
        :param sender: 发送方钱包实例
        :param contract_address: NFT合约地址
        :param receiver: 接收地址
        :param token_id: 代币ID
        :param project: 项目目录名称（用于ABI加载）
        :param gas_strategy: Gas策略选择
        """
        # 初始化合约处理器
        handler = ContractHandler(w3=self.w3, wallet=sender, project=project, contract_name="ERC721",
                                  contract_address=contract_address)
        # 检查NFT所有权
        current_owner = handler.call("ownerOf", token_id)
        if current_owner.lower() != sender.address.lower():
            raise ValueError(f"Token {token_id} 不属于发送地址！")

        # 执行转账
        receipt = handler.transact(func_name="safeTransferFrom", from_address=sender.address, to_address=receiver,
                                   token_id=token_id,
                                   gas_strategy=gas_strategy)
        return {
            "tx_hash": receipt["tx_hash"],
            "receipt": receipt["receipt"]
        }

    def send_erc1155(self): # 类似ERC721的实现
        pass
