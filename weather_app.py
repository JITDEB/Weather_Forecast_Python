import requests
import tkinter as tk
from tkinter import ttk
from geopy.geocoders import Nominatim
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_weather(city):
    api_key = "1495ace3fc2b10f9b3e127785b12c3e5"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    return response.json()

def update_weather():
    city = city_entry.get()
    weather_data = get_weather(city)

    if weather_data["cod"] != "404":
        if "main" in weather_data:
            main = weather_data["main"]
            weather_desc = weather_data["weather"][0]["description"]
            temperature = main["temp"]
            humidity = main["humidity"]
            pressure = main["pressure"]
            wind_speed = weather_data["wind"]["speed"]
            aqi_index = "AQI data here"  # Integrate AQI data

            # Update labels
            temp_label.config(text=f"Temperature: {temperature}°C")
            humidity_label.config(text=f"Humidity: {humidity}%")
            pressure_label.config(text=f"Pressure: {pressure} hPa")
            wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
            description_label.config(text=f"Description: {weather_desc}")
            aqi_label.config(text=f"AQI Index: {aqi_index}")

            # Change background based on weather
            set_background(weather_desc)
        else:
            error_label.config(text="Error: 'main' key not found in the response.")
    else:
        error_label.config(text="City Not Found!")

def set_background(weather_desc):
    try:
        if "clear" in weather_desc.lower():
            bg_image = ImageTk.PhotoImage(Image.open("clear_sky.jpg"))
        elif "cloud" in weather_desc.lower():
            bg_image = ImageTk.PhotoImage(Image.open("cloudy.jpg"))
        elif "rain" in weather_desc.lower():
            bg_image = ImageTk.PhotoImage(Image.open("rain.jpg"))
        else:
            bg_image = ImageTk.PhotoImage(Image.open("default.jpg"))
        
        bg_label.config(image=bg_image)
        bg_label.image = bg_image
    except Exception as e:
        error_label.config(text=f"Error loading background image: {e}")

def add_city():
    city = city_entry.get()
    if city not in cities_list:
        cities_list.append(city)
        cities_listbox.insert(tk.END, city)

def plot_data():
    try:
        temperatures = [get_weather(city)['main']['temp'] for city in cities_list]

        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(1, 1, 1)
        plot.bar(cities_list, temperatures, color='blue')
        plot.set_title('Temperature in Different Cities')
        plot.set_ylabel('Temperature (°C)')
        plot.set_xlabel('City')

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    except Exception as e:
        error_label.config(text=f"Error plotting data: {e}")

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("800x600")

bg_label = tk.Label(root)
bg_label.place(relwidth=1, relheight=1)

city_label = tk.Label(root, text="Enter City:", bg="lightgray")
city_label.pack(pady=10)

city_entry = tk.Entry(root)
city_entry.pack(pady=10)

search_button = tk.Button(root, text="Search", command=update_weather)
search_button.pack(pady=10)

add_city_button = tk.Button(root, text="Add City", command=add_city)
add_city_button.pack(pady=10)

temp_label = tk.Label(root, text="Temperature: ", bg="lightgray")
temp_label.pack(pady=5)

humidity_label = tk.Label(root, text="Humidity: ", bg="lightgray")
humidity_label.pack(pady=5)

pressure_label = tk.Label(root, text="Pressure: ", bg="lightgray")
pressure_label.pack(pady=5)

wind_label = tk.Label(root, text="Wind Speed: ", bg="lightgray")
wind_label.pack(pady=5)

description_label = tk.Label(root, text="Description: ", bg="lightgray")
description_label.pack(pady=5)

aqi_label = tk.Label(root, text="AQI Index: ", bg="lightgray")
aqi_label.pack(pady=5)

error_label = tk.Label(root, text="", fg="red", bg="lightgray")
error_label.pack(pady=5)

cities_list = []
cities_listbox = tk.Listbox(root)
cities_listbox.pack(pady=10)

plot_button = tk.Button(root, text="Plot Data", command=plot_data)
plot_button.pack(pady=10)

root.mainloop()