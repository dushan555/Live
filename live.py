import os
import sys
import subprocess
import threading
from enum import Enum


class Platform(Enum):
    Darwin = 0
    Win32 = 1
    Linux = 2


platform = None
if sys.platform == 'darwin':
    platform = Platform.Darwin
elif sys.platform == 'win32':
    platform = Platform.Win32
elif sys.platform == 'linux':
    platform == Platform.Linux

if platform is Platform.Darwin:
    import rumps
else:
    from pystray import Menu, MenuItem, Icon
    from PIL import Image


import app.gui


def get_base_path(path="."):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.getcwd()
    return os.path.join(base_path, path)


def set_mpv_default_path():
    mpv_path = 'mpv'
    if sys.platform == 'darwin':
        mpv_path = get_base_path('bin/MacOS/mpv')
    elif sys.platform == 'win32':
        mpv_path = get_base_path('bin/mpv.exe')
    return mpv_path


if platform is Platform.Darwin:
    class App(rumps.App):
        def __init__(self):
            super(LiveApp, self).__init__('Live', icon=app.gui.icon_path)

        @rumps.clicked("Start")
        def prefs(self, _):
            self.start_live()

        def start_live(self):
            pass

        def start(self):
            super(App, self).run()
else:
    class App:
        def __init__(self):
            print('App init')
            image = Image.open(app.gui.icon_path)
            self.app = Icon('Live', icon=image, menu=Menu(MenuItem('Start', self.start_live), MenuItem('Quit', self.quit_live)))

        def start_live(self, icon, item):
            pass

        def quit_live(self):
            self.app.stop()

        def start(self):
            self.app.run()


class LiveApp(App):
    def __init__(self):
        super(LiveApp, self).__init__()
        self.mpv_thread = None

    def start_live(self):
        if self.mpv_thread is None or self.mpv_thread.is_alive() is False:
            self.mpv_thread = threading.Thread(target=self.start_mpv, name="MPV_THREAD")
            self.mpv_thread.start()

    @staticmethod
    def start_mpv():
        spc = subprocess.Popen([set_mpv_default_path(), 'http://notag.cn/live/macast_live.m3u8'])
        spc.communicate()


if __name__ == '__main__':
    LiveApp().start()
