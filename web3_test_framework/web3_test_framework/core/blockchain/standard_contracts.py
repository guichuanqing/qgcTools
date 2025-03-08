# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 16:17
# @File : standard_contracts.py
# Description : 文件说明
"""
# src/core/blockchain/standard_contracts.py
import json
import requests
from pathlib import Path
from typing import Optional


class StandardContracts:
    def __init__(self, libs_path: Path = Path("libs")):
        self.base_dir = libs_path / "openzeppelin" / "contracts"
        self.versions = {
            "erc20": ["4.9.3", "5.0.0"],
            "erc721": ["4.9.3", "5.0.0"]
        }

    def get_abi(self, contract_type: str, version: str = "latest") -> dict:
        """获取标准合约ABI"""
        version = self._resolve_version(contract_type, version)
        abi_path = self.base_dir / version / f"{contract_type.upper()}.json"

        if not abi_path.exists():
            self._download_contract(contract_type, version)

        with open(abi_path) as f:
            return json.load(f)

    def _download_contract(self, contract_type: str, version: str):
        """从OpenZeppelin仓库下载预编译ABI"""
        url = f"https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/v{version}/build/contracts/{contract_type}.json"
        response = requests.get(url)
        response.raise_for_status()

        # 保存完整JSON（包含ABI和字节码）
        save_dir = self.base_dir / version
        save_dir.mkdir(parents=True, exist_ok=True)
        with open(save_dir / f"{contract_type}.json", "w") as f:
            json.dump(response.json(), f)

    def _resolve_version(self, contract_type: str, version: str) -> str:
        """解析版本别名"""
        if version == "latest":
            return self.versions[contract_type.lower()][-1]
        return version