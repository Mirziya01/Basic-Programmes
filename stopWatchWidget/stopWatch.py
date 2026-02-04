import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel,
    QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer


class StopWatch(QWidget):
    def __init__(self):
        super().__init__()

        # Time handling
        self.elapsed_ms = 0
        self.elapsed_timer = QElapsedTimer()

        # UI elements
        self.time_label = QLabel("00:00:00.00")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("Reset")

        # Timer for UI updates
        self.timer = QTimer(self)
        self.timer.setInterval(10)

        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.setWindowTitle("Stopwatch")
        self.setFixedSize(520, 260)

        self.time_label.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.time_label)

        hbox = QHBoxLayout()
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)

        vbox.addLayout(hbox)

        self.stop_button.setEnabled(False)

        self.setStyleSheet("""
            QLabel {
                font-size: 110px;
                font-family: "JetBrains Mono", Consolas, monospace;
                background-color: hsl(200, 100%, 85%);
                border-radius: 20px;
                padding: 20px;
            }
            QPushButton {
                font-size: 36px;
                padding: 15px;
                font-weight: bold;
                font-family: Calibri;
            }
        """)

    def connect_signals(self):
        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)
        self.timer.timeout.connect(self.update_display)

        # Keyboard shortcuts
        self.start_button.setShortcut("Space")
        self.reset_button.setShortcut("R")

    def start(self):
        if not self.elapsed_timer.isValid():
            self.elapsed_timer.start()
        else:
            self.elapsed_timer.restart()

        self.timer.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop(self):
        self.timer.stop()
        self.elapsed_ms += self.elapsed_timer.elapsed()
        self.elapsed_timer.invalidate()

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def reset(self):
        self.timer.stop()
        self.elapsed_timer.invalidate()
        self.elapsed_ms = 0

        self.time_label.setText("00:00:00.00")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_display(self):
        total_ms = self.elapsed_ms + self.elapsed_timer.elapsed()
        self.time_label.setText(self.format_time(total_ms))

    @staticmethod
    def format_time(ms):
        hours = ms // 3_600_000
        minutes = (ms // 60_000) % 60
        seconds = (ms // 1_000) % 60
        centiseconds = (ms // 10) % 100
        return f"{hours:02}:{minutes:02}:{seconds:02}.{centiseconds:02}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StopWatch()
    window.show()
    sys.exit(app.exec_())

