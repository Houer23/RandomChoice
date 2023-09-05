# -*- coding: utf-8 -*-
"""
Created on 2023年9月4日 13:36:53

@author: 李忆来
"""

import base64
import json
import random
import re
import time
import threading
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askokcancel
import tkinter.font as tkfont
import os

import ico



class RChoiceUI():
	def __init__(self, init_window):
		self.main_window = init_window
		self.norepeat_mode = tk.IntVar()
		self.auto_mode = tk.IntVar()
		self.flag_ischoosing = False
		self.origin_list = list('1234567')
		self.choice_list = self.origin_list.copy()
		self.select_list = []
		# self.lock = threading.Lock()
		self.default_name = '？？？'
		self.last_name = self.default_name
		self.name_size_range = [10,40]
		self.name_size = 28
		self.set_windows()


	def set_windows(self):

		# 低层分区，上中下三块分别用于显示设置、执行、信息等内容
		# self.frame_set = tk.LabelFrame(self.main_window)
		# self.frame_set.grid(row=0, column=0)
		# self.frame_result = tk.LabelFrame(self.main_window)
		# self.frame_result.grid(row=1, column=0)
		# self.frame_info = tk.LabelFrame(self.main_window)
		# self.frame_info.grid(row=2, column=0)

		# 设置区的控件
		self.checkbutton_norepeat = tk.Checkbutton(self.main_window, variable=self.norepeat_mode, 
			command=self.check_norepeat_change, onvalue=1, offvalue=0, 
			text='不重复点名', width=15, height=1)
		self.checkbutton_norepeat.grid(row=0, column=0, sticky='w', padx=1, pady=10)
		self.label_unrepeatCounter = tk.Label(self.main_window, 
			text='--/--', 
			width=18, height=1)
		self.label_unrepeatCounter.grid(row=0, column=1)
		self.button_reset = tk.Button(self.main_window, 
			text="复位", command=self.reset_list, 
			width=5, height=1)
		self.button_reset.grid(row=0, column=2, sticky='e', padx=10)

		# 执行区的控件
		self.label_result = tk.Label(self.main_window, 
			text='测试', font=tkfont.Font(size=self.name_size, weight='bold'),
			width=10, height=1)
		self.label_result.grid(row=1, column=0, rowspan=2, columnspan=2, pady=20)
		self.frame_start = tk.Frame(self.main_window)
		self.frame_start.grid(row=1, column=2, rowspan=2)
		self.button_start = tk.Button(self.frame_start, 
			text='开始点名', command=self.start_choice, font=tkfont.Font(size=15, slant='italic'), 
			width=10, height=1)
		self.button_start.grid(row=1, column=0, padx=10)
		self.checkbutton_auto = tk.Checkbutton(self.frame_start, variable=self.auto_mode, 
			command=self.check_auto_change, onvalue=1, offvalue=0, 
			text='自动停止')
		self.checkbutton_auto.grid(row=2, column=0)

		# 信息区的控件
		# self.frame_history = tk.Frame(self.main_window)
		# self.frame_history.grid(row=4, column=0)
		self.button_clear = tk.Button(self.main_window, 
			text='清零', command=self.clear_history, 
			width=5, height=1)
		self.button_clear.grid(row=4, column=0, sticky='w', padx=18, pady=10)
		self.label_history = tk.Label(self.main_window, 
			text='请开始点名', 
			width=25, height=1)
		self.label_history.grid(row=4, column=1, sticky='e', padx=10)
		self.frame_sizebutton = tk.Frame(self.main_window)
		self.frame_sizebutton.grid(row=4, column=2, columnspan=2)
		self.button_fontsize_more = tk.Button(self.frame_sizebutton, 
			text='+', command=lambda:self.fontsize_change(1), 
			width=1, height=1)
		self.button_fontsize_more.grid(row=0, column=0)
		self.button_fontsize_less = tk.Button(self.frame_sizebutton, 
			text='-', command=lambda:self.fontsize_change(0), 
			width=1, height=1)
		self.button_fontsize_less.grid(row=0, column=1)

		# tk.Button(self.main_window, text='测试数据', command=self.test_).grid(row=5, column=2)


	def start_choice(self):
		self.flag_ischoosing = not self.flag_ischoosing
		# print(self.flag_ischoosing)

		if self.flag_ischoosing:
			print('start')
			self.choice_name()
			if not self.auto_mode.get():
				self.button_start['text'] = '停止点名'
			else:
				delay_time = random.randrange(2,6)
				print('延迟：',delay_time)
				self.button_start['state'] = tk.DISABLED
				threading.Timer(delay_time, self.auto_choice).start()

		else:
			self.button_start['text'] = '开始点名'
			time.sleep(0.2)
			print(self.last_name)

	def choice_name(self):
		multichoice = threading.Thread(target=self.random_multichoice)
		multichoice.start() 

	def random_multichoice(self, timeflash=0.1):
		if not self.choice_list:
			name = 'ERROR'
		else:
			while True:
				name = random.choice(self.choice_list)
				# print(name)
				# with self.lock:
				self.label_result['text'] = name
				time.sleep(timeflash)
				if not self.flag_ischoosing:
					self.last_name = name
					break
			self.set_choice_result()
		return name

	def set_choice_result(self):
		self.select_list.append(self.last_name)
		self.label_history['text'] = f'总人数{len(self.origin_list)}，已点到 {len(self.select_list):0>3}名同学'
		if self.norepeat_mode.get():
			# print('lastname:', self.last_name)
			self.choice_list.remove(self.last_name)
			self.label_unrepeatCounter['text'] = f'未被点到人数：{len(self.choice_list)}/{len(self.origin_list)}'

	def auto_choice(self):
		self.flag_ischoosing = False
		self.button_start['state'] = tk.NORMAL
		self.button_start['text'] = '开始点名'

	def check_norepeat_change(self):
		if self.norepeat_mode.get():
			self.update_form(reset=True)
		# print(self.norepeat_mode.get())

	def update_form(self, reset=False):
		if reset:
			self.reset_list()
		self.label_unrepeatCounter['text'] = f'{len(self.choice_list)}/{len(self.origin_list)}'
		self.label_result['text'] = self.last_name	

	def check_auto_change(self):
		if self.auto_mode.get() and self.flag_ischoosing:
			self.button_start['state'] = tk.DISABLED
			threading.Timer(3, self.auto_choice).start()

	def reset_list(self):
		self.last_name = self.default_name
		self.label_unrepeatCounter['text'] = '--/--'
		self.clear_history()

	def clear_history(self):
		self.choice_list = self.origin_list.copy()
		self.select_list = []
		self.label_history['text'] = f'总人数{len(self.origin_list)}，请重新开始点名'
		self.label_result['text'] = self.last_name

	def fontsize_change(self, mode):
		if mode and self.name_size < self.name_size_range[1]:
			self.name_size += 2
		elif (not mode) and self.name_size >self.name_size_range[0]:
			self.name_size -= 2
		# print(self.name_size)
		self.label_result['font'] = tkfont.Font(size=self.name_size)


	def test_(self):
		print(self.norepeat_mode.get())
		print('待点名清单：', self.choice_list)

		print('最近点到的名字', self.last_name)
		print('已点到的名单', self.select_list)
		print(str(self.main_window.geometry()))



