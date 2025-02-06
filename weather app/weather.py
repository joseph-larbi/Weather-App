from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image, ImageTk

root = Tk()
root.title("HETHS Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

def getWeather():
    city = textfield.get()

    try:
        # Geolocation
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        if not location:
            messagebox.showerror("Error", f"City '{city}' not found!")
            return

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        # Timezone
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # Weather API
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=64efa9f6fa3e46e9400779a71938aff0&units=metric"
        json_data = requests.get(api).json()

        if json_data["cod"] == 200:
            description = json_data['weather'][0]['description']
            temp = json_data['main']['temp']
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']

            # Update labels
            t.config(text=(temp, "°C"))
            d.config(text=description)
            p.config(text=f"{pressure} hPa")
            h.config(text=f"{humidity}%")
            w.config(text=f"{wind} m/s")
        else:
            messagebox.showerror("Error", f"City '{city}' not found!")
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data. Please try again.")

# Search box
Search_image = PhotoImage(file="search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

Search_icon = PhotoImage(file="search_icon.png")
myimage_icon = Button(image=Search_icon, border=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=33)

# Logo
logo_image = Image.open("logo.png")
resized_logo = logo_image.resize((150, 100))  # Resize logo
Logo_image = ImageTk.PhotoImage(resized_logo)
logo = Label(image=Logo_image)
logo.place(x=150, y=100)

# Button box
Frame_image = PhotoImage(file="box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(side=BOTTOM, pady=4, padx=4)

# Time
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvectica", 20))
clock.place(x=30, y=130)

# Labels
label1 = Label(root, text="WIND", font=("Helvetca", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetca", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetca", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE", font=("Helvetca", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

# Dynamic data
t = Label(font=("arial", 70, "bold"), fg="#ee665d")
t.place(x=400, y=150)

c = Label(font=("arial", 15, 'bold'))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
w.place(x=130, y=430)

h = Label(text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
h.place(x=280, y=430)

d = Label(text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
d.place(x=460, y=430)

p = Label(text="...", font=("arial", 20, 'bold'), bg="#1ab5ef")
p.place(x=670, y=430)

root.mainloop()
