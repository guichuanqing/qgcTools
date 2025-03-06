# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/6 16:55
# @File : wallet_generator
# Description : 文件说明
"""
import os
import json
from typing import List
from pathlib import Path
from web3_test_framework.core.account.wallet import Wallet
from web3_test_framework.utils.file_util import FileUtil


class WalletBatchGenerator:
    @classmethod
    def generate_batch(
            cls,
            count: int,
            file_path: str = "batch_accounts"
    ) -> List["Wallet"]:
        """批量生成钱包并保存到单个文件"""
        wallets = [Wallet.generate() for _ in range(count)]
        file_name = os.path.basename(file_path)
        batch_data = {
            "version": "1.0",
            "wallets": [
                {
                    "address": w.address,
                    "private_key": w.private_key,
                    "alias": f"{file_name}_{i}"
                } for i, w in enumerate(wallets)
            ]
        }

        output_path = FileUtil.data_base / f"{file_path}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(batch_data, f, indent=2)

        # 返回生成的钱包对象
        for w, data in zip(wallets, batch_data["wallets"]):
            w.alias = data["alias"]
            w.batch_file = output_path
        return wallets

    @classmethod
    def load_batch(cls, file_path: Path) -> List["Wallet"]:
        """从批量文件加载钱包"""
        with open(file_path) as f:
            data = json.load(f)

        wallets = []
        for acc in data["wallets"]:
            wallet = Wallet(
                address=acc["address"],
                private_key=acc["private_key"],
                alias=acc["alias"],
            )
            wallets.append(wallet)
        return wallets

if __name__ == "__main__":
    pass
    # count = 5
    # file_name = "test_batch_accounts"
    # path = FileUtil.data_base / f"test_batch_accounts.json"
    # # wallets = WalletBatchGenerator.generate_batch(count, file_name=file_name)
    # wallets = WalletBatchGenerator.load_batch(path)
    # print(wallets[0].address)