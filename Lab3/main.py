import sqlite3
import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QTabWidget, QTableWidget,
    QTableWidgetItem, QFileDialog, QMessageBox, QAbstractItemView,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 3 — SQL и PyQt")
        self.resize(900, 550)
        self.connection = None

        menu = self.menuBar().addMenu("Menu")
        menu.addAction("Set connection", self.open_database)
        menu.addAction("Close connection", self.close_database)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.bt1 = QPushButton("bt1: названия объектов")
        self.columns = QComboBox()
        row1 = QHBoxLayout()
        row1.addWidget(self.bt1)
        row1.addWidget(QLabel("Столбец sqlite_master:"))
        row1.addWidget(self.columns)
        layout.addLayout(row1)
        self.bt2 = QPushButton("bt2: все студенты")
        self.bt3 = QPushButton("bt3: оценка от 4")
        row2 = QHBoxLayout()
        row2.addWidget(self.bt2)
        row2.addWidget(self.bt3)
        layout.addLayout(row2)

        self.tabs = QTabWidget()
        self.tables = []
        for number in range(1, 6):
            table = QTableWidget()
            table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.tables.append(table)
            self.tabs.addTab(table, f"Tab{number}")
        layout.addWidget(self.tabs)

        self.bt1.clicked.connect(
            lambda: self.show_query("SELECT name FROM sqlite_master", 1))
        self.bt2.clicked.connect(
            lambda: self.show_query("SELECT * FROM students", 3))
        self.bt3.clicked.connect(lambda: self.show_query(
            "SELECT * FROM students WHERE grade >= 4 ORDER BY grade DESC", 4))
        self.columns.currentTextChanged.connect(self.select_column)
        self.set_controls(False)
        self.statusBar().showMessage("Выберите Menu → Set connection")

    def set_controls(self, enabled):
        for control in (self.bt1, self.bt2, self.bt3, self.columns):
            control.setEnabled(enabled)

    def open_database(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите базу SQLite", str(Path(__file__).parent),
            "Базы SQLite (*.db *.sqlite *.sqlite3);;Все файлы (*)")
        if not path:
            return

        new_connection = None
        try:
            uri = Path(path).resolve().as_uri() + "?mode=ro"
            new_connection = sqlite3.connect(uri, uri=True)
            cursor = new_connection.execute("SELECT * FROM sqlite_master")
            column_names = [column[0] for column in cursor.description]
        except sqlite3.Error as error:
            if new_connection is not None:
                new_connection.close()
            QMessageBox.warning(self, "Ошибка подключения", str(error))
            return

        self.close_database()
        self.connection = new_connection
        self.set_controls(True)
        self.columns.blockSignals(True)
        self.columns.addItems(column_names)
        self.columns.setCurrentIndex(-1)
        self.columns.blockSignals(False)
        self.show_query("SELECT * FROM sqlite_master", 0)

    def show_query(self, sql, tab_index):
        if self.connection is None:
            return
        try:
            cursor = self.connection.execute(sql)
            headers = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
        except sqlite3.Error as error:
            QMessageBox.warning(self, "Ошибка SQL", str(error))
            return

        table = self.tables[tab_index]
        table.clear()
        table.setColumnCount(len(headers))
        table.setRowCount(len(rows))
        table.setHorizontalHeaderLabels(headers)
        for row_index, row in enumerate(rows):
            for column_index, value in enumerate(row):
                text = "NULL" if value is None else str(value)
                table.setItem(row_index, column_index, QTableWidgetItem(text))
        table.resizeColumnsToContents()
        self.tabs.setCurrentIndex(tab_index)
        self.statusBar().showMessage(f"{sql} | Строк: {len(rows)}")

    def select_column(self, column):
        if column:
            # идентификатор из структуры БД; кавычки экранируются.
            quoted_column = '"' + column.replace('"', '""') + '"'
            self.show_query(f"SELECT {quoted_column} FROM sqlite_master", 2)

    def close_database(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        self.columns.blockSignals(True)
        self.columns.clear()
        self.columns.blockSignals(False)
        for table in self.tables:
            table.clear()
            table.setRowCount(0)
            table.setColumnCount(0)
        self.tabs.setCurrentIndex(0)
        self.set_controls(False)
        self.statusBar().showMessage("Соединение закрыто. Выберите Menu → Set connection")

    def closeEvent(self, event):
        self.close_database()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())