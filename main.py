import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QAction,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QComboBox,
    QStatusBar,
    QMessageBox,
)
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QDrag
from PyQt5.QtGui import QColor

class ButtonData:
    def __init__(self, title, left, top, style, content):
        self.title = title
        self.left = left
        self.top = top
        self.style = style
        self.content = content

class Button(QPushButton):
    def __init__(self, data, parent):
        super().__init__(data.title, parent)
        self.data = data
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            mimeData = QMimeData()
            mimeData.setData("application/x-buttondata", self.data.__dict__)
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.MoveAction)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("MyCompany", "MyApp")
        self.buttons = []
        self.dark_theme = self.settings.value("dark_theme", False, bool)

        self.setup_ui()
        self.load_settings()
        self.update_theme()

    def setup_ui(self):
        self.setWindowTitle("Button Manager")
        self.setGeometry(100, 100, 800, 600)

        # Menu bar
        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu("&File")
        self.edit_menu = self.menubar.addMenu("&Edit")

        self.new_action = QAction("&New...", self, shortcut=QKeySequence.New, triggered=self.new_button)
        self.save_action = QAction("&Save", self, shortcut=QKeySequence.Save, triggered=self.save_settings)
        self.exit_action = QAction("E&xit", self, shortcut=QKeySequence.Quit, triggered=self.close)

        self.undo_action = QAction("&Undo", self, shortcut=QKeySequence.Undo, triggered=self.handle_undo)
        self.redo_action = QAction("&Redo", self, shortcut=QKeySequence.Redo, triggered=self.handle_redo)
        self.movable_action = QAction("&Movable", self, shortcut=QKeySequence.Copy, triggered=self.toggle_movable)

        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)

        self.central_widget = QWidget()

        # self.layout = QHBoxLayout(self.button_container)
        self.button_container = QWidget()  # Instantiate the button container
        self.layout = QHBoxLayout(self.button_container)
        self.layout.setSpacing(0)

        # Status bar
        self.statusbar = QStatusBar(self)
        self.statusbar.showMessage("Ready")
        self.status_label = QLabel("0 buttons")
        self.statusbar.addWidget(self.status_label)
        self.setStatusBar(self.statusbar)

        self.update_status_bar()



    def update_theme(self):
        palette = QPalette()
        if self.dark_theme:
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
        else:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
        self.setPalette(palette)


    def load_settings(self):
        self.buttons.clear()
        data = self.settings.value("buttons", [])
        for item in data:
            button_data = ButtonData(**item)
            self.add_button(button_data)

    def save_settings(self):
        data = [button.data.__dict__ for button in self.buttons]
        self.settings.setValue("buttons", data)

    def update_status_bar(self):
        self.status_label.setText(f"{len(self.buttons)} buttons")

    def add_button(self, data):
        button = Button(data, self.button_container)
        button.clicked.connect(lambda: self.copy_to_clipboard(button.data.content))
        self.layout.addWidget(button)
        button.move(data.left, data.top)
        self.buttons.append(button)
        self.update_status_bar()

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def new_button(self):
        self.new_button_window = NewButtonWindow(self)
        self.new_button_window.show()

    def toggle_movable(self):
        self.movable_action.setChecked(not self.movable_action.isChecked())
        for button in self.buttons:
            button.setMovable(self.movable_action.isChecked())

    def handle_undo(self):
        return

    def handle_redo(self):
        return

    def closeEvent(self, event):
        self.save_settings()
        event.accept()

class NewButtonWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("New Button")

        self.layout = QVBoxLayout(self)

        self.title_label = QLabel("Title:")
        self.title_input = QLineEdit()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_input)

        self.position_layout = QHBoxLayout()
        self.left_label = QLabel("Left:")
        self.left_input = QLineEdit()
        self.position_layout.addWidget(self.left_label)
        self.position_layout.addWidget(self.left_input)

        self.top_label = QLabel("Top:")
        self.top_input = QLineEdit()
        self.position_layout.addWidget(self.top_label)
        self.position_layout.addWidget(self.top_input)
        self.layout.addLayout(self.position_layout)

        self.style_label = QLabel("Style:")
        self.style_combo = QComboBox()
        self.style_combo.addItem("Default")
        self.style_combo.addItem("Primary")
        self.style_combo.addItem("Secondary")
        self.layout.addWidget(self.style_label)
        self.layout.addWidget(self.style_combo)

        self.content_label = QLabel("Content:")
        self.content_edit = QTextEdit()
        self.layout.addWidget(self.content_label)
        self.layout.addWidget(self.content_edit)

        self.buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_and_close)
        self.buttons_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.buttons_layout)

    def save_and_close(self):
        title = self.title_input.text()
        left = int(self.left_input.text())
        top = int(self.top_input.text())
        style = self.style_combo.currentText()
        content = self.content_edit.toPlainText()
        data = ButtonData(title, left, top, style, content)
        self.parent.add_button(data)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
    
