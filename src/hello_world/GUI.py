import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable

class PathChooser:
    def __init__(self, root: tk.Tk,main:Callable[[str,str,str],None]):
        self.root = root
        self.root.title("路径选择器")

        # 创建变量来存储路径
        self.input_folder_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()
        self.image_path = tk.StringVar()

        # 创建文本框和按钮
        self.input_folder_text = tk.Text(self.root, height=1, width=50)
        self.input_folder_button = tk.Button(self.root, text="选择输入文件夹", command=self.choose_input_folder)
        self.output_folder_text = tk.Text(self.root, height=1, width=50)
        self.output_folder_button = tk.Button(self.root, text="选择输出文件夹", command=self.choose_output_folder)
        self.image_path_text = tk.Text(self.root, height=1, width=50)
        self.image_path_button = tk.Button(self.root, text="选择图片路径", command=self.choose_image_path)
        self.start_button = tk.Button(self.root, text="开始", command=self.start_process)

        # 布局
        self.input_folder_text.grid(row=0, column=1, padx=10, pady=10)
        self.input_folder_button.grid(row=0, column=0, padx=10, pady=10)
        self.output_folder_text.grid(row=1, column=1, padx=10, pady=10)
        self.output_folder_button.grid(row=1, column=0, padx=10, pady=10)
        self.image_path_text.grid(row=2, column=1, padx=10, pady=10)
        self.image_path_button.grid(row=2, column=0, padx=10, pady=10)
        self.start_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.main:Callable[[str,str,str],None] = main
        
    def choose_input_folder(self):
        folder_path = filedialog.askdirectory()
        self.input_folder_text.delete(1.0, tk.END)
        self.input_folder_text.insert(1.0, folder_path)
        self.input_folder_path.set(folder_path)

    def choose_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder_text.delete(1.0, tk.END)
        self.output_folder_text.insert(1.0, folder_path)
        self.output_folder_path.set(folder_path)

    def choose_image_path(self):
        image_path = filedialog.askdirectory()
        self.image_path_text.delete(1.0, tk.END)
        self.image_path_text.insert(1.0, image_path)
        self.image_path.set(image_path)

    def start_process(self):
        # 这里假设 main 函数定义在其他地方，并将在此处调用
        if self.main is not None and self.input_folder_path.get() !="" and self.output_folder_path.get() !="" and self.image_path.get() !="":
            self.main(self.input_folder_path.get(),self.output_folder_path.get(),self.image_path.get())
        messagebox.showinfo("完成", "处理完成")


def run(main:Callable[[str,str,str],None]):
    # 创建主窗口
    root = tk.Tk()
    # 创建 PathChooser 实例
    chooser = PathChooser(root,main)
    # 运行主循环
    root.mainloop()