# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/5 17:49
# @File : account
# Description : 文件说明
"""
import logging
from typing import Dict, List
from pathlib import Path
from web3_test_framework.core.account.wallet import Wallet
from web3_test_framework.config.loader import ConfigLoader
from web3_test_framework.utils.file_util import FileUtil
from web3_test_framework.utils.wallet_batch_generator import WalletBatchGenerator
import time


class Manager:
    def __init__(self, project_name: str, env: str = "test"):
        self.project_name = project_name
        self.logger = logging.getLogger("AccountManager")
        self.config = ConfigLoader(project_name, env)
        self._wallets: Dict[str, Wallet] = {}
        self.batch_dir = FileUtil.data_base
        self.temp_dir = self.batch_dir / f"{project_name}_temp"

        # 初始化默认账户
        # self._load_config_accounts()

    def _load_config_accounts(self):
        """加载配置文件中的账户"""
        accounts = self.config.load_accounts()
        for alias, acc in accounts.items():
            wallet = Wallet(
                address=acc["address"],
                private_key=acc["private_key"],
                alias=alias
            )
            self._wallets[alias] = wallet
            self.logger.info(f"Loaded config account: {alias}@{wallet.address[:8]}")

    def _generate_temp_accounts(self, count: int):
        """批量生成并统一存储"""
        file_name = self.temp_dir / f"accounts_{int((time.time()) * 1000)}"
        wallets = WalletBatchGenerator.generate_batch(count, file_path=file_name)
        for w in wallets:
            self._wallets[w.alias] = w

    def _load_account_file(self, file_path: Path):
        if file_path:
            try:
                wallets = WalletBatchGenerator.load_batch(file_path)
                for w in wallets:
                    self._wallets[w.alias] = w
                self.logger.info(f"Loaded {len(wallets)} accounts from {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to load {file_path}: {str(e)}")

    def _load_all_account_files(self):
        """加载所有批量账户文件"""
        for batch_file in self.temp_dir.glob("*.json"):
            try:
                wallets = WalletBatchGenerator.load_batch(batch_file)
                for w in wallets:
                    self._wallets[w.alias] = w
                self.logger.info(f"Loaded {len(wallets)} accounts from {batch_file}")
                print("wallets:", self._wallets)
            except Exception as e:
                self.logger.error(f"Failed to load {batch_file}: {str(e)}")

    def get_wallet(self, alias: str = None) -> Wallet:
        """获取指定账户（默认返回第一个）"""
        if alias:
            return self._wallets.get(alias, None)
        return next(iter(self._wallets.values()))

    def get_all_wallets(self) -> List[Wallet]:
        """获取所有账户（排除临时账户）"""
        return [w for w in self._wallets.values() if not w.alias.startswith(f"{self.project_name}")]

    def add_wallet(self, wallet: Wallet):
        """添加新钱包到管理池"""
        if wallet.alias in self._wallets:
            raise KeyError(f"Alias {wallet.alias} already exists")
        self._wallets[wallet.alias] = wallet


if __name__ == "__main__":
    pass
    # p_name = "CCat"
    # env = "test"
    # mm = Manager(project_name=p_name, env=env)
    msg = "Welcome to PoPP!\n\nPoPP DAPP\n\nNote: This request will not trigger a blockchain transaction or cost any gas fees.\n\nWallet address:\n0xa0c9990db6847e751536ead8a6347b90dfd68950\n\nNonce:\n9fbf14cf-0add-4c83-847b-164c48c3cb8f\n\nTimestamp:\n1741412572868"
    w = Wallet(address='0xA0c9990dB6847e751536eAD8a6347b90dFd68950', private_key='1dcffdf711a32c80927b2c8ffb9e83569317093af619f904e5633b239eb6dda9', alias='accounts_1741312954197_0')
    print(w.sign_message(msg))

    # mm._load_config_accounts()
    # mm._generate_temp_accounts(100)
    # mm._load_account_file(FileUtil.data_base/"CCat_temp"/"accounts_1741312954197.json")
    # mm._load_all_account_files()
    # mm.add_wallet(w)
    # print(mm.get_all_wallets())
    # print(mm.get_wallet("accounts_1741312954197_1"))