# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/8 12:34
# @File : abi_loader
# Description : 文件说明
"""
import json
from pathlib import Path
from typing import Dict, Any
from web3_test_framework.utils.file_util import FileUtil


class ABILoader:
    def __init__(self, base_path: Path = None):
        """
        :param base_path: 基准路径，默认框架安装目录下的test文件夹
        """
        if not base_path:
            self.base_path = FileUtil.app_base
        else:
            self.base_path = Path(base_path)

        self._cache: Dict[str, Any] = {}

    def load_abi(self, project: str, contract_name: str) -> list:
        """
        加载指定项目的ABI文件
        :param project: 项目目录名称（如"ask"）
        :param contract_name: 合约逻辑名称（如"ERC20"）
        :return: 解析后的ABI列表
        """
        cache_key = f"{project}/{contract_name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # 构建ABI文件路径
        abi_file = self.base_path / project / f"{contract_name}_abi.json"

        if not abi_file.exists():
            available_files = [f.name for f in (self.base_path / project).glob("*.json")]
            raise FileNotFoundError(
                f"ABI文件未找到: {abi_file}\n"
                f"可用文件: {available_files}"
            )

        try:
            with open(abi_file, "r", encoding="utf-8") as f:
                abi = json.load(f)
                self._cache[cache_key] = abi
                return abi
        except json.JSONDecodeError as e:
            raise ValueError(f"ABI文件格式错误: {abi_file}") from e
        except Exception as e:
            raise RuntimeError(f"加载ABI文件失败: {str(e)}") from e

    def set_custom_path(self, path: str):
        """设置自定义ABI存储路径"""
        self.base_path = Path(path)