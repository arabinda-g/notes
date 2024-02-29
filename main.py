import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QMessageBox, QPushButton, QWidget, QDialog, QVBoxLayout,
                             QLineEdit, QDialogButtonBox, QLabel, QComboBox, QHBoxLayout, QFormLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSettings, QPoint, QMimeData
from PyQt5.QtGui import QCursor, QDrag, QPainter, QPixmap
from PyQt5 import QtCore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.settings = QSettings("MyCompany", "MyApp")
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("PyQt Application")
        self.setGeometry(100, 100, 800, 600)
        
        # Create the menu
        self.createMenu()
        
        # Status bar
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Ready")

        # Main container
        self.mainContainer = QWidget()
        self.setCentralWidget(self.mainContainer)

        # Add a layout to the main container and set the alignment to top
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainContainer.setLayout(self.mainLayout)

        # Theme handling
        self.applyTheme()
        
        # Load settings
        self.loadSettings()
        
    def createMenu(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')
        
        # File actions
        newAct = QAction('New...', self, shortcut='Ctrl+N')
        newAct.triggered.connect(self.showAddButtonDialog)
        fileMenu.addAction(newAct)
        
        saveAct = QAction('Save', self, shortcut='Ctrl+S')
        saveAct.triggered.connect(self.saveSettings)
        fileMenu.addAction(saveAct)
        
        fileMenu.addSeparator()
        
        exitAct = QAction('Exit', self, shortcut='Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAct)
        
        # Edit actions
        undoAct = QAction('Undo', self, shortcut='Ctrl+Z')
        editMenu.addAction(undoAct)
        
        redoAct = QAction('Redo', self, shortcut='Ctrl+Y')
        editMenu.addAction(redoAct)
        
        editMenu.addSeparator()
        
        movableAct = QAction('Movable', self, shortcut='Ctrl+D')
        movableAct.triggered.connect(self.toggleMovable)
        editMenu.addAction(movableAct)

    def applyTheme(self):
        # This function should handle theme switching
        pass

    def saveSettings(self):
        self.settings.setValue("windowSize", self.size())
        self.settings.setValue("windowPosition", self.pos())
        self.settings.beginWriteArray("buttons")
        for i, button in enumerate(self.buttons):
            self.settings.setArrayIndex(i)
            self.settings.setValue("title", button.title)
            self.settings.setValue("content", button.content)
            self.settings.setValue("left", button.left)
            self.settings.setValue("top", button.top)
            self.settings.setValue("style", button.style)
        self.settings.endArray()

    def loadSettings(self):
        self.resize(self.settings.value("windowSize", self.size()))
        self.move(self.settings.value("windowPosition", self.pos()))
        size = self.settings.beginReadArray("buttons")
        for i in range(size):
            self.settings.setArrayIndex(i)
            buttonInfo = {
                "title": self.settings.value("title"),
                "content": self.settings.value("content"),
                "left": int(self.settings.value("left")),
                "top": int(self.settings.value("top")),
                "style": self.settings.value("style")
            }
            self.addNewButton(buttonInfo)
        self.settings.endArray()

    def showAddButtonDialog(self):
        dialog = AddButtonDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            buttonInfo = dialog.getButtonInfo()
            self.addNewButton(buttonInfo)

    def addNewButton(self, buttonInfo):
        newButton = DraggableButton(buttonInfo['title'], buttonInfo['content'],
                                    buttonInfo['left'], buttonInfo['top'],
                                    buttonInfo['style'], self)
        self.buttons.append(newButton)  # Keep track of the button
        # newButton.show()

        # Add the button to the main layout
        self.mainLayout.addWidget(newButton)

    def toggleMovable(self):
        # Toggle movable state for buttons
        pass


class DraggableButton(QWidget):
    def __init__(self, title, content, left, top, style, parent=None):
        super().__init__(parent)
        self.title = title
        self.content = content
        self.left = left
        self.top = top
        # self.style = style
        self.initUI()
        self.setFixedSize(100, 50)
        self.move(left, top)
        self.dragStartPos = QPoint()
        self.wasMoved = False  # Track if the button was moved

    def initUI(self):
        self.button = QPushButton(self.title, self)
        self.button.setGeometry(0, 0, 100, 50)
        # self.applyStyle(self.style)
        self.button.clicked.connect(self.copyContentToClipboard)

        # Set the mouse event handlers
        self.button.mousePressEvent = self.btnMousePressEvent
        self.button.mouseMoveEvent = self.btnMouseMoveEvent
        self.button.mouseReleaseEvent = self.btnMouseReleaseEvent

    def applyStyle(self, style):
        if style == "Style 1":
            self.button.setStyleSheet("background-color: lightgray; color: black;")
        elif style == "Style 2":
            self.button.setStyleSheet("background-color: darkgray; color: white;")

    def copyContentToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.content)

    def btnMousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStartPos = event.pos()
            self.wasMoved = False  # Reset the moved flag on new press

    def btnMouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.dragStartPos).manhattanLength() < QApplication.startDragDistance():
            return
        self.move(self.mapToParent(event.pos() - self.dragStartPos))
        self.wasMoved = True  # Set the flag to true as the button is being moved

    def btnMouseReleaseEvent(self, event):
        if not self.wasMoved:
            # The button was clicked without being dragged
            self.onClickAction()
        self.wasMoved = False  # Reset the moved flag after the release



class AddButtonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add New Button')
        self.layout = QFormLayout(self)

        self.titleInput = QLineEdit(self)
        self.leftInput = QLineEdit(self)
        self.topInput = QLineEdit(self)
        self.styleDropdown = QComboBox(self)
        self.contentInput = QLineEdit(self)

        self.styleDropdown.addItems(["Style 1", "Style 2"])  # Add your styles here

        self.layout.addRow(QLabel("Title:"), self.titleInput)
        self.layout.addRow(QLabel("Left:"), self.leftInput)
        self.layout.addRow(QLabel("Top:"), self.topInput)
        self.layout.addRow(QLabel("Style:"), self.styleDropdown)
        self.layout.addRow(QLabel("Content:"), self.contentInput)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

    def getButtonInfo(self):
        return {
            "title": self.titleInput.text(),
            "left": int(self.leftInput.text()),
            "top": int(self.topInput.text()),
            "style": self.styleDropdown.currentText(),
            "content": self.contentInput.text()
        }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
