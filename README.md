# 🌦️ WeatherNow — Python Weather Application

A modern **Python weather application** built with **Tkinter**, **Object-Oriented Programming (OOP)**, and the **OpenWeatherMap API**.

WeatherNow allows users to search for a city and view current weather conditions, weather details, and a 5-day forecast in a graphical desktop interface.

---

## ✨ Features

* 🔍 Search for weather by city
* 🌡️ Current temperature
* 🌤️ Weather condition and description
* 🌡️ Feels-like temperature
* 💧 Humidity
* 💨 Wind speed
* 🧭 Atmospheric pressure
* 🌅 Sunrise and sunset times
* 📅 5-day weather forecast
* 🌡️ Switch between **Celsius (°C)** and **Fahrenheit (°F)**
* ⚠️ Error handling for invalid cities and connection problems
* 🖥️ Clean Tkinter graphical interface

---

## 🛠️ Technologies Used

* **Python**
* **Tkinter** — Graphical User Interface
* **Requests** — API requests
* **OpenWeatherMap API** — Weather data
* **Object-Oriented Programming (OOP)**

The project separates responsibilities into classes for the API, weather data, and application interface.

---

## 📸 Application

WeatherNow provides a desktop interface with:

* City search
* Current weather card
* Weather details
* 5-day forecast
* Celsius/Fahrenheit toggle

The application starts with **Brisbane** as the default city.

---

## 📂 Project Structure

```text
WeatherNow/
│
├── weather_app.py
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

### 2. Open the project folder

```bash
cd YOUR-REPOSITORY
```

### 3. Install the required package

```bash
pip install requests
```

The project uses the `requests` package to communicate with the weather API.

### 4. Add your API key

The application uses the **OpenWeatherMap API** to retrieve weather information.

For security, don't publish your API key directly in a public GitHub repository. Store it securely, ideally using an environment variable.

---

## ▶️ Run the Application

Run:

```bash
python weather_app.py
```

The Tkinter application will open and allow you to search for cities and view their weather.

---

## 🧱 OOP Structure

This project was also built to practise **Object-Oriented Programming**.

### `WeatherAPI`

Responsible for communicating with OpenWeatherMap and retrieving current weather and forecast information.

### `WeatherData`

Responsible for taking the API response and converting the information into useful values such as temperature, humidity, wind, sunrise, sunset, and forecast data.

### `WeatherApp`

Responsible for creating and controlling the Tkinter graphical interface.

---

## 🌡️ Celsius & Fahrenheit

The application can switch between Celsius and Fahrenheit without making another API request.

```text
Celsius → Fahrenheit
°C      → °F
```

The conversion is handled directly inside the application.

---

## 🧠 What I Learned

This project helped me practise:

* Python classes and objects
* Object-Oriented Programming
* Working with APIs
* Handling JSON data
* Using external Python libraries
* Tkinter GUI development
* Error handling
* Properties
* Static methods
* Working with dates and times
* Converting temperature units
* Organising a larger Python project

---

## 🚀 Future Improvements

Possible improvements for future versions:

* 🌍 Add more detailed weather information
* 📍 Add automatic location detection
* 🌙 Add light/dark mode
* 📊 Add weather charts
* 🗺️ Add maps
* 💾 Save favourite cities
* 🔔 Add weather alerts
* 📱 Create a mobile/web version

---

## 📄 License

This project was created as part of my journey learning **Python and real-world software development**.

---

### 🐍 Built with Python

**WeatherNow** is a practical project focused on taking Python knowledge and turning it into a real working application.
