from PySide6.QtWidgets import (
    QWidget, QMainWindow, QListWidget, QTextEdit, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt
from .utils.storage import load_pages, save_pages


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notes")
        self.resize(800, 600)

        self.pages = load_pages()
        self.current_page = None

        # Widgets
        self.sidebar = QListWidget()
        self.editor = QTextEdit()
        self.new_button = QPushButton("Nueva página")
        self.save_button = QPushButton("Guardar página")

        # Layout sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(5)
        sidebar_layout.addWidget(self.new_button)
        sidebar_layout.addWidget(self.save_button)
        sidebar_layout.addWidget(self.sidebar, 1)
        sidebar_layout.addStretch(0)
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        main_layout.addWidget(sidebar_widget, 1)
        main_layout.addWidget(self.editor, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.new_button.clicked.connect(self.new_page)
        self.save_button.clicked.connect(self.save_current_page)
        self.sidebar.itemClicked.connect(self.load_selected_page)

        self.refresh_sidebar()

    def refresh_sidebar(self):
        self.sidebar.clear()
        for title in self.pages.keys():
            self.sidebar.addITem(title)

    def new_page(self):
        title, ok = QInputDialog.getText(self, "Nueva página", "Título de la página:")
        if ok and title:
            if title in self.pages:
                QMessageBox.warning(self, "Error", "Ya existe una página con ese nombre.")
                return
            self.pages[title] = ""
            self.refresh_sidebar()

    def save_current_page(self):
        if self.current_page:
            self.pages[self.current_page] = self.editor.toPlainText()
            save_pages(self.pages)
            QMessageBox.information(self, "Guardado", f"Página '{self.current_page}' guardada correctamente.")

    def load_selected_page(self, item):
        self.current_page = item.text()
        self.editor.setPlainText(self.pages.get(self.current_page, ""))
