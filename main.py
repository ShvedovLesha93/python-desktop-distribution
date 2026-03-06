import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)
from PySide6.QtCore import QTimer, Qt


from app.logger import configure_logging
from app.update_checker import UpdateChecker
import updater


from app.translator import language_manager, _

configure_logging()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.update_cheker = UpdateChecker()
        self.update_cheker.check_for_updates()
        self.status_msg = QLabel()

        self.lang_manager = language_manager
        self._languages = ["ru", "en"]
        self._current_lang = "en"
        self.lang_manager.set_language(self._current_lang)
        self._setup_ui()
        self._setup_status_bar()
        self._setup_menu_bar()
        self.retranslate()
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.update_cheker.message.connect(self.set_status_msg)
        self.button.clicked.connect(self.on_button_click)
        self.update_btn.clicked.connect(updater.run)

    def _setup_ui(self) -> None:
        self.setWindowTitle("Click Me Demo")
        self.setGeometry(100, 100, 300, 150)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Button
        self.button = QPushButton()
        layout.addWidget(self.button)

        # Greeting label
        self.greet_label = QLabel()
        layout.addWidget(self.greet_label)

        # Label
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Update btn
        self.update_btn = QPushButton()
        layout.addWidget(self.update_btn)

        # Timer for hiding the message
        self.hide_label = QTimer()
        self.hide_label.timeout.connect(self.clear_label)
        self.hide_label.setSingleShot(True)  # Fire only once

        self.hide_status_msg = QTimer()
        self.hide_status_msg.timeout.connect(self.status_msg.clear)
        self.hide_label.setSingleShot(True)  # Fire only once

    def _setup_menu_bar(self) -> None:
        menu = self.menuBar()
        self.help_menu = menu.addMenu("")
        self.upd_checker_action = self.help_menu.addAction("")
        self.upd_checker_action.triggered.connect(self.update_cheker.check_for_updates)

    def set_status_msg(self, msg: str) -> None:
        self.status_msg.setText(msg)
        self.hide_status_msg.start(3000)  # 3000 milliseconds = 3 seconds

    def _setup_status_bar(self) -> None:
        status_bar = self.statusBar()
        status_bar.addWidget(self.status_msg)

    def on_button_click(self) -> None:
        self.change_lang()
        self.retranslate()
        self.hide_label.start(3000)

    def change_lang(self) -> None:
        if self._current_lang == "en":
            self._current_lang = "ru"
            self.lang_manager.set_language("ru")
        else:
            self._current_lang = "en"
            self.lang_manager.set_language("en")

    def clear_label(self) -> None:
        self.label.setText("")

    def retranslate(self) -> None:
        self.label.setText(
            _("Language changed to: {lang}").format(lang=self._current_lang)
        )
        self.greet_label.setText(_("Hello World!"))
        self.button.setText(_("Change language"))
        self.help_menu.setTitle(_("Help"))
        self.upd_checker_action.setText(_("Check for updates"))
        self.update_btn.setText(_("Update app"))


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
