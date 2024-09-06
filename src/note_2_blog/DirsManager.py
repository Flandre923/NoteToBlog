from typing import List
import os
from loguru import logger


class RelativateDirs:
    def __init__(self, file_path: str, relative_path: str) -> None:
        self.file_path: str = file_path
        self.relative_path: str = relative_path


class DirsManager:
    # 1. 给出root dir的路径
    # 2. 查找所有的该root的下的md文件
    # 3. 并保证md所作为文件下有init.json文件，没有则报错
    # 4. 计算 root 文件和 md 文件的相对路径
    def __init__(self, root_dir: str, output: str) -> None:
        self.root_dir = root_dir
        self.out_put = output
        self.md_files: List[RelativateDirs] = []
        logger.info(f"Initializing DirsManager with root_dir: {self.root_dir}")
        self._find_md_files()

    def _find_md_files(self):
        logger.info("Searching for md files in the directory...")
        # 遍历root_dir下的所有文件和文件夹
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                # 检查文件扩展名是否为.md
                if file.endswith(".md"):
                    md_file_path = os.path.join(root, file)
                    self.md_files.append(
                        RelativateDirs(
                            md_file_path, self.calculate_relative_paths(md_file_path)
                        )
                    )
                    try:
                        # 检查init.json文件是否存在于同一目录
                        init_json_path = os.path.join(root, "init.json")
                        if not os.path.isfile(init_json_path):
                            raise FileNotFoundError(
                                f"Missing init.json in the directory of {md_file_path}"
                            )
                        logger.info(f"Found init.json for md file: {md_file_path}")
                    except FileNotFoundError as e:
                        logger.error(
                            f"files not have init json: {os.path.dirname(file)}, error is: {e}"
                        )
                        continue

    def calculate_relative_paths(self, md_file: str) -> str:
        # 计算root_dir和md文件的相对路径
        md_dir_path = os.path.dirname(md_file)
        relative_path = os.path.relpath(md_dir_path, self.root_dir)
        return relative_path
