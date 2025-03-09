# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 14:43
# @File : test_transfer_utils
# Description : 文件说明
"""
# tests/test_transfer_utils.py
from web3 import Web3

from web3_test_framework.config.loader import ConfigLoader
from web3_test_framework.core.account.wallet import Wallet
from web3_test_framework.utils.transfer_utils import TransferUtils
from web3_test_framework.core.contract.contract_loader import ContractLoader
from web3_test_framework.core.contract.contract_handler import ContractHandler

config = ConfigLoader("CCat", "test")

class TestTransferUtils:

    def __init__(self, w3):
        self.utils = TransferUtils(w3)
        self.config = config
        self.alice = Wallet.from_private_key("01da4c47854e12d070bf0f07e358902d0583ac82617dfcbfaecdc42766d89bec")
        self.bob = Wallet.from_private_key("5385cab2a10a9bc6b197aba6f06e022ae23f9a3a149c5a5a5a1874b478ed7575")

    def test_eth_transfer(self):
        # 执行ETH转账
        result = self.utils.send_eth(self.alice, self.bob.address, Web3.to_wei(0.01, 'ether'))
        # 验证结果
        assert result['receipt'].status == 1

    def test_nft_transfer(self):
        # 执行ETH转账
        result = self.utils.send_erc721(self.alice, "0xaCaBC6EA6A00e8b5F3D04D29d43E4F089b26a980", self.bob.address, 89)
        print(result)
        # 验证结果
        assert result['receipt'].status == 1


if __name__ == "__main__":
    # 初始化
    network = config.load_network_config("Taiko Hekla")
    w3 = Web3(Web3.HTTPProvider(network["rpc"]))
    loader = ContractLoader(w3)

    contract = loader.from_address(
        address="0xaCaBC6EA6A00e8b5F3D04D29d43E4F089b26a980",
        abi_source="standard",
        source_params={
            "contract_type": "ERC721",
            "version": "5.0.1"
        }
    )


    t = TestTransferUtils(w3)

    # t.test_eth_transfer()
    t.test_nft_transfer()
    # wallet = Wallet.from_private_key("0x...")