#Imports
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinterweb
import requests
import json 
from geopy.geocoders import Nominatim
import os

#API key
API_KEY = os.environ['API_KEY']

#Window parameters
window = tk.Tk()
window.title("Heat Check")
window.geometry("400x400")

#Colors
tab1bg = "indianred"
tab2bg = "skyblue"
tab2widgetcolor = "skyblue"
tab2textcolor = "black"
tab2buttonbg = "darkturquoise"
tab2buttonhighlightcolor = "white"
tab3bg = "sandybrown"
tab4bg = "cornflowerblue"

#Fonts
Font10 = ("Times New Roman", 10)

#App window
notebook = ttk.Notebook(window)
notebook.pack(expand = True, fill = "both")

#Tab manager
tab1 = tk.Frame(notebook, width = 400, height = 400, bg = tab1bg)
tab2 = tk.Frame(notebook, width = 400, height = 400, bg = tab2bg)
tab3 = tk.Frame(notebook, width = 400, height = 1000)
tab4 = tk.Frame(notebook, width = 400, height = 1000)
tab5 = tkinterweb.HtmlFrame(notebook)
tab5.load_website("https://graphical.weather.gov/sectors/conus.php#tabs")

tab1.pack(fill = "both", expand = 1)
tab2.pack(fill = "both", expand = 1)
tab3.pack(fill = "both", expand = 1)
tab4.pack(fill = "both", expand = 1)
tab5.pack(fill="both", expand=True)

notebook.add(tab1, text = "Heat Risk Calculator")
notebook.add(tab2, text = "Water Progress Bar")
notebook.add(tab3, text = "Heat Stroke Info")
notebook.add(tab4, text = "Dehydration Info")
notebook.add(tab5, text = "Map")

#1st tab 0000000000000000000000000000000000000000000000000000000000000000000000000
#111111111111111111111111111111111111111111111111111111111111111111111111111111111

#Button function
def myClick():
  
    #Converts location to longitude and latitude
    geolocator = Nominatim(user_agent = "Congressional App Competition")
    coords = geolocator.geocode(str(address.get()))

    #Check if address exists, give error message if not
    try:
      
        #Gets openweather API data from longitude and latitude
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=" + str(coords.latitude) + "&lon=" + str(coords.longitude) + "&appid="+ API_KEY + "&units=imperial")

        #Pulls info from API data
        json_data = json.loads(response.text)
        temp = json_data["main"]["temp"]
        humidity = json_data["main"]["humidity"]
        city1 = json_data["name"]
        country1 = json_data["sys"]["country"]

        #Casts desired data to useful variables
        T = float(temp)
        RH = float(humidity)
        city = str(city1)
        country = str(country1)

        #Calculates Heat index (HI) from temperature and humidity API data
        if T < 80:
            HI = 0.5 * (T + 61.0 + ((T - 68.0) * 1.2) + (RH * 0.094))
        else:
            HI = -42.379 + (2.04901523*T) + (10.14333127*RH) - (0.22475541*T*RH) - (0.00683783*T*T) - (0.05481717*RH*RH) + (0.00122874*T*T*RH) + (0.00085282*T*RH*RH) - (0.00000199*T*T*RH*RH)
        if RH < 13 and 80 <= T <= 112:
            HI -= ((13 - RH) / 4) * (((17 - abs(T - 95)) / 17) ^ (1 / 2))
        elif RH > 85 and 80 <= T <= 87:
            HI += ((RH - 85) / 10) * ((87 - T) / 5)

        #Fills info labels with extracted data
        Location.config(font = Font10, text = "Location: " + str(coords.latitude) + ", " +str(coords.longitude))
        City.config(font = Font10, text = "City: " + str(city) + ", " + str(country))
        Temp.config(font = Font10, text = "Temperature: " + str(T) + "°F")
        RelHum.config(font = Font10, text = "Relative Humidity: " + str(RH) + "%")
        HILabel.config(font = Font10, text = "Heat Index: " + str(round(HI, 2)) + "°F")

        #Displays heat danger based on HI
        if (HI < 80):
            Caution.configure(text = "Minimal Heat Stroke Risk", fg = "teal")
        if (80 <= HI < 90):
            Caution.configure(text = "Caution: Fatigue possible with prolonged exposure and/or physical activity", fg = "blue")
        if (90 <= HI < 103):
            Caution.configure(text = "Extreme Caution: Heat stroke, heat cramps, or heat exhaustion possible with prolonged exposure and/or physical activity", fg = "green")
        if (103 <= HI < 124):
            Caution.configure(text = "Danger: Heat cramps or heat exhaustion likely, and heat stroke possible with prolonged exposure and/or physical activity", fg = "orange")
        if (124 <= HI):
            Caution.configure(text = "Extreme Danger: Heat stroke highly likely", fg = "red")

        #Resets error message
        AddressError.config(text = " ", bg = tab1bg)
      
    #prompt user if input is invalid
    except:
        AddressError.config(text = "Type in a real address", fg = "yellow")

