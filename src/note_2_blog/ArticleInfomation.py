import json
import os
from typing import List

from loguru import logger

from note_2_blog.GitHubUploader import GitHubUploader
from note_2_blog.ImageHelper import ImageManager


class SharedMetadata:
    # 通过JSON序列化共享的元数据
    def __init__(
        self, published: str, tags: List[str], description: str, category: str
    ):
        self.published = published
        self.tags = tags
        self.description = description
        self.category = category

    def to_json(self):
        # 将对象序列化为JSON字符串
        return json.dumps(self.__dict__)


class BlogPost:
    # 博客文章的特定属性
    def __init__(
        self,
        image_manager: ImageManager,
        uploader: GitHubUploader,
        root_path: str,
        file_path: str,
        relative_path: str,
        out_path: str,
        is_appned_content: bool,
    ):
        self.image_manager: ImageManager = image_manager
        self.uploader: GitHubUploader = uploader
        self.title: str  # 标题
        self.file_name: str
        self.image_path: str = root_path  # 图片
        self.draft: str = "false"  # false
        self.root_path: str  # root 文件夹的路径
        self.relative_path: str = relative_path  # 文件相对 root 文件夹的路径
        self.file_path: str = file_path  # 文件的路径
        self.out_path: str = out_path  # 输出root的路径
        self.shared_metadata: SharedMetadata  # 共享的元数据
        self.is_append_content: bool = is_appned_content  # 是否在结尾追加内容

    def __str__(self):
        return (
            f"Title: {self.title}\n"
            f"Image: {self.image}\n"
            f"Draft: {self.draft}\n"
            f"Shared Metadata: {self.shared_metadata.to_json()}"
        )

    def reslove(self) -> None:
        # 1. 给发出地址切分出文件名
        # 2. 将获得的文件名去掉空格和非法字符作为title
        # 2. 读取file所在目录下的init.json 文件的内容
        # 3. 序列化为SharedMetadata对象
        # 4. 通过图片管理的类获得一张图片
        # 5. 将图片上传到github 获得 连接
        # 6. 读取文件的内容，
        # 7. 找到本地图片的路径
        # 8. 将本地图片上传到github
        # 9. 使用获得的链接替换掉本地连接
        # 10 将文章输出到指定文件相同的子目录下
        logger.info("Resolving blog post processing...")
        try:
            file_name = os.path.basename(self.file_path)
            self.title = file_name.replace(".md", "").strip()
            self.file_name = self.title.replace(" ", "_").replace("-", "_")
            init_file_path = os.path.join(os.path.dirname(self.file_path), "init.json")
            with open(init_file_path, "r", encoding="utf-8") as f:
                init_data = json.load(f)
                self.shared_metadata = SharedMetadata(**init_data)
            self.image_path = self.uploader.upload(self.image_manager.getImage())
            updated_content = self._markdown_content_replace()
            output_file_path = os.path.join(
                os.path.join(self.out_path, self.relative_path), f"{self.file_name}.md"
            )
            # 如果output_file_path不存在，则创建
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            logger.info(f"Blog post written to {output_file_path}")
        except Exception as e:
            logger.error(f"Error resolving blog post: {e}")

    def _markdown_content_replace(self) -> str:
        """
        读取markdown文件的内容，将其中的所有本地的图片上传到图床，并用上传后的地址替换本地的地址，将替换后的内容返回
        """
        logger.debug("Starting markdown content replacement...")
        try:
            # 读取Markdown文件的内容
            with open(self.file_path, "r", encoding="utf-8") as file:
                markdown_content = file.read()

            # 分割文件内容为行
            lines = markdown_content.splitlines()

            # 新的Markdown内容列表
            updated_lines = []

            # 遍历每一行
            for line in lines:
                # 检查是否是图片链接
                if "![" in line:
                    # 找到所有可能的链接（考虑到一行可能有多个图片）
                    start_link_index = 0
                    while start_link_index < len(line):
                        # 查找图片链接的起始位置
                        start_img_index = line.find("![", start_link_index)
                        if start_img_index == -1:
                            break
                        # 查找图片链接的结束位置
                        end_img_index = line.find("](", start_img_index)
                        if end_img_index == -1:
                            break
                        end_url_index = line.find(")", end_img_index + 2)
                        if end_url_index == -1:
                            break

                        # 提取图片链接
                        img_link = line[end_img_index + 2 : end_url_index]
                        img_link = os.path.join(
                            os.path.dirname(self.file_path), img_link
                        )
                        # 上传图片并获取GitHub链接
                        github_img_url = self.uploader.upload(img_link)
                        # 替换Markdown中的图片链接
                        line = (
                            line[: end_img_index + 2]
                            + github_img_url
                            + line[end_url_index:]
                        )
                        # 更新链接查找的起始位置
                        start_link_index = end_url_index + 1

                # 添加处理后的行到新的内容列表
                updated_lines.append(line)
            # 将新的内容列表合并为字符串
            if self.is_append_content:
                updated_content = (
                    self._gen_prefix()
                    + "\n".join(updated_lines)
                    + self._append_content()
                )
            else:
                updated_content = self._gen_prefix() + "\n".join(updated_lines)

            # 返回更新后的Markdown内容
            return updated_content
        except Exception:
            logger.exception("Error in markdown content replacement")

    def _gen_prefix(self) -> str:
        logger.debug("Generating YAML front matter for markdown...")
        try:
            if (
                self.file_name is None
                or self.title is None
                or self.shared_metadata is None
                or self.image_path is None
            ):
                raise Exception("title or shared_metadata or image_path is None")
            return f"""---
title: {self.title}
published: {self.shared_metadata.published}
tags: {self.shared_metadata.tags}
description: {self.shared_metadata.description}
image: {self.image_path}
category: {self.shared_metadata.category}
draft: false
---


"""
        except Exception as e:
            logger.error(f"Error generating YAML front matter: {e}")

    def _append_content(self) -> str:
        return """

---
本文是个人学习记录，如果有侵权请联系后删除。
"""
