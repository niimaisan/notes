from PySide6.QtWidgets import (
    QWidget, QMainWindow, QListWidget, QTextEdit,
    QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox,
    QInputDialog, QTextBrowser, QSplitter
)
from PySide6.QtCore import Qt, QTimer
from .utils.storage import load_pages, save_pages

import markdown


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
        self.preview = QTextBrowser()
        self.new_button = QPushButton("Nueva página")
        self.delete_button = QPushButton("Eliminar página")

        # Layout sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(5)
        sidebar_layout.addWidget(self.new_button)
        sidebar_layout.addWidget(self.delete_button)
        sidebar_layout.addWidget(self.sidebar, 1)
        sidebar_layout.addStretch(0)
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)

        # editor + preview en splitter
        self.editor_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.editor_splitter.addWidget(self.editor)
        self.editor_splitter.addWidget(self.preview)
        self.editor_splitter.setStretchFactor(0, 3)
        self.editor_splitter.setStretchFactor(1, 2)

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        main_layout.addWidget(sidebar_widget, 1)
        main_layout.addWidget(self.editor_splitter, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.new_button.clicked.connect(self.new_page)
        self.delete_button.clicked.connect(self.delete_page)
        self.sidebar.itemClicked.connect(self.load_selected_page)

        # evitar renderizar demasiado seguido
        self.preview_timer = QTimer()
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self.render_preview)

        # autoguardado con retardo
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.autosave)

        # conectar editor
        self.editor.textChanged.connect(self.update_preview)
        self.editor.textChanged.connect(self.schedule_autosave)

        self.refresh_sidebar()

    def refresh_sidebar(self):
        self.sidebar.clear()
        for title in self.pages.keys():
            self.sidebar.addItem(title)

    def new_page(self):
        title, ok = QInputDialog.getText(self, "Nueva página", "Título de la página:")
        if ok and title:
            if title in self.pages:
                QMessageBox.warning(self, "Error", "Ya existe una página con ese nombre.")
                return
            self.pages[title] = ""
            self.refresh_sidebar()

    def delete_page(self):
        if not self.current_page:
            QMessageBox.warning(self, "Error", "No hay ninguna página seleccionada")
            return

        reply = QMessageBox.question(
            self,
            "Eliminar página",
            f"¿Seguro que dese eliminar la página '{self.current_page}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            del self.pages[self.current_page]
            save_pages(self.pages)
            self.current_page = None
            self.editor.clear()
            self.preview.clear()
            self.refresh_sidebar()
            QMessageBox.information(self, "Eliminada", "La página ha sido eliminada")

    def load_selected_page(self, item):
        self.current_page = item.text()
        self.editor.setPlainText(self.pages.get(self.current_page, ""))

    def update_preview(self):
        self.preview_timer.start(200)


    def render_preview(self):
        text = self.editor.toPlainText()
        html = markdown.markdown(text)
        self.preview.setHtml(html)

    def schedule_autosave(self):
        if self.current_page:
            self.save_timer.start(1000)

    def autosave(self):
        if self.current_page:
            self.pages[self.current_page] = self.editor.toPlainText()
            save_pages(self.pages)
