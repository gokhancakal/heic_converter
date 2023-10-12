import sys
from PyQt5.QtWidgets import QApplication
from gui import HEICtoJPGConverter


def main():
    app = QApplication(sys.argv)
    ex = HEICtoJPGConverter()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
