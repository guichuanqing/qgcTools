# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 12:34
# @File : abi_loader
# Description : 文件说明
"""
import json
import requests
from pathlib import Path
from typing import Dict, Any, Optional, Union
from eth_utils import is_address, to_checksum_address


class ABILoader:
    """
    多源ABI加载器，支持以下加载方式：
    1. 本地项目文件 (project/contract_name)
    2. 标准合约库 (如OpenZeppelin)
    3. 区块链浏览器API (如Etherscan)
    """

    def __init__(
            self,
            base_path: Optional[Path] = None,
            standard_libs_path: Path = Path("libs"),
            etherscan_api_key: Optional[str] = None
    ):
        """
        :param base_path: 本地项目ABI基础路径
        :param standard_libs_path: 标准合约库存储路径
        :param etherscan_api_key: Etherscan API密钥
        """
        # 路径配置
        self.base_path = base_path or Path(__file__).parent.parent.parent / "test"
        self.standard_libs_path = standard_libs_path

        # API配置
        self.etherscan_api_key = etherscan_api_key

        # 缓存系统
        self._cache: Dict[str, Any] = {}
        self._init_standard_contracts()

    def load_abi(
            self,
            source_type: str = "local",
            **kwargs
    ) -> list:
        """
        多源ABI加载入口
        :param source_type: 来源类型 (local/standard/etherscan)
        :param kwargs: 不同来源需要的参数
            - local: project, contract_name
            - standard: contract_type, version
            - etherscan: contract_address, network
        """
        if source_type == "local":
            return self._load_local_abi(
                kwargs["project"],
                kwargs["contract_name"]
            )
        elif source_type == "standard":
            return self._load_standard_abi(
                kwargs["contract_type"],
                kwargs.get("version", "latest")
            )
        elif source_type == "etherscan":
            return self._load_etherscan_abi(
                kwargs["contract_address"],
                kwargs["network"]
            )
        else:
            raise ValueError(f"不支持的ABI来源类型: {source_type}")

    def _load_local_abi(self, project: str, contract_name: str) -> list:
        """加载本地项目ABI文件"""
        cache_key = f"local_{project}_{contract_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        abi_file = self.base_path / project / f"{contract_name}_abi.json"

        if not abi_file.exists():
            available = [f.stem.replace("_abi", "")
                         for f in self.base_path.glob(f"{project}/*_abi.json")]
            raise FileNotFoundError(
                f"本地ABI文件未找到: {abi_file}\n"
                f"可用合约: {available}"
            )

        with open(abi_file, "r", encoding="utf-8") as f:
            abi = json.load(f)
            self._cache[cache_key] = abi
            return abi

    def _load_standard_abi(self, contract_type: str, version: str) -> list:
        """加载标准合约ABI"""
        contract_type = contract_type.lower()
        version = self._resolve_standard_version(contract_type, version)

        cache_key = f"standard_{contract_type}_{version}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # 标准合约路径示例: libs/openzeppelin/erc20/4.9.3/ERC20.json
        abi_path = (
                self.standard_libs_path / "openzeppelin" /
                contract_type / version / f"{contract_type.upper()}.json"
        )

        if not abi_path.exists():
            self._download_standard_abi(contract_type, version)

        with open(abi_path) as f:
            full_json = json.load(f)
            self._cache[cache_key] = full_json["abi"]
            return full_json["abi"]

    def _load_etherscan_abi(self, contract_address: str, network: str) -> list:
        """从Etherscan加载ABI"""
        contract_address = to_checksum_address(contract_address)
        cache_key = f"etherscan_{network}_{contract_address}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        base_urls = {
            "mainnet": "https://api.etherscan.io",
            "goerli": "https://api-goerli.etherscan.io",
            "taiko": "https://explorer.test.taiko.xyz/api"
        }

        url = (
            f"{base_urls[network]}/api?module=contract"
            f"&action=getabi&address={contract_address}"
            f"&apikey={self.etherscan_api_key}"
        )

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "1":
            raise ValueError(f"Etherscan返回错误: {data['result']}")

        abi = json.loads(data["result"])
        self._cache[cache_key] = abi
        return abi

    def _init_standard_contracts(self):
        """初始化标准合约版本索引"""
        self.standard_versions = {
            "erc20": ["4.9.3", "5.0.0"],
            "erc721": ["4.8.0", "5.0.1"]
        }

    def _resolve_standard_version(self, contract_type: str, version: str) -> str:
        """解析标准合约版本"""
        if version == "latest":
            return self.standard_versions[contract_type][-1]
        if version not in self.standard_versions.get(contract_type, []):
            raise ValueError(f"不支持的版本: {contract_type} {version}")
        return version

    def _download_standard_abi(self, contract_type: str, version: str):
        """下载标准合约ABI"""
        url = (
            f"https://raw.githubusercontent.com/OpenZeppelin/openzeppelin-contracts/"
            f"v{version}/build/contracts/{contract_type.capitalize()}.json"
        )

        response = requests.get(url)
        response.raise_for_status()

        save_path = (
                self.standard_libs_path / "openzeppelin" /
                contract_type / version / f"{contract_type.upper()}.json"
        )
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with open(save_path, "w") as f:
            json.dump(response.json(), f)

    def set_custom_path(self, path_type: str, path: Union[str, Path]):
        """设置自定义路径
        :param path_type: local/standard
        """
        if path_type == "local":
            self.base_path = Path(path)
        elif path_type == "standard":
            self.standard_libs_path = Path(path)
        else:
            raise ValueError(f"不支持的路径类型: {path_type}")