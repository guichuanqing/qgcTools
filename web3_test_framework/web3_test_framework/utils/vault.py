# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/5 18:27
# @File : vault
# Description : 文件说明
"""
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

class Vault:
    def __init__(self, key=None):
        self.key = key or Fernet.generate_key()

    def encrypt_value(self, value: str) -> str:
        return Fernet(self.key).encrypt(value.encode()).decode()

    def decrypt_value(self, encrypted: str) -> str:
        return Fernet(self.key).decrypt(encrypted.encode()).decode()