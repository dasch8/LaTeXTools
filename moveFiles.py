# ST2/ST3 compat
from __future__ import print_function 
import sublime
import shutil
if sublime.version() < '3000':
    # we are on ST2 and Python 2.X
	_ST3 = False
	import getTeXRoot
else:
	_ST3 = True
	from . import getTeXRoot


import sublime_plugin, os.path, subprocess, time


class move_filesCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		# get the root filename
		self.file_name = getTeXRoot.get_tex_root(self.view)
		if not os.path.isfile(self.file_name):
			sublime.error_message(self.file_name + ": file not found.")
			return

		self.tex_base, self.tex_ext = os.path.splitext(self.file_name)

		# load the output settings
		output_settings = sublime.load_settings("LaTeXTools.sublime-settings").get("output_settings")

		# root directory path
		dir_path = os.path.dirname(self.file_name)

		for move_entry in output_settings:
			move_path = move_entry.get("path")
			move_exts = move_entry.get("exts")
			if move_path!=None and move_exts!=None:
				# destination folder
				dest_dir = os.path.normpath(os.path.join(dir_path,move_path))
				# create destionation folder if not already exists
				if not os.path.exists(dest_dir):
					os.mkdir(dest_dir)
				for ext in move_exts:
					# move files specified in the extension settings if existing
					file_to_move = self.tex_base + ext
					if os.path.exists(file_to_move):
						file_name_to_move = os.path.basename(file_to_move)
						dest_path = os.path.normpath(os.path.join(dir_path,move_path,file_name_to_move))
						print("moving file "+file_to_move+"->"+dest_path)
						shutil.move(file_to_move,dest_path)

		