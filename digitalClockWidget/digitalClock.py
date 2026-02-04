import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QFontDatabase


class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()

        self.time_label = QLabel()
        self.timer = QTimer(self)

        self.init_ui()

    def init_ui(self):
        # Window setup
        self.setWindowTitle("Digital Clock")
        self.resize(600, 200)
        self.setStyleSheet("background-color: black;")

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.time_label)

        # Label setup
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("""
            color: hsl(111, 100%, 50%);
        """)

        # Load custom font safely
        font = self.load_font("DS-DIGIT.TTF", fallback="Arial", size=150)
        self.time_label.setFont(font)

        # Timer setup
        self.timer.timeout.connect(self.update_time)
        self.timer.start(500)  # better responsiveness & accuracy

        self.update_time()

    def load_font(self, font_path, fallback="Arial", size=150):
        """
        Safely loads a custom font.
        Falls back to a system font if loading fails.
        """
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                return QFont(families[0], size)

        # Fallback font
        return QFont(fallback, size)

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.time_label.setText(current_time)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    clock = DigitalClock()
    clock.show()

    sys.exit(app.exec_())
