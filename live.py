import os
import sys
import subprocess
import threading

from app.gui import App


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


if __name__ == '__main__':

    class LiveApp(App):
        def __init__(self):
            menu = None
            super(LiveApp, self).__init__('Live', menu=menu)
            self.mpv_thread = threading.Thread(target=self.start_mpv, name="MPV_THREAD")
            self.mpv_thread.start()

        def start_mpv(self):
            spc = subprocess.Popen([set_mpv_default_path(), 'http://notag.cn/live/macast_live.m3u8'])
            spc.communicate()


    LiveApp().start()
