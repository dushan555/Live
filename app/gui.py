import rumps
import os


class App:
    def __init__(self, name):
        icon_path = self.get_base_path('assets/icon.png')
        self.name = name
        self.app = rumps.App(name, icon=icon_path)

    def start(self):
        self.app.run()

    @staticmethod
    def get_base_path(path='.'):
        b = os.path.join(os.path.dirname(__file__), path)
        return b


if __name__ == "__main__":
    print('gui main')


    class LiveApp(App):
        def __init__(self):
            super(LiveApp, self).__init__('Live')


    LiveApp().start()