#tab1 geometry
tab1widgetpadx = 0
tab1widgetpady = 5

#establishes frame to center widgets
frame1 = tk.Frame(tab1, bg = tab1bg)
frame1.pack(anchor = "n", pady = tab1widgetpady)

#box for user input of desired location
address = tk.Entry(frame1, font = Font10)
address.pack(pady = tab1widgetpady)

#button converts address to heat index of address entered in text box
button = tk.Button(frame1, font = Font10, text = "Get Heat Stroke Risk", command = myClick)
button.pack(pady = tab1widgetpady)

#placeholder labels for future information, filled by button click
Location= tk.Label(frame1, font = Font10, text = "Location: ", bg = tab1bg, justify = "left")
Location.pack(anchor = "w", padx = tab1widgetpadx, pady = tab1widgetpady)
City = tk.Label(frame1, font = Font10, text = "City: ", bg = tab1bg)
City.pack(anchor = "w", padx = tab1widgetpadx, pady = tab1widgetpady)
Temp = tk.Label(frame1, font = Font10, text = "Temperature: ", bg = tab1bg)
Temp.pack(anchor = "w", padx = tab1widgetpadx, pady = tab1widgetpady)
RelHum = tk.Label(frame1, font = Font10, text = "Relative Humidity: ", bg = tab1bg)
RelHum.pack(anchor = "w", padx = tab1widgetpadx, pady = tab1widgetpady)
HILabel = tk.Label(frame1, font = Font10, text = "Heat Index: ", bg = tab1bg)
HILabel.pack(anchor = "w", padx = tab1widgetpadx, pady = tab1widgetpady)
Caution = tk.Label(frame1, font = Font10, text = " ", bg = tab1bg, wraplength = 245)
Caution.pack(padx = tab1widgetpadx, pady = tab1widgetpady)
AddressError = tk.Label(tab1, font = Font10, bg = tab1bg)
AddressError.pack(padx = tab1widgetpadx, pady = tab1widgetpady)

#2nd tab 1111111111111111111111111111111111111111111111111111111111111111111111111
#222222222222222222222222222222222222222222222222222222222222222222222222222222222

#determines sex from button click
def setsex(input):
    global sex
    if input == True:
        sex = True
    else:
        sex = False

#establishes frame to center widgets
frame2 = tk.Frame(tab2, bg = tab2bg)
frame2.pack(anchor = "n")
tab2widgetpadx = 0
tab2widgetpady = 5

