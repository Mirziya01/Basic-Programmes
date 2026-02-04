import sys
import os
import requests

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal


# -------------------- Worker Thread --------------------

class WeatherWorker(QThread):
    success = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, city: str, api_key: str):
        super().__init__()
        self.city = city
        self.api_key = api_key

    def run(self):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": self.city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "en",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            self.success.emit(response.json())

        except requests.exceptions.HTTPError as e:
            status = response.status_code
            errors = {
                400: "Bad Request:\nCheck city name.",
                401: "Unauthorized:\nInvalid API key.",
                403: "Forbidden:\nAccess denied.",
                404: "City not found.",
                500: "Server error.\nTry again later.",
            }
            self.error.emit(errors.get(status, str(e)))

        except requests.exceptions.ConnectionError:
            self.error.emit("Connection error.\nCheck internet.")
        except requests.exceptions.Timeout:
            self.error.emit("Request timed out.")
        except requests.exceptions.RequestException as e:
            self.error.emit(str(e))


# -------------------- Main App --------------------

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENWEATHER_API_KEY environment variable not set")

        self.init_widgets()
        self.init_ui()

    def init_widgets(self):
        self.city_label = QLabel("Enter City Name")
        self.city_input = QLineEdit()
        self.get_weather_button = QPushButton("Get Weather")

        self.temperature_label = QLabel("")
        self.emoji_label = QLabel("")
        self.description_label = QLabel("")

    def init_ui(self):
        self.setWindowTitle("Weather App")

        layout = QVBoxLayout(self)
        for widget in (
            self.city_label,
            self.city_input,
            self.get_weather_button,
            self.temperature_label,
            self.emoji_label,
            self.description_label,
        ):
            if isinstance(widget, (QLabel, QLineEdit)):
                widget.setAlignment(Qt.AlignCenter)
            layout.addWidget(widget)

        self.city_input.setPlaceholderText("e.g. London")

        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: Calibri;
            }
            QLabel#city_label {
                font-size: 70px;
                font-style: italic;
            }
            QLineEdit {
                font-size: 28px;
            }
            QPushButton {
                font-size: 24px;
                font-weight: bold;
            }
            QLabel#temperature {
                font-size: 64px;
            }
            QLabel#emoji {
                font-size: 96px;
                font-family: "Segoe UI Emoji";
            }
            QLabel#description {
                font-size: 40px;
            }
        """)

        self.temperature_label.setObjectName("temperature")
        self.emoji_label.setObjectName("emoji")
        self.description_label.setObjectName("description")

        self.get_weather_button.clicked.connect(self.get_weather)

    # -------------------- Logic --------------------

    def get_weather(self):
        city = self.city_input.text().strip()

        if not city:
            self.display_error("Please enter a city name.")
            return

        self.set_loading_state(True)

        self.worker = WeatherWorker(city, self.api_key)
        self.worker.success.connect(self.display_weather)
        self.worker.error.connect(self.display_error)
        self.worker.finished.connect(lambda: self.set_loading_state(False))
        self.worker.start()

    def set_loading_state(self, loading: bool):
        self.get_weather_button.setDisabled(loading)
        self.get_weather_button.setText("Loading..." if loading else "Get Weather")

    def display_error(self, message: str):
        self.temperature_label.setStyleSheet("color: red; font-size: 28px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data: dict):
        self.temperature_label.setStyleSheet("color: black; font-size: 64px;")

        temp_c = data["main"]["temp"]
        temp_f = (temp_c * 9 / 5) + 32

        weather = data["weather"][0]
        description = weather["description"].capitalize()
        emoji = self.get_weather_emoji(weather["main"])

        self.temperature_label.setText(f"{temp_c:.0f} °C / {temp_f:.0f} °F")
        self.description_label.setText(description)
        self.emoji_label.setText(emoji)

    @staticmethod
    def get_weather_emoji(condition: str) -> str:
        return {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Fog": "🌫️",
            "Haze": "🌫️",
        }.get(condition, "🌈")


# -------------------- Entry Point --------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
