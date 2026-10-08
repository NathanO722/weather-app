"""
WeatherNow — OOP Weather Application
Requirements:
    pip install requests
Run:
    python weather_app.py

Uses the OpenWeatherMap Current Weather and 5 Day / 3 Hour Forecast APIs.
Keep your API key private; do not publish it in a public repository.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import requests


API_KEY = "e15551dee3e98eed23b8a0226cd84217"
BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherAPI:
    """Handles communication with OpenWeatherMap."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()

    def _request(self, endpoint, city):
        try:
            response = self.session.get(
                f"{BASE_URL}/{endpoint}",
                params={"q": city, "appid": self.api_key, "units": "metric"},
                timeout=10,
            )
            if response.status_code == 404:
                raise ValueError("City not found. Check the spelling and try again.")
            if response.status_code == 401:
                raise ValueError("The API key was rejected. Check that it is active.")
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise ConnectionError("The weather service took too long to respond.")
        except requests.ConnectionError:
            raise ConnectionError("Could not connect. Check your internet connection.")
        except requests.HTTPError:
            raise ConnectionError("The weather service is temporarily unavailable.")

    def get_current(self, city):
        return self._request("weather", city)

    def get_forecast(self, city):
        return self._request("forecast", city)


class WeatherData:
    """Converts API responses into convenient display values."""

    def __init__(self, current, forecast):
        self.current = current
        self.forecast = forecast

    @property
    def city(self):
        return self.current["name"]

    @property
    def country(self):
        return self.current["sys"].get("country", "")

    @property
    def temperature(self):
        return round(self.current["main"]["temp"])

    @property
    def feels_like(self):
        return round(self.current["main"]["feels_like"])

    @property
    def description(self):
        return self.current["weather"][0]["description"].title()

    @property
    def icon(self):
        return self.current["weather"][0]["icon"]

    @property
    def humidity(self):
        return self.current["main"]["humidity"]

    @property
    def wind(self):
        return round(self.current["wind"].get("speed", 0) * 3.6)

    @property
    def pressure(self):
        return self.current["main"]["pressure"]

    @property
    def sunrise(self):
        return datetime.fromtimestamp(self.current["sys"]["sunrise"]).strftime("%I:%M %p")

    @property
    def sunset(self):
        return datetime.fromtimestamp(self.current["sys"]["sunset"]).strftime("%I:%M %p")

    def daily_forecast(self):
        """Select one forecast near midday for each of the next five dates."""
        grouped = {}
        for item in self.forecast["list"]:
            date = datetime.fromtimestamp(item["dt"])
            key = date.date()
            if key not in grouped or abs(date.hour - 12) < abs(
                datetime.fromtimestamp(grouped[key]["dt"]).hour - 12
            ):
                grouped[key] = item

        days = []
        for date, item in list(grouped.items())[:5]:
            weather = item["weather"][0]
            days.append({
                "day": date.strftime("%a"),
                "date": date.strftime("%b %d"),
                "temp": round(item["main"]["temp"]),
                "description": weather["description"].title(),
                "icon": weather["icon"],
            })
        return days


