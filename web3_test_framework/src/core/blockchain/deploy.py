# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/5 17:08
# @File : deploy
# Description : 文件说明
"""
class ContractDeployer:
    def deploy_with_retry(self, contract_name, retries=3):
        """带重试机制的部署方法"""
        for i in range(retries):
            try:
                return self._deploy(contract_name)
            except GasPriceTooHigh:
                self.adjust_gas_strategy()