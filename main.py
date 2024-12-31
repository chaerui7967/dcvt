import sys

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from widgets.convert_dataset import DataSetConvert


class AutoLabelMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tab_widget = None
        self.convert_widget = None

        # self.init_menu()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.tr("DataSet Converter"))
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        self.tab_widget = QTabWidget(self)

        self.convert_widget = DataSetConvert(self)

        self.tab_widget.addTab(self.convert_widget, self.tr("DataSet 변환"))

        self.setCentralWidget(self.tab_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_widget = AutoLabelMainWindow()
    main_widget.show()

    sys.exit(app.exec())