class WeatherApp:
    """Builds and controls the Tkinter weather interface."""

    BG = "#081426"
    PANEL = "#101f36"
    PANEL_LIGHT = "#172945"
    TEXT = "#f4f7ff"
    MUTED = "#a8b8d2"
    BLUE = "#367df5"
    BORDER = "#263b5c"

    def __init__(self, root):
        self.root = root
        self.api = WeatherAPI(API_KEY)
        self.unit = "C"
        self.weather_data = None
        self.root.title("WeatherNow | Live Weather")
        self.root.geometry("1100x760")
        self.root.minsize(900, 650)
        self.root.configure(bg=self.BG)

        self._build_ui()
        self.search_city("Brisbane")

    def _label(self, parent, text, size=12, color=None, bold=False, **kwargs):
        return tk.Label(
            parent, text=text, bg=kwargs.pop("bg", parent.cget("bg")),
            fg=color or self.TEXT, font=("Segoe UI", size, "bold" if bold else "normal"),
            **kwargs
        )

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.BG)
        header.pack(fill="x", padx=30, pady=(22, 16))
        self._label(header, "☀  WeatherNow", 22, bold=True).pack(side="left")
        self._label(header, "LIVE WEATHER  •  OPENWEATHERMAP", 9, self.MUTED, bold=True).pack(
            side="right", pady=9
        )

        # Search bar
        search = tk.Frame(self.root, bg=self.PANEL, highlightbackground=self.BORDER,
                          highlightthickness=1)
        search.pack(fill="x", padx=30, pady=(0, 20), ipady=5)
        self.city_entry = tk.Entry(
            search, bg=self.PANEL, fg=self.TEXT, insertbackground=self.TEXT,
            relief="flat", font=("Segoe UI", 13), borderwidth=0
        )
        self.city_entry.insert(0, "Brisbane")
        self.city_entry.pack(side="left", fill="x", expand=True, padx=(18, 10), ipady=10)
        self.city_entry.bind("<Return>", lambda _event: self._search_clicked())
        tk.Button(
            search, text="Search  →", command=self._search_clicked,
            bg=self.BLUE, fg="white", activebackground="#2866d4",
            activeforeground="white", relief="flat", bd=0, cursor="hand2",
            font=("Segoe UI", 11, "bold"), padx=22, pady=10
        ).pack(side="right", padx=8, pady=5)

        # Main content columns
        content = tk.Frame(self.root, bg=self.BG)
        content.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        content.columnconfigure(0, weight=3, uniform="columns")
        content.columnconfigure(1, weight=2, uniform="columns")
        content.rowconfigure(0, weight=1)

        left = tk.Frame(content, bg=self.BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        right = tk.Frame(content, bg=self.BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        # Current conditions card
        self.current_card = tk.Frame(left, bg=self.PANEL, highlightbackground=self.BORDER,
                                     highlightthickness=1)
        self.current_card.pack(fill="x")
        self.city_label = self._label(self.current_card, "Searching…", 19, bold=True)
        self.city_label.pack(anchor="w", padx=24, pady=(22, 2))
        self.date_label = self._label(self.current_card, "", 10, self.MUTED)
        self.date_label.pack(anchor="w", padx=24)

        temp_row = tk.Frame(self.current_card, bg=self.PANEL)
        temp_row.pack(fill="x", padx=24, pady=(20, 0))
        self.icon_label = self._label(temp_row, "☀", 48, "#ffd166")
        self.icon_label.pack(side="left", padx=(0, 18))
        self.temp_label = self._label(temp_row, "--°C", 52, bold=True)
        self.temp_label.pack(side="left")
        self.unit_button = tk.Button(
            temp_row, text="°C  |  °F", command=self._toggle_unit,
            bg=self.PANEL_LIGHT, fg=self.TEXT, activebackground=self.BLUE,
            activeforeground="white", relief="flat", bd=0, cursor="hand2",
            font=("Segoe UI", 10, "bold"), padx=10, pady=7
        )
        self.unit_button.pack(side="left", padx=(18, 0), pady=(12, 0))
        self.condition_label = self._label(self.current_card, "Loading conditions", 15, self.MUTED)
        self.condition_label.pack(anchor="w", padx=28, pady=(0, 18))

        self.feels_label = self._label(self.current_card, "Feels like --°", 11, self.MUTED)
        self.feels_label.pack(anchor="w", padx=26, pady=(0, 22))

        # Details
        self._label(left, "WEATHER DETAILS", 10, self.MUTED, bold=True).pack(
            anchor="w", pady=(22, 10)
        )
        details = tk.Frame(left, bg=self.BG)
        details.pack(fill="x")
        for col in range(2):
            details.columnconfigure(col, weight=1, uniform="details")
        self.detail_values = {}
        for index, (key, title, symbol) in enumerate([
            ("humidity", "Humidity", "◌"),
            ("wind", "Wind speed", "↗"),
            ("pressure", "Pressure", "▤"),
            ("sun", "Sunrise / Sunset", "☼"),
        ]):
            card = tk.Frame(details, bg=self.PANEL, highlightbackground=self.BORDER,
                            highlightthickness=1)
            card.grid(row=index // 2, column=index % 2, sticky="nsew",
                      padx=(0, 8) if index % 2 == 0 else (8, 0),
                      pady=(0, 12))
            self._label(card, f"{symbol}  {title}", 10, self.MUTED).pack(
                anchor="w", padx=15, pady=(13, 5)
            )
            value = self._label(card, "--", 16, bold=True)
            value.pack(anchor="w", padx=15, pady=(0, 14))
            self.detail_values[key] = value

        # Forecast panel
        forecast_card = tk.Frame(right, bg=self.PANEL, highlightbackground=self.BORDER,
                                  highlightthickness=1)
        forecast_card.pack(fill="both", expand=True)
        self._label(forecast_card, "5-DAY FORECAST", 11, self.MUTED, bold=True).pack(
            anchor="w", padx=20, pady=(20, 14)
        )
        self.forecast_rows = []
        for _ in range(5):
            row = tk.Frame(forecast_card, bg=self.PANEL_LIGHT)
            row.pack(fill="x", padx=12, pady=5)
            day = self._label(row, "--", 10, bold=True, width=7, anchor="w")
            day.pack(side="left", padx=(12, 4), pady=13)
            icon = self._label(row, "☀", 17, "#ffd166", width=3)
            icon.pack(side="left")
            desc = self._label(row, "—", 9, self.MUTED, anchor="w")
            desc.pack(side="left", fill="x", expand=True, padx=4)
            temp = self._label(row, "--°", 12, bold=True)
            temp.pack(side="right", padx=12)
            self.forecast_rows.append((day, icon, desc, temp))

        self.status = self._label(self.root, "Ready", 9, self.MUTED)
        self.status.pack(anchor="w", padx=32, pady=(0, 10))

    def _search_clicked(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showinfo("City required", "Enter a city name to search.")
            return
        self.search_city(city)

    def search_city(self, city):
        self.status.config(text=f"Getting weather for {city}…")
        self.root.config(cursor="watch")
        self.root.update_idletasks()
        try:
            current = self.api.get_current(city)
            forecast = self.api.get_forecast(city)
            data = WeatherData(current, forecast)
            self._display_weather(data)
            self.status.config(text=f"Updated just now  •  {data.city}, {data.country}")
        except (ValueError, ConnectionError, requests.RequestException) as error:
            self.status.config(text="Could not update weather")
            messagebox.showerror("Weather unavailable", str(error))
        finally:
            self.root.config(cursor="")

    def _format_temperature(self, celsius):
        """Format a Celsius value in the currently selected unit."""
        if self.unit == "F":
            return f"{round(celsius * 9 / 5 + 32)}°F"
        return f"{round(celsius)}°C"

    def _toggle_unit(self):
        """Switch between Celsius and Fahrenheit without another API request."""
        self.unit = "F" if self.unit == "C" else "C"
        if self.weather_data is not None:
            self._display_weather(self.weather_data)

    @staticmethod
    def _weather_symbol(icon_code):
        code = icon_code[:2]
        symbols = {
            "01": "☀", "02": "⛅", "03": "☁", "04": "☁",
            "09": "🌧", "10": "🌦", "11": "⛈", "13": "❄", "50": "🌫"
        }
        return symbols.get(code, "☁")

    def _display_weather(self, data):
        self.weather_data = data
        self.city_label.config(text=f"📍  {data.city}, {data.country}")
        self.date_label.config(text=datetime.now().strftime("%A, %d %B  •  %I:%M %p"))
        self.icon_label.config(text=self._weather_symbol(data.icon))
        self.temp_label.config(text=self._format_temperature(data.temperature))
        self.condition_label.config(text=data.description)
        self.feels_label.config(text=f"Feels like {self._format_temperature(data.feels_like)}")
        self.detail_values["humidity"].config(text=f"{data.humidity}%")
        self.detail_values["wind"].config(text=f"{data.wind} km/h")
        self.detail_values["pressure"].config(text=f"{data.pressure} hPa")
        self.detail_values["sun"].config(text=f"{data.sunrise}  /  {data.sunset}")

        for index, (day, icon, desc, temp) in enumerate(self.forecast_rows):
            if index < len(data.daily_forecast()):
                item = data.daily_forecast()[index]
                day.config(text=f'{item["day"]} {item["date"]}')
                icon.config(text=self._weather_symbol(item["icon"]))
                desc.config(text=item["description"])
                temp.config(text=self._format_temperature(item["temp"]))
            else:
                day.config(text="—")
                icon.config(text="")
                desc.config(text="No forecast")
                temp.config(text="—")


def main():
    root = tk.Tk()
    WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
