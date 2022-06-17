import subprocess
import threading

import requests
from app.gui import *

LIVE_PATH = os.path.join('live.m3u8')
SCRIPT_PATH = os.path.join('config.lua')

if not os.path.exists(LIVE_PATH):
    r = requests.get('https://notag.cn/live/live.m3u8')
    with open(LIVE_PATH, 'wb') as f:
        f.write(r.content)

if not os.path.exists(SCRIPT_PATH):
    r = requests.get('https://notag.cn/live/config.lua')
    with open(SCRIPT_PATH, 'wb') as f:
        f.write(r.content)


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


class LiveApp(App):
    def __init__(self):
        super(LiveApp, self).__init__()
        self.mpv_thread = None
        self.mpvsocket = '/tmp/mpvsocket'
        # self.start_live()

    def start_live(self):
        if self.mpv_thread is None or self.mpv_thread.is_alive() is False:
            self.mpv_thread = threading.Thread(target=self.start_mpv, name="MPV_THREAD")
            self.mpv_thread.start()

    @staticmethod
    def start_mpv():
        params = [
            set_mpv_default_path(),
            '--no-config',
            '--no-input-default-bindings',
            '--geometry=80%:0%', '--autofit=20%',
            '--idle',
            '--hwdec=yes'
            '--force-window=yes',
            '--osc=no',
            '--script=' + SCRIPT_PATH,
            '--stop-playback-on-init-failure=yes'
        ]
        spc = subprocess.Popen(params)
        spc.communicate()


if __name__ == '__main__':
    LiveApp().start()