#user selects their sex
frame2sex = tk.Frame(frame2, bg = tab2bg)
frame2sex.grid(sticky = "nw", row = 0, column = 0) 
male = tk.Button(frame2sex, text = "Male", font = Font10, command = lambda: setsex(True), bg = tab2widgetcolor, fg = tab2textcolor, activebackground = tab2buttonbg, highlightcolor = tab2buttonhighlightcolor)
male.grid(sticky = "n", row = 0, column = 0, padx = tab2widgetpadx, pady = tab2widgetpady) 
female = tk.Button(frame2sex, text = "Female", font = Font10, command = lambda: setsex(False), bg = tab2widgetcolor, fg = tab2textcolor, activebackground = tab2buttonbg, highlightcolor = tab2buttonhighlightcolor)
female.grid(sticky = "n", row = 0, column = 1, pady = tab2widgetpady, padx = 5) 

#user input box for weight
weightLabel = tk.Label(frame2, text = "Weight (lbs):", font = Font10, bg = tab2widgetcolor, fg = tab2textcolor)
weightLabel.grid(sticky = "w", row = 1, column = 0, padx = tab2widgetpadx, pady = tab2widgetpady) 
weight = tk.Entry(frame2)
weight.grid(sticky = "e", row = 1, column = 1, padx = tab2widgetpadx, pady = tab2widgetpady) 

#user input box for exercise time
exerciseLabel = tk.Label(frame2, text = "Exercise Amount (min):", font = Font10, bg = tab2widgetcolor, fg = tab2textcolor)
exerciseLabel.grid(sticky = "w", row = 2, column = 0, padx = tab2widgetpadx, pady = tab2widgetpady) 
exercisetime = tk.Entry(frame2)
exercisetime.grid(sticky = "e", row = 2, column = 1, padx = tab2widgetpadx, pady = tab2widgetpady) 

#water drunk to required ratio
TotalWaterDrunk = 0
WaterRatioLabel = tk.Label(frame2, text = "Progress: ", font = Font10, bg = tab2widgetcolor, fg = tab2textcolor)
WaterRatioLabel.grid(row = 3, column = 0, columnspan = 2, padx = tab2widgetpadx, pady = tab2widgetpady) 

#hydration bar
s = ttk.Style()
s.theme_use('alt')
s.configure("slategrey.Horizontal.TProgressbar", background = "slategrey")
s.configure("red.Horizontal.TProgressbar", background = 'red')
hydration_lvls = ttk.Progressbar(frame2, style = "slategrey.Horizontal.TProgressbar", orient = "horizontal", length = 200, mode = "determinate")
hydration_lvls.grid(row = 4, column = 0, columnspan = 2, padx = tab2widgetpadx, pady = tab2widgetpady)

#update made to progress bar from button click
def step():
    try:
        global tempTotalWaterDrunk
        global TotalWaterDrunk
        global WN
        global templength
        tempTotalWaterDrunk = TotalWaterDrunk
        #calculates estimated daily water intake from weight, exercise, and sex
        W = int(weight.get())
        ET = int(exercisetime.get())
        if sex == True:
            WN = 0.5 * W + 2 * ET / 5
        if sex == False:
            WN = 0.45 * W + 2 * ET / 5
        WD = int(waterdrunk.get())  #water drunk (in oz)
        templength = 100 * TotalWaterDrunk / WN

        TotalWaterDrunk += WD
        WaterRatioLabel.config(text = "Progress: " + str(TotalWaterDrunk) + "oz. / " + str(WN) + "oz., " + str(round(100 * TotalWaterDrunk / WN, 2)) + "%")

        #changes bar color to red once daily intake is exceeded
        if TotalWaterDrunk > WN:
            hydration_lvls.configure(style = "red.Horizontal.TProgressbar")

        #adds to the progress bar the portion of calculated intake completed
        hydration_lvls["value"] += 100 * WD / WN

        #resets error message
        ErrorLabel2.config(text = " ")

    #prompt user if input is invalid
    except:
        ErrorLabel2.config(text = "Please select a sex and type in all the information", font = Font10, bg = tab2widgetcolor, fg = "red")

