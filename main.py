import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import subprocess

# 定義視窗和元件
root = Tk()
root.title("檔案清單")
root.geometry("800x600")

file_list = ttk.Treeview(root, columns=("Size", "Date", "Path"))

scrollbar = Scrollbar(root, orient=VERTICAL, command=file_list.yview)
scrollbar.pack(side=RIGHT, fill=Y)
file_list.pack(fill=BOTH, expand=True)

file_list.configure(yscrollcommand=scrollbar.set)

file_list.heading("#0", text="檔名", command=lambda: sort_column(file_list, "#0", False))
file_list.heading("Size", text="檔案大小", command=lambda: sort_column(file_list, "Size", False))
file_list.heading("Date", text="建立日期", command=lambda: sort_column(file_list, "Date", False))
file_list.heading("Path", text="檔案路徑", command=lambda: sort_column(file_list, "Path", False))

# 詢問使用者要指定的路徑
path = filedialog.askdirectory(initialdir="/", title="選擇要遍歷的資料夾")

# 遍歷指定路徑下的所有檔案，並將它們加入清單
for dirpath, dirnames, filenames in os.walk(path):
    for filename in filenames:
        filepath = os.path.abspath(os.path.join(dirpath, filename))
        filesize = os.path.getsize(filepath)
        filedate = os.path.getctime(filepath)
        file_list.insert("", "end", text=filename, values=(filesize, filedate, filepath))

file_list.pack(fill=BOTH, expand=True)

def sort_column(tree, col, reverse):
    # 從列表中獲取數據
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    
    # 根據要排序的列轉換數據類型
    if col == "Size":
        data = [(int(size), child) for size, child in data]
    elif col == "Date":
        data = [(float(date), child) for date, child in data]
    
    # 排序數據
    data.sort(reverse=reverse)
    
    for index, (val, child) in enumerate(data):
        tree.move(child, '', index)
    
    # 切換排序方向
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

# 定義點擊清單項目右鍵時的事件處理函數
def open_file(filepath):
    subprocess.call(["explorer", "/select,", filepath])

# 定義點擊清單項目右鍵時的事件處理函數
def popup_menu(event):
    # 選取滑鼠位置的項目
    item = file_list.identify_row(event.y)
    if item:
        # 取得項目的文字
        filepath = file_list.item(item, "values")[2]
        print(filepath)
        # 建立選單
        menu = Menu(root, tearoff=0)
        # 新增"在檔案總管中開啟"選項，點擊後會使用系統預設應用程式開啟該檔案
        menu.add_command(label="在檔案總管中開啟", command=lambda: open_file(filepath))
        # 顯示選單
        menu.post(event.x_root, event.y_root)



# 綁定點擊右鍵的事件處理函數
file_list.bind("<Button-3>", popup_menu)
root.mainloop()