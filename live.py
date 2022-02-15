import json
import subprocess
import threading
import socket

import requests
from app.gui import *

LIVE_PATH = os.path.join('live.m3u8')

if not os.path.exists(LIVE_PATH):
    r = requests.get('http://notag.cn/live/macast_live.m3u8')
    with open(LIVE_PATH, 'wb') as f:
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
        self.ipc_thread = None
        self.mpvsocket = '/tmp/mpvsocket'
        self.ipc = None
        self.start_live()

    def close(self):
        self.send_command(['quit'])

    def start_live(self):
        if self.mpv_thread is None or self.mpv_thread.is_alive() is False:
            self.mpv_thread = threading.Thread(target=self.start_mpv, name="MPV_THREAD")
            self.mpv_thread.start()
        time.sleep(0.5)
        if self.ipc_thread is None or self.ipc_thread.is_alive() is False:
            self.ipc_thread = threading.Thread(target=self.start_ipc, name="IPC_THREAD")
            self.ipc_thread.start()

    def send_msg(self, msg):
        if self.ipc is not None:
            self.ipc.sendall(msg.encode())

    def send_command(self, command):
        data = {"command": command}
        msg = json.dumps(data) + '\n'
        self.send_msg(msg)

    def start_ipc(self):
        if self.mpv_thread.is_alive and self.ipc_thread.is_alive():
            self.ipc = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.ipc.connect(self.mpvsocket)
            self.send_command(['loadlist', LIVE_PATH])
            while True:
                try:
                    data = self.ipc.recv(1048576)
                    if data == b'':
                        break
                    print('recv:', data)
                except Exception as e:
                    print('excep:', e)
                    break
            self.ipc.close()
            self.ipc = None

    def start_mpv(self):
        params = [
            set_mpv_default_path(),
            '--no-config',
            '--no-input-default-bindings',
            '--geometry=80%:0%', '--autofit=30%',
            '--idle',
            '--force-window=yes',
            '--osc=no',
            '--input-ipc-server=' + self.mpvsocket,
            '--script=' + script_path,
        ]
        spc = subprocess.Popen(params)
        spc.communicate()


if __name__ == '__main__':
    LiveApp().start()
