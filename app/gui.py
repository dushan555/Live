import os
import sys
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


def get_base_path(path='.'):
    b = os.path.join(os.path.dirname(__file__), path)
    return b


script_path = get_base_path('assets/config.lua')
if platform is Platform.Darwin:
    icon_path = get_base_path('assets/icon.png')
else:
    icon_path = get_base_path('assets/icon.ico')

if platform is Platform.Darwin:
    class App(rumps.App):
        def __init__(self):
            super(App, self).__init__('Live', icon=icon_path, quit_button=None)

        @rumps.clicked("Start")
        def Start(self, _):
            self.start_live()

        @rumps.clicked("Quit")
        def Quit(self, _):
            rumps.quit_application()

        def start_live(self):
            pass

        def start(self):
            super(App, self).run()

else:
    class App:
        def __init__(self):
            image = Image.open(icon_path)
            self.app = Icon('Live', icon=image,
                            menu=Menu(MenuItem('Start', self.start_live), MenuItem('Quit', self.quit_live)))

        def start_live(self, icon, item):
            pass

        def quit_live(self):
            self.app.stop()

        def start(self):
            self.app.run()


if __name__ == "__main__":
    print('gui main')
