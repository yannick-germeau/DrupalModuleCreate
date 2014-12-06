import sublime, sublime_plugin
import os, shutil
import pprint

def Window():
    return sublime.active_window()

class DmcreateCommand(sublime_plugin.WindowCommand):
    def run(self, paths = [], name = ""):
        import functools
        Window().run_command('hide_panel');
        Window().show_input_panel("Module Name:", name, functools.partial(self.on_done, paths), None, None)

    def on_done(self, paths, name): 
        self.create_module(paths, name)      
        self.confirm_install(paths,name)      
     

    def create_module(self, paths, name):
        for item in paths:
            item = DMModule(item, name)

            if item.exists():
                sublime.error_message("Unable to create file, file or folder exists.")
                self.run(paths, name)
                return
            else:
                try:
                    item.create()
                except:
                    sublime.error_message("Unable to create file:\n\n"+item.path())
                    self.run(paths, name)
                    return
        self.refresh()

    def confirm_install(self, paths, name):
        import functools
        Window().run_command('hide_panel');
        yes = []
        yes.append('Create '+name+'.install')
        no = []
        no.append('No')
        
        if sublime.platform() == 'osx':
            sublime.set_timeout(lambda:Window().show_quick_panel([yes, no], functools.partial(self.on_confirm_install, paths)), 200)
        else:
            Window().show_quick_panel([yes, no], functools.partial(self.on_confirm_install, paths, name))

    def on_confirm_install(self, paths,name, result):
        if (result == 0):
            for item in paths:
                item = DMModule(item, name)
                try:
                    item.create_install()
                except:
                    return
        self.refresh()

    def refresh(self):
        try:
            sublime.set_timeout(lambda:Window().run_command('refresh_folder_list'), 200);
            sublime.set_timeout(lambda:Window().run_command('refresh_folder_list'), 1300);
        except:
            pass


class DMModule:
    def __init__(self, path, name):
        self._path = os.path.join(path, name)
        self._name = name

    def exists(self):
        return os.path.isdir(self.path()) or os.path.isfile(self.path())

    def create(self):
        self.dirnameCreate()
        os.makedirs(self.path(), 0o775)
        self.write(self._name+'.info',"name = "+self._name+"\n\rdescription =\n\rcore = 7.x\n\rpackage = Globule");
        self.write(self._name+'.module', "<?php");

    def create_install(self):
        self.write(self._name+'.install', "<?php");
    
    def dirnameCreate(self):
        try:
            os.makedirs(self.dirname(), 0o775)
        except:
            pass

    def dirname(self):
        branch, leaf = os.path.split(self.path())
        pprint.pprint(branch)
        pprint.pprint(leaf)
        return branch;

    def path(self, path = ''):
        if path == '':
            return self._path
        else:
            self._path = path
            return path

    def dirnameCreate(self):
        try:
            os.makedirs(self.dirname(), 0o775)
        except:
            pass

    def name(self):
        branch, leaf = os.path.split(self.path())
        return leaf;

    def write(self,filename, content):
        pprint.pprint(os.path.join(self.path(),filename))
        open(os.path.join(self.path(),filename), 'w+', encoding='utf8', newline='').write(str(content))