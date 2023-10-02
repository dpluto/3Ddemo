import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import detect111  # 确保detect0.py在同一个目录下
import sys  # 用于重定向stdout


class MainApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # 设置主窗口的默认大小
        self.window.geometry('1200x760')  # 例如，设置为800x600像素

        self.video_source = None  # 初始时不启动摄像头

        # 使用place方法调整Canvas部件的位置
        self.canvas = Canvas(window, width=760, height=540)
        self.canvas.place(x=50, y=10)  # 使用x和y参数来指定Canvas部件的位置

        # 使用place方法调整按钮的位置
        self.btn_start = tk.Button(window, text="Start", width=10, command=self.start_camera)
        self.btn_start.place(x=1000, y=600)  # 使用x和y参数来指定按钮的位置

        # 添加一个Text部件来显示detect0.py的输出
        self.output_box = tk.Text(window, height=30, width=40)  # 你可以根据需要调整height和width的值
        self.output_box.place(x=850, y=10)  # 你可以根据需要调整x和y的值

        # 重定向stdout，使得所有打印到控制台的内容都会被写入到Text部件中
        sys.stdout = self

        self.delay = 10

        self.window.mainloop()

    def start_camera(self):
        if not self.video_source:  # 如果摄像头还没启动
            self.video_source = detect111.detect()  # 创建摄像头帧的生成器
            self.update()  # 开始更新

    def update(self):
        frame = next(self.video_source, None)  # 获取下一个摄像头帧，如果没有更多帧，则返回None

        if frame is not None:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.window.after(self.delay, self.update)  # 继续更新

    def write(self, s):
        self.output_box.insert(tk.END, s)
        self.output_box.see(tk.END)  # 自动滚动到最后一行

    def flush(self):
        # 这个方法是为了满足sys.stdout的接口要求，实际上我们不需要实现任何功能
        pass


root = tk.Tk()
app = MainApp(root, "Main App")