def undostep():
    try:
        global tempTotalWaterDrunk
        global TotalWaterDrunk
        global WN
        global templength
        TotalWaterDrunk = tempTotalWaterDrunk
        WaterRatioLabel.config(text = "Progress: " + str(TotalWaterDrunk) + "oz. / " + str(WN) + "oz., " + str(round(100 * TotalWaterDrunk / WN, 2)) + "%")
        hydration_lvls["value"] = templength
        if TotalWaterDrunk < WN:
            hydration_lvls.configure(style = "slategrey.Horizontal.TProgressbar")
    except:
        ErrorLabel2.config(text = "Cannot undo action", font = Font10, bg = tab2widgetcolor, fg = "red")

def resetstep():
    try:
        global TotalWaterDrunk
        TotalWaterDrunk = 0
        WaterRatioLabel.config(text = "Progress: ")
        hydration_lvls["value"] = 0
        hydration_lvls.configure(style = "slategrey.Horizontal.TProgressbar")
    except:
        ErrorLabel2.config(text = "Cannot reset progressbar", font = Font10, bg = tab2widgetcolor, fg = "red")

#button to update progress bar
juicers = tk.Button(frame2, text = "Add Amount of Water Drunken", font = Font10, command = step, bg = tab2widgetcolor, fg = tab2textcolor, activebackground = tab2buttonbg, highlightcolor = tab2buttonhighlightcolor)
juicers.grid(sticky = "w",  row = 5, column = 0, padx = tab2widgetpadx, pady = tab2widgetpady) 

#user input box for water drunk
waterdrunk = tk.Entry(frame2)
waterdrunk.grid(sticky = "e", row = 5, column = 1, padx = tab2widgetpadx, pady = tab2widgetpady) 

#undo button
undo = tk.Button(frame2, text = "Undo", font = Font10, command = undostep, bg = tab2widgetcolor, fg = tab2textcolor, activebackground = tab2buttonbg, highlightcolor = tab2buttonhighlightcolor)
undo.grid(sticky = "e", row = 6, column = 1, padx = tab2widgetpadx, pady = tab2widgetpady)

#reset button
reset = tk.Button(frame2, text = "Reset", font = Font10, command = resetstep, bg = tab2widgetcolor, fg = tab2textcolor, activebackground = tab2buttonbg, highlightcolor = tab2buttonhighlightcolor)
reset.grid(sticky = "w", row = 6, column = 1, padx = tab2widgetpadx, pady = tab2widgetpady)

#placeholder invisible error message
ErrorLabel2 = tk.Label(frame2, bg = tab2widgetcolor)
ErrorLabel2.grid(row = 7, column = 0, columnspan = 2, padx = tab2widgetpadx, pady = tab2widgetpady) 

#3rd tab 2222222222222222222222222222222222222222222222222222222222222222222222222
#333333333333333333333333333333333333333333333333333333333333333333333333333333333

#reads heatstroke risk text file into info variable
with open("Information1.txt", "r", encoding = "utf-8") as file:
    info = file.read()
    
#loads scrollable text onto page
text = tk.Text(tab3, wrap = "word", width = 300, height = 1000, padx = 15, pady = 10, bg = tab3bg)
text.insert(tk.END, info)
text.configure(font = Font10, state = "disabled")
text.pack()

#4th tab 3333333333333333333333333333333333333333333333333333333333333333333333333
#444444444444444444444444444444444444444444444444444444444444444444444444444444444

#reads dehydration risk text file into info variable
with open("Information2.txt", "r", encoding = "utf-8") as file:
    info2 = file.read()

#loads scrollable text onto page
text = tk.Text(tab4, wrap = "word", width = 300, height = 1000, padx = 15, pady = 10, bg = tab4bg)
text.insert(tk.END, info2)
text.configure(font = Font10, state = "disabled")
text.pack()

#444444444444444444444444444444444444444444444444444444444444444444444444444444444
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

tk.mainloop()

#weather data from openweathermap
#heat index equation from NWS (Nation Weather Service)
#daily water intake equation from University of Missouri System
#heat stroke info from mayoclinic
#dehydration info from mayoclinic
#heat map from Nation Weather Service

