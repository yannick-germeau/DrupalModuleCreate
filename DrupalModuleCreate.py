import sublime, sublime_plugin
import os, shutil
import pprint

def Window():
	return sublime.active_window()

class DmcreateCommand(sublime_plugin.WindowCommand):
	def run(self, paths = [], name = ""):
		import functools
		#Window().run_command('hide_panel');
		Window().show_input_panel("Module Name:", name, functools.partial(self.on_done, paths), None, None)

	def on_done(self, paths, name):
		pprint.pprint(name)
		
		if sublime.ok_cancel_dialog('Create '+name+'.install'):
			pprint.pprint(paths)
		else:
			pprint.pprint('nope')
		# for item in SideBarSelection(paths).getSelectedDirectoriesOrDirnames():
		# 	item = SideBarItem(item.join(name), True)
		# 	console.log(item.join(name));
		# 	if item.exists():
		# 		sublime.error_message("Unable to create module, folder or file exists.")
		# 		self.run(paths, name)
		# 		return
		# 	else:
		# 		item.create()
		# 		if not item.exists():
		# 			sublime.error_message("Unable to create folder:\n\n"+item.path())
		# 			self.run(paths, name)
		# 			return
		self.refresh()
	def refresh(self):
		try:
			sublime.set_timeout(lambda:sublime.active_window().run_command('refresh_folder_list'), 200);
			sublime.set_timeout(lambda:sublime.active_window().run_command('refresh_folder_list'), 1300);
		except:
			pass
