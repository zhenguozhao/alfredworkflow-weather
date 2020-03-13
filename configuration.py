#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置信息操作
"""

import Tkinter
import tkMessageBox as messagebox

class Configuration(object):
    # 配置信息文件
    __file = "config.py"

    # 读取配置信息
    def get(self):
        self.__get_frame = Tkinter.Tk()
        self.__get_frame.title("配置信息")
        self.__get_frame.geometry("386x116")
        self.__get_label = Tkinter.Label(self.__get_frame, text="认证key：")
        self.__get_label.place(x=20, y=20, width=60)
        self.__get_entry = Tkinter.Label(self.__get_frame, text=self.get_content())
        self.__get_entry.place(x=86, y=20, width=280)
        self.__get_button = Tkinter.Button(self.__get_frame, text="关闭", command=self.__get_frame.quit)
        self.__get_button.place(x=266, y=68, width="100")
        self.__get_frame.mainloop()

    def get_content(self):
        return self.__read()

    # 设置配置信息
    def set(self):
        self.__set_frame = Tkinter.Tk()
        self.__set_frame.title("配置信息")
        self.__set_frame.geometry("386x116")
        self.__set_label = Tkinter.Label(self.__set_frame, text="认证key：")
        self.__set_label.place(x=20, y=20, width=60)
        self.__set_entry = Tkinter.Entry(self.__set_frame)
        self.__set_entry.insert(0, self.get_content())
        self.__set_entry.place(x=86, y=20, width=280)
        self.__set_button = Tkinter.Button(self.__set_frame, text="保存", command=self.__set_save)
        self.__set_button.place(x=266, y=68, width="100")
        self.__set_frame.mainloop()

    def __set_save(self):
        key = self.__set_entry.get() or None
        if key is not None and 32 <= len(key):
            self.__write(key)
            messagebox.showerror("信息", "配置已保存。")
            self.__set_frame.quit()
        else:
            messagebox.showerror("错误", "请填写有效的认证key！")

    # 读取配置文件信息
    def __read(self):
        with open(self.__file, "r") as file:
            content = file.read()
        return content[7:-2]

    # 写入配置文件信息
    def __write(self, data):
        with open(self.__file, "w") as file:
            file.write("KEY = \"%s\"\n" % data[:32])
