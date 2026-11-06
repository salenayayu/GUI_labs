import os
from pathlib import Path
import PyQt5
import sys

qt_folder = Path(PyQt5.__file__).resolve().parent / "Qt5"

os.environ["QT_PLUGIN_PATH"] = str(qt_folder / "plugins")
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = str(
    qt_folder / "plugins" / "platforms"
)
os.environ["QML2_IMPORT_PATH"] = str(qt_folder / "qml")

from PyQt5.QtCore import (
    QUrl, QObject, QTimer, QMetaObject, Q_ARG, Q_RETURN_ARG,
)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Interface(QObject):
    def __init__(self):
        super().__init__()
        self.canvas = None
        self.file_path = Path(__file__).parent / "saved" / "canvas.png"
        self.timer = QTimer(self)
        self.timer.setInterval(10000)  # Миллисекунды: 10 секунд.
        self.timer.timeout.connect(self.save_canvas)

    def start(self, canvas):
        self.canvas = canvas
        self.timer.start()

    def save_canvas(self):
        if self.canvas is None or not self.canvas.property("available"):
            return
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            # Вызываем метод Canvas.save() у QML-объекта из Python.
            success = QMetaObject.invokeMethod(
                self.canvas, "save", Q_RETURN_ARG(bool),
                Q_ARG(str, str(self.file_path.resolve())),
            )
            if success:
                print("Рисунок сохранён:", self.file_path, flush=True)
            else:
                print("Не удалось сохранить рисунок:", self.file_path, flush=True)
        except (OSError, RuntimeError) as error:
            print("Ошибка сохранения:", error, flush=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("_backend", interface)

    # Абсолютный путь позволяет запускать проект из любой рабочей папки.
    qml_path = Path(__file__).with_name("mainWindow.qml").resolve()
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    if not engine.rootObjects():
        print("Ошибка: не удалось загрузить mainWindow.qml")
        sys.exit(1)

    canvas = engine.rootObjects()[0].findChild(QObject, "drawingCanvas")
    if canvas is None:
        print("Ошибка: область рисования не найдена")
        sys.exit(1)
    interface.start(canvas)
    app.aboutToQuit.connect(interface.timer.stop)
    sys.exit(app.exec_())
