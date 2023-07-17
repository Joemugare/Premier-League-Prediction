# -*- coding: utf-8 -*-

import tkinter as tk
import requests
import time

def getweather():
    city = textfield.get()
    api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=abb54687f0029b17322ac8ed183fbe14"
    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    temp = int(json_data['main']['temp'] - 273.15)
    temp_min = int(json_data['main']['temp_min'] - 273.15)
    temp_max = int(json_data['main']['temp_max'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']
    sunrise = time.strftime("%H:%M:%S", time.gmtime(json_data['sys']['sunrise'] - 21600))
    sunset = time.strftime("%H:%M:%S", time.gmtime(json_data['sys']['sunset'] - 21600))

    final_info = condition + "\n" + str(temp) + "\u00b0C"
    final_data = (
        "Max Temp: " + str(temp_max) + "\n" +
        "Min Temp: " + str(temp_min) + "\n" +
        "Pressure: " + str(pressure) + "\n" +
        "Humidity: " + str(humidity) + "\n" +
        "Wind Speed: " + str(wind) + "\n" +
        "Sunrise: " + sunrise + "\n" +
        "Sunset: " + sunset
    )
    label1.config(text=final_info)
    label2.config(text=final_data)

canvas = tk.Tk()
canvas.geometry("650x550")
canvas.title("Weather App")
canvas.configure(bg="blue")  # Set the background color to blue

# Set fonts
title_font = ("poppins", 30, "bold")
label_font = ("poppins", 12, "bold")

# Define text field
textfield = tk.Entry(canvas, font=title_font)
textfield.pack(pady=20)
textfield.focus()
textfield.bind('<Return>', lambda event: getweather())

# Label data
label1 = tk.Label(canvas, font=title_font)
label1.pack()
label2 = tk.Label(canvas, font=label_font)
label2.pack()

canvas.mainloop() 
