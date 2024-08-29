import os
import shutil
import winreg
import subprocess
import tkinter as tk
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("《黑神话：悟空》离线补丁 辅助安装脚本")
        self.geometry("750x500")

        self.frames = {}
        self.current_frame = None
        self.spath = ""
        self.userID = None

        self.create_frames()
        self.show_frame("WelcomePage")  # 初始化时显示欢迎页面

    def create_frames(self):
        # 按照新的顺序创建页面
        page_classes = (FifthPage, FourthPage, SecondPage, WelcomePage)
        for F in page_classes:
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if self.current_frame is not None:
            self.current_frame.grid_forget()  # 隐藏当前页面
        self.current_frame = frame
        frame.grid(row=0, column=0, sticky="nsew")  # 显示新页面

    def get_steam_path(self):
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path, _ = winreg.QueryValueEx(reg_key, "SteamPath")
            winreg.CloseKey(reg_key)
            return steam_path
        except WindowsError:
            return ""

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="欢迎使用本脚本，请确保正在使用管理员权限运行\n\n"
                                    "本脚本旨在帮助游戏玩家为《黑神话：悟空》（Steam）安装一个补丁\n"
                                    "它用于对抗Denuvo反篡改（Anti-Tamper）技术。\n"
                                    "过程中可能需要支付很少的费用，是否需要付费只取决于一件事：\n"
                                    "你是否有可以借用的已经将《黑神话：悟空》正版入库的账户。\n"
                                    "如果没有则需要低价租赁，这只需要付很少的钱，\n"
                                    "我不会从中获得任何利益。\n\n"
                                    "我们开始吧，现在，请登录一个拥有《黑神话：悟空》的Steam账号，\n"
                                    "下载游戏，确保Steam处于上线模式的状态下，运行它，\n"
                                    "你不需要现在开始游玩，只需要等待着色器加载完成，然后退出它。\n\n"
                                    "现在请点击本窗口内的[下一页]按钮。",
                         font=("楷体", 16))
        label.pack(pady=20)

        next_button = tk.Button(self, text="下一页", command=lambda: controller.show_frame("SecondPage"))
        next_button.pack(side="right", padx=10, pady=10)

class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="看起来你已经完成了上一步\n\n"
                                    "由于Denuvo反篡改技术的运行机制\n"
                                    "补丁在需要每台电脑单独安装\n"
                                    "所以我并不能制作好补丁后直接拷贝到你的电脑中\n"
                                    "我需要刚刚那个通过了Denuvo反篡改技术的Steam账号的ID     \n"
                                    "不是很麻烦\n"
                                    "现在，我们需要获取你的Steam安装路径\n"
                                    "通常程序会通过注册表自动获取Steam安装路径   \n"
                                    "如果它获取错了，请修改",
                         font=("楷体", 16))

        label.pack(pady=20)

        self.path_entry = tk.Entry(self, width=70)
        self.path_entry.pack(pady=10)

        self.load_path()

        save_button = tk.Button(self, text="下一页", command=self.save_path)
        save_button.pack(side="right", padx=10, pady=10)
    def load_path(self):
        self.path_entry.delete(0, tk.END)
        steam_path = self.controller.get_steam_path()
        self.controller.spath = steam_path
        self.path_entry.insert(0, steam_path)

    def save_path(self):
        self.controller.spath = self.path_entry.get()
        self.controller.show_frame("FourthPage")

'''
class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 页面标签
        label = tk.Label(self, text="这是第3页", font=("楷体", 16))
        label.pack(pady=20)

        # “下一页”按钮
        next_button = tk.Button(self, text="下一页", command=lambda: controller.show_frame("FourthPage"))
        next_button.pack(side="right", padx=10, pady=10)

        # “备份 ACF”按钮
        backup_button = tk.Button(self, text="备份 ACF", command=self.backup_acf_files)
        backup_button.pack(side="right", padx=10, pady=10)

    def backup_acf_files(self):
        steam_path = self.controller.spath
        if not steam_path:
            messagebox.showerror("错误", "Steam 路径未设置。")
            return

        steamapps_path = os.path.join(steam_path, "steamapps")
        backup_path = os.path.join(steamapps_path, "acfbk")

        # 检查并创建备份目录
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        # 移动 .acf 文件
        moved_files = []
        for filename in os.listdir(steamapps_path):
            if filename.endswith(".acf"):
                source_path = os.path.join(steamapps_path, filename)
                destination_path = os.path.join(backup_path, filename)
                try:
                    shutil.move(source_path, destination_path)
                    moved_files.append(filename)
                except Exception as e:
                    messagebox.showerror("错误", f"移动文件 {filename} 时出错: {e}")

        if moved_files:
            messagebox.showinfo("完成", f"已备份 {len(moved_files)} 个 ACF 文件。")
        else:
            messagebox.showinfo("完成", "没有找到 ACF 文件。")
'''

class FourthPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # 页面标签
        label = tk.Label(self, text="和你想的一样\n"
                                    "点击左侧的按钮\n\n"
                                    "请注意，安装期间会弹出多个弹窗\n"
                                    "其中一个需要你确认《黑神话：悟空》的安装路径", font=("楷体", 16))
        label.pack(pady=20)

        # “下一页”按钮
        next_button = tk.Button(self, text="下一页", command=lambda: controller.show_frame("FifthPage"))
        next_button.pack(side="right", padx=10, pady=10)
        
        # 添加“读取ID→写入补丁→安装补丁”按钮
        read_id_button = tk.Button(self, text="读取ID→写入补丁→安装补丁", command=self.read_id_from_acf)
        read_id_button.pack(side="right", padx=10, pady=10)

    def read_id_from_acf(self):
        # 使用 Steam 路径
        steam_path = self.controller.spath
        if not steam_path:
            messagebox.showerror("错误", "Steam 路径未设置。")
            return

        appmanifest_path = os.path.join(steam_path, "steamapps", "appmanifest_2358720.acf")
        user_id = None

        try:
            with open(appmanifest_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 14:
                    # 读取第14行
                    line = lines[13].strip()  # 行索引从0开始
                    if "LastOwner" in line:
                        # 提取"LastOwner"的值
                        parts = line.split('"')
                        if len(parts) >= 3:
                            user_id = parts[3].strip()
                            self.controller.userID = user_id  # 保存为控制器的变量
                            messagebox.showinfo("成功", f"读取的ID是: {user_id}")
                            self.save_user_id_to_file(user_id, steam_path)
                        else:
                            messagebox.showerror("错误", "无法解析LastOwner值。")
                    else:
                        messagebox.showerror("错误", "第14行不包含LastOwner。")
                else:
                    messagebox.showerror("错误", "文件内容少于14行。")
        except FileNotFoundError:
            messagebox.showerror("错误", "appmanifest_2358720.acf 文件未找到。")
        except Exception as e:
            messagebox.showerror("错误", f"读取文件时出错: {e}")

    def save_user_id_to_file(self, user_id, steam_path):
        # 使用脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "p1", "steam_settings", "force_steamid.txt")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        try:
            with open(file_path, 'w') as file:
                file.write(user_id)
            messagebox.showinfo("成功", f"用户ID已写入到补丁")
            self.copy_crack_files_to_steam(steam_path)
        except Exception as e:
            messagebox.showerror("错误", f"写入文件时出错: {e}")

    def copy_crack_files_to_steam(self, steam_path):
        # 使用 Steam 路径
        target_path = os.path.join(steam_path, "steamapps", "common", "BlackMythWukong")
        source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "p1")
        
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
        
        try:
            # 遍历并复制源目录中的所有文件和子目录
            for item in os.listdir(source_dir):
                s = os.path.join(source_dir, item)
                d = os.path.join(target_path, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, False, None)
                else:
                    shutil.copy2(s, d)
            messagebox.showinfo("成功", f"第一部分安装完成")
        except Exception as e:
            messagebox.showerror("错误", f"复制文件时出错: {e}")
        subprocess.run('p2.exe')
class FifthPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = tk.Label(self, text="恭喜你，你成功的安装了补丁\n"
                                    "下面，你只需要运行桌面的\n 猿神启动 \n"
                                    "就能够运行游戏\n"
                                    "如果补丁没有生效，一定是大圣用他的神通阻止了你\n"
                                    "那么你就应该去购买正版游戏\n"
                                    "如果你成功了，也请记住 六耳猕猴 永远成不了 孙悟空 \n"
                                    "在你渡过自己的81难后，请记得购买 正版游戏\n\n\n"
                                    "(C)天津市第二猿神学校", font=("楷体", 16))
        label.pack(pady=20)

        end_button = tk.Button(self, text="结束", command=self.controller.destroy)
        end_button.pack(side="right", padx=10, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
