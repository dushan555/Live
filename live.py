import os
import sys
import subprocess
import threading

import rumps

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


class LiveApp(rumps.App):
    def __init__(self):
        super(LiveApp, self).__init__('Live', icon=app.gui.icon_path)
        self.mpv_thread = None

    def start_live(self):
        if self.mpv_thread is None or self.mpv_thread.is_alive() is False:
            self.mpv_thread = threading.Thread(target=self.start_mpv, name="MPV_THREAD")
            self.mpv_thread.start()

    @rumps.clicked("Start")
    def prefs(self, _):
        self.start_live()

    @staticmethod
    def start_mpv():
        spc = subprocess.Popen([set_mpv_default_path(), 'http://notag.cn/live/macast_live.m3u8'])
        spc.communicate()


if __name__ == '__main__':
    LiveApp().run()
