import sys
import ctypes
import datetime
import tkinter as tk
import random
from tkinter import ttk, messagebox

class TimeChangerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("系统时间修改器")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # 检查管理员权限
        if not self.is_admin():
            messagebox.showwarning("权限不足", "此程序需要管理员权限才能修改系统时间。\n请以管理员身份重新运行。")
            self.root.destroy()
            return
        
        self.create_widgets()
        self.update_time_display()
        
        # 设置定时器更新当前时间显示
        self.update_time()
    
    def is_admin(self):
        """检查是否以管理员权限运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def create_widgets(self):
        """创建界面组件"""
        # 设置样式
        style = ttk.Style()
        style.configure('TButton', font=('微软雅黑', 10))
        style.configure('TLabel', font=('微软雅黑', 10))
        style.configure('Header.TLabel', font=('微软雅黑', 12, 'bold'))
        
        # 创建框架
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 当前时间显示
        time_frame = ttk.LabelFrame(main_frame, text="当前系统时间", padding="10 5 10 10")
        time_frame.pack(fill=tk.X, pady=5)
        
        self.time_var = tk.StringVar()
        time_label = ttk.Label(time_frame, textvariable=self.time_var, 
                              font=("Consolas", 18, "bold"), foreground="blue")
        time_label.pack(pady=5)
        
        # 设置时间区域
        set_frame = ttk.LabelFrame(main_frame, text="设置时间", padding="10 5 10 10")
        set_frame.pack(fill=tk.X, pady=5)
        
        # 时间选择器
        ttk.Label(set_frame, text="选择日期和时间:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.date_entry = ttk.Entry(set_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        
        self.time_entry = ttk.Entry(set_frame, width=8)
        self.time_entry.grid(row=0, column=2, padx=5, pady=5)
        self.time_entry.insert(0, datetime.datetime.now().strftime("%H:%M:%S"))
        
        set_button = ttk.Button(set_frame, text="设置时间", command=self.set_time)
        set_button.grid(row=0, column=3, padx=10, pady=5)
        
        # 时间调整区域
        adjust_frame = ttk.LabelFrame(main_frame, text="调整时间", padding="10 5 10 10")
        adjust_frame.pack(fill=tk.X, pady=5)
        
        # 增加时间
        ttk.Label(adjust_frame, text="增加时间:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.add_minutes_var = tk.StringVar(value="1")
        add_minutes = ttk.Spinbox(adjust_frame, from_=1, to=60, width=5, textvariable=self.add_minutes_var)
        add_minutes.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(adjust_frame, text="分钟").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        add_minutes_btn = ttk.Button(adjust_frame, text="增加分钟", 
                                    command=lambda: self.adjust_time(minutes=int(self.add_minutes_var.get())))
        add_minutes_btn.grid(row=0, column=3, padx=10, pady=5)
        
        self.add_seconds_var = tk.StringVar(value="10")
        add_seconds = ttk.Spinbox(adjust_frame, from_=1, to=60, width=5, textvariable=self.add_seconds_var)
        add_seconds.grid(row=0, column=4, padx=5, pady=5)
        ttk.Label(adjust_frame, text="秒").grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        
        add_seconds_btn = ttk.Button(adjust_frame, text="增加秒钟", 
                                    command=lambda: self.adjust_time(seconds=int(self.add_seconds_var.get())))
        add_seconds_btn.grid(row=0, column=6, padx=10, pady=5)
        
        # 减少时间
        ttk.Label(adjust_frame, text="减少时间:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.sub_minutes_var = tk.StringVar(value="1")
        sub_minutes = ttk.Spinbox(adjust_frame, from_=1, to=60, width=5, textvariable=self.sub_minutes_var)
        sub_minutes.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(adjust_frame, text="分钟").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        
        sub_minutes_btn = ttk.Button(adjust_frame, text="减少分钟", 
                                    command=lambda: self.adjust_time(minutes=-int(self.sub_minutes_var.get())))
        sub_minutes_btn.grid(row=1, column=3, padx=10, pady=5)
        
        self.sub_seconds_var = tk.StringVar(value="10")
        sub_seconds = ttk.Spinbox(adjust_frame, from_=1, to=60, width=5, textvariable=self.sub_seconds_var)
        sub_seconds.grid(row=1, column=4, padx=5, pady=5)
        ttk.Label(adjust_frame, text="秒").grid(row=1, column=5, padx=5, pady=5, sticky=tk.W)
        
        sub_seconds_btn = ttk.Button(adjust_frame, text="减少秒钟", 
                                    command=lambda: self.adjust_time(seconds=-int(self.sub_seconds_var.get())))
        sub_seconds_btn.grid(row=1, column=6, padx=10, pady=5)
        
        # 随机时间增加区域（修改后的功能）
        random_frame = ttk.LabelFrame(main_frame, text="随机时间增加", padding="10 5 10 10")
        random_frame.pack(fill=tk.X, pady=5)
        
        # 分钟随机范围
        ttk.Label(random_frame, text="分钟范围:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.min_minutes_var = tk.StringVar(value="1")
        min_minutes = ttk.Spinbox(random_frame, from_=1, to=60, width=5, textvariable=self.min_minutes_var)
        min_minutes.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(random_frame, text="到").grid(row=0, column=2, padx=5, pady=5)
        
        self.max_minutes_var = tk.StringVar(value="10")
        max_minutes = ttk.Spinbox(random_frame, from_=1, to=60, width=5, textvariable=self.max_minutes_var)
        max_minutes.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(random_frame, text="分钟").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        
        # 秒随机范围
        ttk.Label(random_frame, text="秒范围:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.min_seconds_var = tk.StringVar(value="10")
        min_seconds = ttk.Spinbox(random_frame, from_=1, to=60, width=5, textvariable=self.min_seconds_var)
        min_seconds.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(random_frame, text="到").grid(row=1, column=2, padx=5, pady=5)
        
        self.max_seconds_var = tk.StringVar(value="30")
        max_seconds = ttk.Spinbox(random_frame, from_=1, to=60, width=5, textvariable=self.max_seconds_var)
        max_seconds.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(random_frame, text="秒").grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        
        # 生成随机时间并增加按钮
        random_btn = ttk.Button(random_frame, text="生成随机值并增加", command=self.random_increase)
        random_btn.grid(row=0, column=5, rowspan=2, padx=10, pady=5, sticky=tk.NS)
        
        # 底部按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        refresh_btn = ttk.Button(button_frame, text="刷新时间", command=self.update_time_display)
        refresh_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = ttk.Button(button_frame, text="退出程序", command=self.root.destroy)
        exit_btn.pack(side=tk.RIGHT, padx=10)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_time(self):
        """更新时间显示"""
        self.update_time_display()
        self.root.after(1000, self.update_time)  # 每秒更新一次
    
    def update_time_display(self):
        """更新当前时间显示"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_var.set(current_time)
    
    def set_time(self):
        """设置系统时间"""
        try:
            date_str = self.date_entry.get()
            time_str = self.time_entry.get()
            datetime_str = f"{date_str} {time_str}"
            new_time = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
            
            # 调用设置时间函数
            if self.set_system_time(new_time):
                self.status_var.set(f"时间已设置为: {datetime_str}")
                self.update_time_display()
            else:
                messagebox.showerror("错误", "设置系统时间失败")
        except ValueError:
            messagebox.showerror("错误", "无效的日期或时间格式\n请使用 YYYY-MM-DD 和 HH:MM:SS 格式")
    
    def adjust_time(self, minutes=0, seconds=0):
        """调整系统时间"""
        try:
            # 计算新时间
            current_time = datetime.datetime.now()
            new_time = current_time + datetime.timedelta(minutes=minutes, seconds=seconds)
            
            # 调用设置时间函数
            if self.set_system_time(new_time):
                if minutes > 0 or seconds > 0:
                    self.status_var.set(f"时间已增加: {minutes}分 {seconds}秒")
                elif minutes < 0 or seconds < 0:
                    self.status_var.set(f"时间已减少: {abs(minutes)}分 {abs(seconds)}秒")
                else:
                    self.status_var.set("时间未调整")
                self.update_time_display()
            else:
                messagebox.showerror("错误", "调整系统时间失败")
        except Exception as e:
            messagebox.showerror("错误", f"调整时间时发生错误: {str(e)}")
    
    def random_increase(self):
        """随机增加时间（仅为正数）"""
        try:
            # 获取分钟和秒的随机范围
            min_minutes = int(self.min_minutes_var.get())
            max_minutes = int(self.max_minutes_var.get())
            min_seconds = int(self.min_seconds_var.get())
            max_seconds = int(self.max_seconds_var.get())
            
            # 验证范围有效性
            if min_minutes > max_minutes or min_seconds > max_seconds:
                messagebox.showerror("错误", "最小值不能大于最大值")
                return
                
            if min_minutes < 0 or max_minutes < 0 or min_seconds < 0 or max_seconds < 0:
                messagebox.showerror("错误", "范围值不能为负数")
                return
                
            # 生成随机分钟和秒
            random_minutes = random.randint(min_minutes, max_minutes)
            random_seconds = random.randint(min_seconds, max_seconds)
            
            # 仅增加时间
            self.status_var.set(f"随机增加: {random_minutes}分 {random_seconds}秒")
            self.adjust_time(minutes=random_minutes, seconds=random_seconds)
                
        except Exception as e:
            messagebox.showerror("错误", f"随机增加时间时发生错误: {str(e)}")
    
    def set_system_time(self, new_time):
        """设置系统时间（Windows API）"""
        try:
            # 定义SYSTEMTIME结构
            class SYSTEMTIME(ctypes.Structure):
                _fields_ = [
                    ('wYear', ctypes.c_ushort),
                    ('wMonth', ctypes.c_ushort),
                    ('wDayOfWeek', ctypes.c_ushort),
                    ('wDay', ctypes.c_ushort),
                    ('wHour', ctypes.c_ushort),
                    ('wMinute', ctypes.c_ushort),
                    ('wSecond', ctypes.c_ushort),
                    ('wMilliseconds', ctypes.c_ushort)
                ]
            
            # 设置系统时间
            kernel32 = ctypes.windll.kernel32
            system_time = SYSTEMTIME()
            system_time.wYear = new_time.year
            system_time.wMonth = new_time.month
            system_time.wDay = new_time.day
            system_time.wHour = new_time.hour
            system_time.wMinute = new_time.minute
            system_time.wSecond = new_time.second
            system_time.wMilliseconds = 0
            
            # 调用SetLocalTime
            result = kernel32.SetLocalTime(ctypes.byref(system_time))
            if result == 0:
                error_code = ctypes.windll.kernel32.GetLastError()
                self.status_var.set(f"设置时间失败 (错误代码: {error_code})")
                return False
            
            # 强制刷新系统时间
            kernel32.SetSystemTimeAdjustment(0, True)
            return True
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeChangerApp(root)
    root.mainloop()