import pyautogui
import pyperclip
import time
import keyboard
import threading
from tkinter import *
from tkinter import messagebox

# 定义全局变量，用于控制循环是否继续
continue_loop = False
# 创建一个锁来保证线程安全
loop_lock = threading.Lock()

def action1():
    pyautogui.moveTo(114, 270, duration=0)
    time.sleep(0.02) 
    pyautogui.click(button='right')
    time.sleep(0.02)  
    pyautogui.moveTo(331, 433, duration=0)
    time.sleep(0.02)  # 延迟20毫秒
    pyautogui.click(button='left')
    time.sleep(0.02)  
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.02) 
    clipboard_text = pyperclip.paste()
    return clipboard_text

def action2():
    # 定义动作2的具体操作，例如：
    pyautogui.moveTo(435, 509, duration=0)
    time.sleep(0.02)  
    pyautogui.click(button='right')
    time.sleep(0.02)  
    pyautogui.moveTo(329, 448, duration=0)
    time.sleep(0.02)  
    pyautogui.click(button='left')
    time.sleep(0.02)  
    pyautogui.moveTo(491, 271, duration=0)
    time.sleep(0.02)  
    pyautogui.click(button='right')
    time.sleep(0.02)  
    pyautogui.moveTo(329, 448, duration=0)
    time.sleep(0.02)  
    pyautogui.click(button='left')
    time.sleep(0.02)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.02)  
    clipboard_text = pyperclip.paste()
    return clipboard_text

def on_key():
    global continue_loop
    with loop_lock:
        if continue_loop:
            continue_loop = False
            return
        continue_loop = True
        threading.Thread(target=automation_loop, daemon=True).start()

def automation_loop():
    global continue_loop
    while True:
        with loop_lock:
            if not continue_loop:
                break

        # 根据选中的单选框决定执行的动作
        if action_var.get() == 1:
            clipboard_text = action1()
        else:
            clipboard_text = action2()

        # 判断蓝色输入框和红色输入框
        x = 0
        try:
            x = int(x_entry.get())
        except ValueError:
            pass  # 如果 x 的值不是有效的整数，则默认为 0

        first_column_match = False
        if first_column_entries:  # 只有在有蓝色输入框时才进行判断
            first_column_matches = sum(1 for entry in first_column_entries if entry.get() and entry.get() in clipboard_text)
            first_column_match = first_column_matches >= x

        all_second_column_match = True
        if second_column_entries:  # 只有在有红色输入框时才进行判断
            all_second_column_match = True  # 假设所有输入框都匹配
            for entry in second_column_entries:
                if entry.get() and entry.get() not in clipboard_text:
                    all_second_column_match = False  # 只要有一个不匹配，就标记为 False
                    break  # 不需要再继续检查了

        if (not first_column_entries or first_column_match) and (not second_column_entries or all_second_column_match):
            with loop_lock:
                continue_loop = False
            messagebox.showinfo("提示", "改造成功：" + clipboard_text)
            return

def add_entry(column_entries, color):
    entry = Entry(root, bg=color)
    entry.pack(padx=5, pady=5, side=TOP)  # 竖着排列
    column_entries.append(entry)

def remove_entry(column_entries):
    if column_entries:
        entry = column_entries.pop()
        entry.destroy()

# 创建 Tkinter 窗口
root = Tk()
root.title("剪贴板文本匹配工具")  # 设置窗口标题

# 创建两个 Frame 来分隔蓝色和红色的输入框
first_column_frame = Frame(root)
first_column_frame.pack(side=LEFT, padx=10, pady=10, fill=Y)  # 左侧 Frame

second_column_frame = Frame(root)
second_column_frame.pack(side=RIGHT, padx=10, pady=10, fill=Y)  # 右侧 Frame

# 蓝色的输入框和按钮
first_column_label = Label(first_column_frame, text="蓝色输入框")
first_column_label.pack()

first_column_entries = []
add_first_column_button = Button(first_column_frame, text="添加蓝色输入框", command=lambda: add_entry(first_column_entries, "blue"))
add_first_column_button.pack()

remove_first_column_button = Button(first_column_frame, text="删除蓝色输入框", command=lambda: remove_entry(first_column_entries))
remove_first_column_button.pack()

# 红色的输入框和按钮
second_column_label = Label(second_column_frame, text="红色输入框")
second_column_label.pack()

second_column_entries = []
add_second_column_button = Button(second_column_frame, text="添加红色输入框", command=lambda: add_entry(second_column_entries, "red"))
add_second_column_button.pack()

remove_second_column_button = Button(second_column_frame, text="删除红色输入框", command=lambda: remove_entry(second_column_entries))
remove_second_column_button.pack()

# x 值的输入框
x_label = Label(root, text="至少匹配 x 条蓝色文本")
x_label.pack(padx=10, pady=5)

x_entry = Entry(root, bg="green")
x_entry.pack(padx=10, pady=5)
x_entry.insert(0, "0")  # 默认值为 0

# 动作选择的单选框
action_var = IntVar(value=1)  # 默认选择第一个单选框

action1_radio = Radiobutton(root, text="动作1", variable=action_var, value=1)
action1_radio.pack(padx=10, pady=5)

action2_radio = Radiobutton(root, text="动作2", variable=action_var, value=2)
action2_radio.pack(padx=10, pady=5)

# 信息提示标签
info_label = Label(root, text="剪贴板文本需要匹配蓝色的至少 x 条文本内容，且匹配红色的所有输入框内容")
info_label.pack(padx=10, pady=10)

# 绑定全局热键
keyboard.add_hotkey('[', on_key)

# 运行主循环
root.mainloop()
