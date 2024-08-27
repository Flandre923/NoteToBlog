from typing import List
from loguru import logger
from dotenv import load_dotenv
from hello_world.ArticleInfomation import BlogPost
from hello_world.DirsManager import DirsManager
from hello_world.GitHubUploader import GitHubUploader
import os

from hello_world.ImageHelper import ImageManager

load_dotenv()


class GithubCofig:
    def __init__(self) -> None:
        self.token = os.getenv("TOKEN")
        self.repo = os.getenv("REPO")


def read_md(file_path: str) -> List[None]:
    logger.info(f"read md file {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        return lines


def write_md(file_path: str, lines: List[str]) -> None:
    logger.info(f"write md file {file_path}")
    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)


if __name__ == "__main__":
    github_config = GithubCofig()
    upload_helper = GitHubUploader(github_config.repo, github_config.token, "img")
    image_manager = ImageManager(r"C:\Users\flan\Downloads\python_md\img")
    dirs = DirsManager(
        root_dir=r"C:\Users\flan\Downloads\python_md\a",
        output=r"C:\Users\flan\Downloads\python_md\b",
    )
    for md_file in dirs.md_files:
        BlogPost(
            image_manager,
            upload_helper,
            dirs.root_dir,
            md_file.file_path,
            md_file.relative_path,
            dirs.out_put,
        ).reslove()
