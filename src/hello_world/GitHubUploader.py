from typing import Tuple
import requests
import base64
import json
import uuid
import os
from loguru import logger


class GitHubUploader:
    def __init__(
        self, repo_path: str, token: str, path: str, cache_file="upload_cache.json"
    ):
        """
        初始化GitHubUploader对象。
        
        :param repo_path: GitHub仓库路径，格式为"用户名/仓库名"。
        :param token: GitHub访问令牌。
        :param path: 保存仓库的路径
        """
        self.ext = ""
        self.repo_path = repo_path
        self.token = token
        self.path = path
        self.cache_file = cache_file
        self.cache = self._load_cache()  # 加载缓存
        logger.info("GitHubUploader initialized with cache")

    def _load_cache(self):
        """从文件加载缓存"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        """将缓存保存到文件"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f)

    def upload(self, file_path: str) -> Tuple[str,str]:
        """
        上传文件到GitHub仓库。
        
        :param file_path: 要上传的文件的本地路径。
        :return: 上传成功后返回的文件名。
        """
        response = ""
        try:
            file_key = self._file_base64(file_path.encode())  # 使用文件路径作为键
            if file_key in self.cache:
                logger.info(f"File {file_path} found in cache. Returning cached URL.")
                return f"https://cdn.jsdelivr.net/gh/{self.repo_path}/{self.path}/{self.cache[file_key]}"

            self.ext = os.path.splitext(file_path)[1]
            with open(file_path, "rb") as f:
                fdata_tmp = self._file_base64(f.read())
                response, file_name = self._upload_file(fdata_tmp)
                self.cache[file_key] = file_name  # 更新缓存
                self._save_cache()  # 保存缓存到文件
                logger.info(f"File {file_path} uploaded successfully as {file_name}")
                return f"https://cdn.jsdelivr.net/gh/{self.repo_path}/{self.path}/{file_name}"
        except Exception as e:
            logger.error(f"github upload response:{response}")
            logger.error(f"Failed to upload {file_path}: {e}")
            return ""

    def _file_base64(self, data: bytes) -> str:
        """
        将文件数据转换为base64编码。

        :param data: 文件的二进制数据。
        :return: base64编码的字符串。
        """
        return base64.b64encode(data).decode()

    def _upload_file(self, file_data: str) -> Tuple[str, str]:
        """
        上传文件到GitHub API。
        
        :param file_data: 文件的base64编码字符串。
        :return: API响应和文件名。
        """
        file_name = str(uuid.uuid1()) + self.ext
        headers = {"Authorization": f"token {self.token}"}
        url = f"https://api.github.com/repos/{self.repo_path}/contents/{self.path}/{file_name}"
        data = {"message": "upload pictures", "content": file_data}
        data = json.dumps(data)
        try:
            response = requests.put(url, data=data, headers=headers)
            response.raise_for_status()  # 确保请求成功
            return response.json(), file_name
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            raise
        