class RChoice(RChoiceUI):


	def __init__(self, init_window):
		super(RChoice, self).__init__(init_window)
		self.check_setting()
		self.load_setting()
		self.load_list()
		self.event_bind()

	def event_bind(self):
		self.label_history.bind('<Button-3>', self.show_history)
		self.label_history.bind('<Button-1>', self.select_list_file)
		self.main_window.protocol('WM_DELETE_WINDOW', self.check_setting_change)

	def check_setting(self):
		self.setting_file = 'setting.ini'
		if not os.path.exists(self.setting_file):
			self.save_setting(default=True)
		else:
			with open(self.setting_file, 'rt', encoding='utf-8') as reader:
				setting_text = reader.read()
			self.setting = json.loads(setting_text)

	def load_setting(self):
		self.list_file = self.setting['[choice_list_file]']
		self.default_name = self.setting['[default_name]']
		self.name_size = self.setting['[name_font_size]']
		self.name_size_range = list(map(int, self.setting['[name_font_size_range]'].split('-')))
		self.norepeat_mode.set(self.setting['[no_repeat_mode]'])
		self.auto_mode.set(self.setting['[auto_choice_mode]'])

	def load_list(self):
		with open(self.list_file, 'rt', encoding='utf-8') as reader:
			names = reader.read().strip().split('\n')
			print(names)
		self.origin_list = names
		self.reset_list()

	def save_setting(self, default=False):
		if default:
			self.select_list_file()
			self.default_name = '？？？'
			self.name_size = 28
			self.name_size_range = [10, 40]
			self.norepeat_mode.set(0)
			self.auto_mode.set(0)
		self.setting = {
		'[choice_list_file]': self.list_file,
		'[default_name]' : self.default_name,
		'[name_font_size]': self.name_size,
		'[name_font_size_range]': f'{self.name_size_range[0]}-{self.name_size_range[1]}', 
		'[no_repeat_mode]': self.norepeat_mode.get(),
		'[auto_choice_mode]': self.auto_mode.get()
		}
		setting_text = json.dumps(self.setting, indent=4, separators=[', ', ': '], ensure_ascii=False)
		with open(self.setting_file, 'wt', encoding='utf-8') as writer:
			writer.write(setting_text)

	def save_list(self):
		pass

	def show_history(self, event):
		print(self.select_list)

	def select_list_file(self, event=None):
		choose_file = askopenfilename(title='请选择一个名单文件', filetypes=[('文本文件', '*.txt'), ('csv列表（utf-8）', '*.csv')])
		self.list_file = choose_file

	def check_setting_change(self):
		setting_change = [
		self.setting['[choice_list_file]'] == self.list_file,
		self.setting['[default_name]'] == self.default_name,
		self.setting['[name_font_size]'] == self.name_size,
		self.setting['[name_font_size_range]'] == f'{self.name_size_range[0]}-{self.name_size_range[1]}', 
		self.setting['[no_repeat_mode]'] == self.norepeat_mode.get(),
		self.setting['[auto_choice_mode]'] == self.auto_mode.get()
		]
		if (not all(setting_change)) and askokcancel('保存提示', '系统设置有所改变，是否保存所有改变项？'):
			self.save_setting()
		self.main_window.destroy()

def load_ico(ico_name):
	if os.path.exists(ico_name):
		return
	with open(ico_name, 'wb') as fp:
		fp.write(base64.b64decode(ico.ico))

def main():
	main_windows = tk.Tk()
	main_windows.title("RandomChoice V1.0.1")
	ico_name = 'favicon.ico'
	load_ico(ico_name)
	# 设置窗口属性
	main_windows.iconbitmap(ico_name)
	main_windows.attributes('-alpha', 0.95)
	main_windows.attributes('-topmost', True)
	# 设置功能窗体
	Rchoice_main = RChoice(main_windows)
	main_windows.resizable(False, False)
	main_windows.mainloop()


if __name__ == '__main__':
	main()