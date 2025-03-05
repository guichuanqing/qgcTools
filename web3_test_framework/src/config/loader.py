# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/5 18:22
# @File : loader
# Description : 文件说明
"""
# src/config/loader.py
import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class ConfigLoader:
    def __init__(self, project_name: str, env: str = "prod"):
        self.base_path = Path(__file__).parent.parent / "config"
        self.project_name = project_name
        self.env = env
        load_dotenv()  # 加载环境变量

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        with open(self.base_path / filename) as f:
            return yaml.safe_load(f)

    def load_project_config(self) -> Dict[str, Any]:
        """加载项目级配置"""
        config = self._load_yaml("projects.yaml")[self.project_name]

        # 注入环境变量
        config["env_config"]["current"] = config["env_config"][self.env]
        return config

    def load_network_config(self, network_name: str) -> Dict[str, Any]:
        """加载网络配置"""
        networks = self._load_yaml("networks.yaml")["chains"]
        return networks[network_name]

    def load_accounts(self, pattern: str = None) -> Dict[str, Any]:
        """加载账户配置"""
        accounts_data = self._load_yaml("accounts.yaml")

        # 解密处理
        decrypted = {}
        for alias, acc in accounts_data["accounts"].items():
            if acc["private_key"].startswith("encrypted:"):
                decrypted[alias] = self._decrypt_account(acc, accounts_data["encryption_key"])
            else:
                decrypted[alias] = acc
        return decrypted

    def _decrypt_account(self, account: Dict, key: str) -> Dict:
        """使用Fernet解密账户"""
        from cryptography.fernet import Fernet
        cipher = Fernet(os.getenv(key))

        encrypted = account["private_key"].split("encrypted:")[1]
        account["private_key"] = cipher.decrypt(encrypted.encode()).decode()
        return account

"""
# 初始化配置
loader = ConfigLoader(project_name="nft_marketplace", env="staging")

# 获取项目配置
project_config = loader.load_project_config()
print(project_config["env_config"]["current"]["api"]) 
# 输出：https://staging-api.nft-market.io/v1

# 获取BSC主网配置
bsc_config = loader.load_network_config("bsc_mainnet")
print(bsc_config["rpc"]) 
# 输出：https://bsc-dataseed.binance.org

# 获取管理员账户
accounts = loader.load_accounts()
admin_account = accounts["admin"]
print(admin_account["address"])
"""