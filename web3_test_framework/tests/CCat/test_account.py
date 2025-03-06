# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/6 10:05
# @File : test_account
# Description : 文件说明
"""
import json
import pytest
from web3_test_framework.core.account.manager import Manager as AccountManager
from web3_test_framework.core.account.wallet import Wallet as AccountWallet

def test_account_with_wallet()

def test_wallet_generation(temp_wallet):
    assert temp_wallet.address.startswith("0x")
    assert len(temp_wallet.private_key) == 66  # 32字节的hex表示


# def test_contract_interaction(web3, account_manager):
#     # 获取已部署的合约实例
#     contract = web3.eth.contract(
#         address="0x...",
#         abi=ERC20_ABI
#     )
#
#     # 使用配置账户发送交易
#     admin = account_manager.get_wallet("admin")
#     tx = contract.functions.transfer(
#         "0xRecipientAddress",
#         100
#     ).build_transaction({
#         "from": admin.address,
#         "nonce": web3.eth.get_transaction_count(admin.address)
#     })
#
#     # 签名并发送
#     signed_tx = admin.sign_transaction(tx)
#     tx_hash = web3.eth.send_raw_transaction(signed_tx["rawTransaction"])
#
#     # 验证交易
#     receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
#     assert receipt.status == 1

if __name__ == "__main__":
    # 使用pytest运行测试
    pytest.main(['-v', '--tb=short', __file__])