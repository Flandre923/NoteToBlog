import os

from dotenv import load_dotenv

from hello_world.ArticleInfomation import BlogPost
from hello_world.DirsManager import DirsManager
from hello_world.GitHubUploader import GitHubUploader
from hello_world.GUI import run
from hello_world.ImageHelper import ImageManager

load_dotenv()


class GithubCofig:
    def __init__(self) -> None:
        self.token = os.getenv("TOKEN")
        self.repo = os.getenv("REPO")


def execute_wrapper():
    github_config = GithubCofig()
    upload_helper = GitHubUploader(github_config.repo, github_config.token, "img")

    def execute(input_path: str, output: str, img: str) -> None:
        image_manager = ImageManager(img)
        dirs = DirsManager(root_dir=input_path, output=output)
        for md_file in dirs.md_files:
            BlogPost(
                image_manager,
                upload_helper,
                dirs.root_dir,
                md_file.file_path,
                md_file.relative_path,
                dirs.out_put,
            ).reslove()

    return execute


if __name__ == "__main__":
    function_execute = execute_wrapper()
    run(function_execute)
