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


if platform is Platform.Darwin:
    icon_path = get_base_path('assets/icon.png')
else:
    icon_path = get_base_path('assets/icon.ico')

if platform is Platform.Darwin:
    class App(rumps.App):
        def __init__(self):
            super(App, self).__init__('Live', icon=icon_path, quit_button=None, menu=[{'Update': ['UpdateConfig']},
                                                                                      None,
                                                                                      'Start',
                                                                                      'Quit'
                                                                                      ])

        @rumps.clicked("Update", "UpdateConfig")
        def UpdateConfig(self, _):
            self.updateConfig()

        @rumps.clicked("Start")
        def Start(self, _):
            self.start_live()

        @rumps.clicked("Quit")
        def Quit(self, _):
            self.quit()

        def quit(self):
            rumps.quit_application()

        def start_live(self):
            pass

        def start(self):
            super(App, self).run()

        def updatePlaylist(self):
            pass

        def updateConfig(self):
            pass
else:
    class App:
        def __init__(self):
            image = Image.open(icon_path)
            self.app = Icon('Live', icon=image,
                            menu=Menu(MenuItem('UpdateConfig', self.updateConfig),
                                      None,
                                      MenuItem('Start', self.start_live),
                                      MenuItem('Quit', self.quit)))

        def start_live(self, icon, item):
            pass

        def quit(self):
            self.quit_live()

        def quit_live(self):
            self.app.stop()

        def start(self):
            self.app.run()

        def updatePlaylist(self):
            pass

        def updateConfig(self):
            pass

if __name__ == "__main__":
    print('gui main')
