# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2025/3/5 17:42
# @File : compiler
# Description : 文件说明
"""
class SolidityCompiler:
    def compile_project(self, optimize=True):
        """编译整个contracts目录"""
        return subprocess.check_output([
            'solc',
            '--optimize' if optimize else '',
            '--combined-json', 'abi,bin,userdoc',
            './contracts/**/*.sol'
        ])