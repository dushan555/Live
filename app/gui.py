import os
import sys


def get_base_path(path='.'):
    b = os.path.join(os.path.dirname(__file__), path)
    return b


if sys.platform == 'darwin':
    icon_path = get_base_path('assets/icon.png')
else:
    icon_path = get_base_path('assets/icon.ico')


if __name__ == "__main__":
    print('gui main')
