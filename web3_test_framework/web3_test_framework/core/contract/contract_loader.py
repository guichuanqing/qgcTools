from web3 import Web3
from web3.contract import Contract
from pathlib import Path
from typing import Union
from .abi_loader import ABILoader
import json


class ContractLoader:
    """合约实例化工厂类"""

    def __init__(self, w3: Web3, abi_loader: ABILoader = None):
        self.w3 = w3
        self.abi_loader = abi_loader or ABILoader()

    def from_address(
            self,
            address: str,
            abi_source: str = "etherscan",  # etherscan/standard/local
            source_params: dict = None
    ) -> Contract:
        """通过合约地址加载"""
        source_params = source_params or {}

        # 获取ABI
        if abi_source == "etherscan":
            abi = self.abi_loader.load_abi(source_type=abi_source,
                address = address,
                network=source_params.get("network", "mainnet")
            )
        elif abi_source == "standard":
            abi = self.abi_loader.load_abi(source_type=abi_source,
                contract_type=source_params["contract_type"],
                version=source_params.get("version", "latest")
            )
        elif abi_source == "local":
            abi = self.abi_loader.load_local_abi(source_type=abi_source,
                project=source_params["project"],
                contract_name=source_params["contract_name"]
            )
        else:
            raise ValueError(f"不支持的ABI来源: {abi_source}")

        # 创建合约实例
        return self.w3.eth.contract(
            address=address,
            abi=abi
        )

    def from_abi_file(
            self,
            address: str,
            abi_path: Union[str, Path]
    ) -> Contract:
        """直接通过ABI文件加载"""
        with open(abi_path) as f:
            abi = json.load(f)
        return self.w3.eth.contract(address=address, abi=abi)