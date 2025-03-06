import os
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 定义常用路径
WORKING_BASE = PROJECT_ROOT / "web3_test_framework"
DATA_BASE = PROJECT_ROOT / "data"
CONFIG_FILE = PROJECT_ROOT / "config.xml"

class FileUtil:
    # 类用于处理文件相关的操作，如文件路径管理、文件清理、文件复制等
    parent_url = PROJECT_ROOT
    data_base = DATA_BASE
    working_base = WORKING_BASE

    @staticmethod
    def set_work_base(base_dir: str):
        FileUtil.WORKING_BASE = base_dir

    @staticmethod
    def get_current_dir():
        return os.getcwd()

    @staticmethod
    def get_working_dir():
        work_dir = FileUtil.get_current_dir()
        if FileUtil.working_base:
            work_dir = os.path.join(work_dir, FileUtil.working_base)
        return work_dir

    def get_absolute_path(relative_path: str) -> Path:
        """获取相对于项目根目录的绝对路径"""
        return PROJECT_ROOT / relative_path

    @staticmethod
    def write_str_to_file(file_content: str, file_full_path: str):
        try:
            with open(file_full_path, 'w', encoding='utf-8') as file:
                file.write(file_content)
            return True
        except Exception as e:
            print(f"Error writing to file {file_full_path}: {str(e)}")
            return False
