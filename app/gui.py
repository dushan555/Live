import rumps
import os


class App:
    def __init__(self, name, menu):
        icon_path = self.get_base_path('assets/icon.png')
        self.name = name
        self.menu = menu
        self.app = rumps.App(self.name, icon=icon_path, menu=self._build_menu_rumps(self.menu))

    def start(self):
        self.app.run()

    def quit(self):
        rumps.quit_application()

    def _build_menu_rumps(self, menu):
        items = []
        if menu:
            for item in menu:
                if item is None:
                    items.append(None)
                elif item.children is not None:
                    menu_item = rumps.MenuItem(item.text)
                    items.append([menu_item, self._build_menu_rumps(item.children)])
                else:
                    items.append(self._build_menu_item_rumps(item))
        return items

    def _build_menu_item_rumps(self, item):
        callback = item._rumpsCallback if item.enabled else None
        menu_item = rumps.MenuItem(item.text, callback, item.key)
        menu_item.state = 1 if item.checked else 0
        item.view = menu_item
        return menu_item

    @staticmethod
    def get_base_path(path='.'):
        b = os.path.join(os.path.dirname(__file__), path)
        return b


class MenuItem:
    def __init__(self, text, callback=None, checked=None, enabled=True, children=None, data=None, key=None):
        self.view = None
        self._text = text
        self.callback = callback
        self.children = children
        self._checked = checked
        self._enabled = enabled
        self.data = data
        self.id = text
        self.key = key

    @property
    def text(self):
        return self._text

    @property
    def checked(self):
        return self._checked

    @property
    def enabled(self):
        return self._enabled

    @text.setter
    def text(self, value):
        self._text = value
        print('set', value)
        if self.view is None:
            print('view none')
            return
        self.view.title = self._text

    @checked.setter
    def checked(self, value):
        self._checked = value

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        if self.view is None:
            return
        state = 1 if self._checked else 0
        self.view.set_callback(self._rumpsCallback if self._enabled else None, self.key)

    def items(self):
        return [] if self.children is None else self.children

    def _rumpsCallback(self, item):
        self.callback(self)

if __name__ == "__main__":
    print('gui main')


    class LiveApp(App):
        def __init__(self):
            super(LiveApp, self).__init__('Live', [MenuItem("Live", self.addlive), None])

        def addlive(self, _):
            print("live")


    LiveApp().start()
