import os

from dotenv import load_dotenv

from note_2_blog.ArticleInfomation import BlogPost
from note_2_blog.DirsManager import DirsManager
from note_2_blog.GitHubUploader import GitHubUploader
from note_2_blog.GUI import run
from note_2_blog.ImageHelper import ImageManager

load_dotenv()


class GithubCofig:
    def __init__(self) -> None:
        self.token = os.getenv("TOKEN")
        self.repo = os.getenv("REPO")


def execute_wrapper():
    github_config = GithubCofig()
    upload_helper = GitHubUploader(github_config.repo, github_config.token, "img")

    def execute(input_path: str, output: str, img: str, is_append: bool) -> None:
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
                is_append,
            ).reslove()

    return execute


if __name__ == "__main__":
    function_execute = execute_wrapper()
    run(function_execute)
