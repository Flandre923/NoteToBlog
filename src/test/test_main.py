# from src.hello_world import main 
from note_2_blog import main 
from note_2_blog.ImageHelper import ImageManager

def test_read_images():
    image_helper = ImageManager(r"D:\code\python_uv_test\hello-world\src\res")
    for i in range(5):
        print(image_helper.getImage())
        
def test_image_upload():
    github_config = main.GithubCofig()

    upload_helper = main.GitHubUploader(github_config.repo, github_config.token,"img")
    uploadfilename = upload_helper.upload(
        r"D:\code\python_uv_test\note_2_blog\src\res\images\wallhaven-jxjv3w.png"
    )
    main.logger.info(uploadfilename)
    
def test_article_replace():
    gf = main.GithubCofig()
    im = ImageManager(r"d:\code\python_uv_test\hello\src\res\images")
    gp = main.GitHubUploader(gf.repo, gf.token, "img")
    blog = main.BlogPost(
        im,
        gp,
        r"D:\code\python_uv_test\note_2_blog\src\res\md",
        r"D:\code\python_uv_test\note_2_blog\src\res\md\first\test.md",
        r"/first",
        r"D:\code\python_uv_test\note_2_blog\src\res\md_out",
    )
    blog.reslove()

def test_dirs():
    dirs = main.DirsManager(r"D:\code\python_uv_test\note_2_blog\src\res\md", "./")
    print(dirs.__dict__)
    