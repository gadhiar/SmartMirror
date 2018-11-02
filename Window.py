from __future__ import print_function
import json
import traceback
import time
from tkinter import *
import requests
from PIL import ImageTk, Image
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import dateutil.parser
from bin.hand_recognition import start

"""
Flag for enabling gesture control: Defaulted to off.
Set to true if you have a camera setup and desire to use your hands to swap screens
Set to false otherwise
"""

gesture_control = False

label_array = []
temp_events = []
temp_forecast = []
exclude_list = ['minutely', 'hourly', 'alerts', 'flags']
ui_locale = ''  # e.g. 'fr_FR' fro French, '' as default
time_format = 12  # 12 or 24
date_format = "%b %d, %Y"  # check python doc for strftime() for options
news_country_code = 'us'
weather_lang = 'en'
weather_unit = 'us'
weather_api = 'cf0cb14f4481ad41737f14670b73b52c'

location_api = '485e82dcc7de155ab466e75943dc3a11'
latitude = None  # Set this if IP location lookup does not work for you (must be a string)
longitude = None

font = 'Helvetica'
deg_sign = "\xb0"
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18

#instantiate main root for all windows to use
main_root = None

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
<<<<<<< HEAD
icon_lookup = {
    'clear-day': "Images/Sun.png",  # clear sky day
    'wind': "Images/Wind.png",  # wind
    'cloudy': "Images/Cloud.png",  # cloudy day
    'partly-cloudy-day': "Images/PartlySunny.png",  # partly cloudy day
    'rain': "Images/Rain.png",  # rain day
    'snow': "Images/Snow.png",  # snow day
    'snow-thin': "Images/Snow.png",  # sleet day
    'fog': "Images/Haze.png",  # fog day
    'clear-night': "Images/Moon.png",  # clear sky night
    'partly-cloudy-night': "Images/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "Images/Storm.png",  # thunderstorm
    'tornado': "Images/Tornado.png",  # tornado
    'hail': "Images/Hail.png"  # hail
||||||| merged common ancestors
icon_lookup = {
    'clear-day': "Images/Sun.png",  # clear sky day
    'wind': "Images/Wind.png",  # wind
    'cloudy': "Images/Cloud.png",  # cloudy day
    'partly-cloudy-day': "Images/PartlySunny.png",  # partly cloudy day
    'rain': "Images/Rain.png",  # rain day
    'snow': "Images/Snow.png",  # snow day
    'snow-thin': "Images/Snow.png",  # sleet day
    'fog': "Images/Haze.png",  # fog day
    'clear-night': "Images/Moon.png",  # clear sky night
    'partly-cloudy-night': "Images/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "Images/Storm.png",  # thunderstorm
    'tornado': "Images/Tornado.png",  # tornado
    'hail': "Images/Hail.png"  # hail
=======
icon_lookup = {
    'clear-day': "Images/Sun.png",  # clear sky day
    'wind': "Images/Wind.png",  # wind
    'cloudy': "Images/Cloud.png",  # cloudy day
    'partly-cloudy-day': "Images/PartlySunny.png",  # partly cloudy day
    'rain': "Images/Rain.png",  # rain day
    'snow': "Images/Snow.png",  # snow day
    'snow-thin': "Images/Snow.png",  # sleet day
    'fog': "Images/Haze.png",  # fog day
    'clear-night': "Images/Moon.png",  # clear sky night
    'partly-cloudy-night': "Images/artlyMoon.png",  # scattered clouds night
    'thunderstorm': "Images/Storm.png",  # thunderstorm
    'tornado': "Images/Tornado.png",  # tornado
    'hail': "Images/Hail.png"  # hail
>>>>>>> 95bff1e214b54df901c50516ae9a121532daf1f7
}


def make_image(x, y, img):
    im = Image.open(img)
    im = im.resize((x, y), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(im)
    return ph


class Window:
    def __init__(self):
        global main_root
        # create the root window and apply all configs to it along with frames
        self.root = Tk()
        main_root = self.root
        self.root.title("Kevin is the ugliest man on the planet")
        self.root.overrideredirect = TRUE
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.end_fullscreen)
        self.root.configure(background='black')

        self.rightFrame = Frame(self.root, background='black')
        self.leftFrame = Frame(self.root, background='black')
        self.rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES)

        # Create objects
        self.weather = Weather(self.rightFrame)
        self.weather.pack(side=TOP, anchor=E)
        self.forecast = Forecast(self.rightFrame)
        self.forecast.pack(side=TOP, anchor=E, pady=30)
        self.date = Date(self.leftFrame)
        self.date.pack(side=TOP, anchor=W)
        self.calendar = Calendar(self.leftFrame)
        self.calendar.pack(side=TOP, anchor=W)

    def end_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        return "break"


class rightScreen:
    def __init__(self, screen_root):
        # create the root window and apply all configs to it along with frames
        self.top = Toplevel(screen_root)
        self.top.withdraw()
        self.top.title("Kevin is the ugliest man on the planet")
        self.top.overrideredirect = TRUE
        self.top.attributes('-fullscreen', True)
        self.top.bind("<Escape>", self.end_fullscreen)
        self.top.configure(background='black')

        self.rightFrame = Frame(self.top, background='black')
        self.leftFrame = Frame(self.top, background='black')
        self.rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES)

        right = Label(self.rightFrame, text='RIGHTSCREEN', fg="white", bg="black", font=('Helvetica', 20), padx=30)
        right.pack()

    def end_fullscreen(self, event=None):
        self.top.attributes("-fullscreen", False)
        return "break"


class leftScreen:
    def __init__(self, screen_root):
        # create the root window and apply all configs to it along with frames
        self.top = Toplevel(screen_root)
        self.top.withdraw()
        self.top.title("Left Screen")
        self.top.overrideredirect = TRUE
        self.top.attributes('-fullscreen', True)
        self.top.bind("<Escape>", self.end_fullscreen)
        self.top.configure(background='black')

        self.rightFrame = Frame(self.top, background='black')
        self.leftFrame = Frame(self.top, background='black')
        self.rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES)

        right = Label(self.rightFrame, text='LEFTSCREEN', fg="white", bg="black", font=('Helvetica', 70), padx=30)
        right.pack()

    def end_fullscreen(self, event=None):
        self.top.attributes("-fullscreen", False)
        return "break"

class topScreen:
    def __init__(self, screen_root):
        # create the root window and apply all configs to it along with frames
        self.top = Toplevel(screen_root)
        self.top.withdraw()
        self.top.title("Top Screen")
        self.top.overrideredirect = TRUE
        self.top.attributes('-fullscreen', True)
        self.top.bind("<Escape>", self.end_fullscreen)
        self.top.configure(background='black')

        self.rightFrame = Frame(self.top, background='black')
        self.leftFrame = Frame(self.top, background='black')
        self.rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES)

        right = Label(self.rightFrame, text='TOPSCREEN', fg="white", bg="black", font=('Helvetica', 70), padx=30)
        right.pack()

    def end_fullscreen(self, event=None):
        self.top.attributes("-fullscreen", False)
        return "break"

class botScreen:
    def __init__(self, screen_root):
        # create the root window and apply all configs to it along with frames
        self.top = Toplevel(screen_root)
        self.top.withdraw()
        self.top.title("Bot Screen")
        self.top.overrideredirect = TRUE
        self.top.attributes('-fullscreen', True)
        self.top.bind("<Escape>", self.end_fullscreen)
        self.top.configure(background='black')

        self.rightFrame = Frame(self.top, background='black')
        self.leftFrame = Frame(self.top, background='black')
        self.rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES)
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES)

        right = Label(self.rightFrame, text='BOTSCREEN', fg="white", bg="black", font=('Helvetica', 70), padx=30)
        right.pack()

    def end_fullscreen(self, event=None):
        self.top.attributes("-fullscreen", False)
        return "break"


class Forecast(Frame):
    icon = None
    picture1 = None
    label_array = None

    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')

        # create all the labels and insert them into the array
        day1 = Label(self, fg="white", bg="black", font=(font, 20), padx=30)
        day1.pack(side=TOP, anchor=E)
        day2 = Label(self, fg="white", bg="black", font=(font, 20), padx=30)
        day2.pack(side=TOP, anchor=E)
        day3 = Label(self, fg="white", bg="black", font=(font, 20), padx=30)
        day3.pack(side=TOP, anchor=E)
        day4 = Label(self, fg="white", bg="black", font=(font, 20), padx=30)
        day4.pack(side=TOP, anchor=E)
        day5 = Label(self, fg="white", bg="black", font=(font, 20), padx=30)
        day5.pack(side=TOP, anchor=E)
        day6 = Label(self, fg="white", bg="black", font=(font, 20), padx=30)
        day6.pack(side=TOP, anchor=E)
        day7 = Label(self, fg="white", bg="black", font=(font, 20), padx=30)
        day7.pack(side=TOP, anchor=E)

        self.label_array = [day1, day2, day3, day4, day5, day6, day7]

        self.getForecast()

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def getForecast(self):
        try:
            if latitude is None and longitude is None:
                # retrieve location based off of ip lookup
                location_req = "http://api.ipstack.com/%s?access_key=%s&output=json&legacy=1" % (self.get_ip(), location_api)
                req = requests.get(location_req)
                location_json = json.loads(req.text)
                lat = location_json['latitude']
                lon = location_json['longitude']
                # get the weather
                weather_req = "https://api.darksky.net/forecast/%s/%s,%s?exclude=%s&units=%s" % (
                    weather_api, lat, lon, exclude_list, weather_unit)
            else:
                # retrieve location using preset Lat/Long
                location2 = ''
                weather_req = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                    weather_api, latitude, longitude, weather_lang, weather_unit)

            req = requests.get(weather_req)
            forecast_json = json.loads(req.text)
            temp_forecast.clear()

            # scroll through the array, starting at next day, of daily events and retrieve icon and high/low for each
            #  day
            x = 1
            while x < 8:
                icon1 = forecast_json['daily']['data'][x].get('icon')
                tempMax = str(int(forecast_json['daily']['data'][x].get('temperatureHigh'))) + deg_sign
                tempLow = str(int(forecast_json['daily']['data'][x].get('temperatureLow'))) + deg_sign
                temp_info = [icon1, tempMax, tempLow]
                temp_forecast.append(temp_info)
                x += 1

            # iterate through label and forecast arrays, setting the proper ones
            y = 0
            while y < 7:
                picture = None
                self.icon = temp_forecast[y][0]
                maxTemp = temp_forecast[y][1]
                minTemp = temp_forecast[y][2]
                text1 = maxTemp + " / " + minTemp

                if self.icon in icon_lookup:
                    picture = icon_lookup[self.icon]

                if picture is not None:
                    if self.icon != picture:
                        self.picture1 = make_image(40, 40, picture)
                        self.label_array[y].config(image=self.picture1, compound=LEFT, text=text1)
                        self.label_array[y].image = self.picture1  # keep a reference to the image!
                y += 1

        except Exception as e:
            traceback.print_exc()
            print("Error: %s. Cannot get weather." % e)

        self.after(1800000, self.getForecast)


class Calendar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')

        self.calendarEvents = []
        self.setEvents(True)

    def setEvents(self, override=False):
        if self.calendarEvents != self.getEvents() or override:
            self.calendarEvents = [x for x in self.getEvents()]
            tempDayString = self.calendarEvents[0][0] if len(self.calendarEvents) > 0 else ""
            intPoint = 0
            dayLabel = 0
            for x in range(len(self.calendarEvents) + 1):
                if x != intPoint and (x == len(self.calendarEvents) or self.calendarEvents[x][0] != tempDayString):
                    if dayLabel < len(self.winfo_children()):
                        self.winfo_children()[dayLabel].updateDate(self.calendarEvents[intPoint:x])
                    else:
                        CalendarDate(self, self.calendarEvents[intPoint:x]).pack(side=TOP, anchor=W)
                    dayLabel += 1
                    intPoint = x
                    tempDayString = self.calendarEvents[x][0] if x != len(self.calendarEvents) else ""
            for widget in self.winfo_children()[dayLabel:]:
                widget.animate(widget.winfo_children(), 200, 10, True)  # relevant to animation
        self.after(2000, self.setEvents)

    def getEvents(self):

        # Setup the Calendar API
        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=5, singleEvents=True,
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        # return events

        temp_events.clear()
        for event in events:
            startTime1 = event['start'].get('dateTime')  # print start time
            endTime1 = event['end'].get('dateTime')  # print end time
            date1 = event['start'].get('dateTime')
            name = event['summary']

            # parse the start and end times into friendly elements and store them
            sT = dateutil.parser.parse(startTime1)
            eT = dateutil.parser.parse(endTime1)
            dT = dateutil.parser.parse(date1)
            startTime = sT.strftime('%I:%M %p')
            endTime = eT.strftime('%I:%M %p')
            dateTime = dT.strftime('%A, %B %d')

            # give each object it's own array of info values
            temp_array = [dateTime, name, startTime, endTime]
            temp_events.append(temp_array)
        return temp_events


class CalendarDate(Frame):
    def __init__(self, parent, events):
        Frame.__init__(self, parent, bg='black')

        Label(self, text=events[0][0], font=("Helvetica", 23), fg='black', bg="black",
              justify=LEFT).pack(side=TOP, anchor=W, padx=45, pady=(50, 0))

        for event in events:
            Label(self, text=event[1], font=("Helvetica", 19), fg='black', bg="black",
                  justify=LEFT).pack(side=TOP, anchor=W, padx=65, pady=(10, 0))

            Label(self, text=event[2] + " - " + event[3], font=("Helvetica", 15), fg='black',
                  bg="black", justify=LEFT).pack(side=TOP, anchor=W, padx=65)

        self.animate(self.winfo_children(), 200, 3)

    def updateDate(self, events):

        animateList = []

        dateLabel = self.winfo_children()[0]
        if dateLabel.cget("text") != events[0][0]:
            dateLabel.config(text=events[0][0], fg='white')
            animateList.append(dateLabel)

        eventLabel = 1
        for event in events:
            if eventLabel < len(self.winfo_children()) - 1:
                eventLbl = self.winfo_children()[eventLabel]
                timeLbl = self.winfo_children()[eventLabel + 1]
                if eventLbl.cget("text") != event[1]:
                    eventLbl.config(text=event[1], fg='white')
                    animateList.append(eventLbl)
                if timeLbl.cget("text") != event[2] + " - " + event[3]:
                    timeLbl.config(text=event[2] + " - " + event[3], fg='white')
                    animateList.append(timeLbl)
            else:
                Label(self, text=event[1], font=("Helvetica", 19), fg='black', bg="black",
                      justify=LEFT).pack(side=TOP, anchor=W, padx=65, pady=(10, 0))
                Label(self, text=event[2] + " - " + event[3], font=("Helvetica", 15), fg='black',
                      bg="black", justify=LEFT).pack(side=TOP, anchor=W, padx=65)
                animateList += self.winfo_children()[-2:]
            eventLabel += 2

        self.animate(self.winfo_children()[eventLabel:], 200, 10, True)
        self.animate(animateList, 200, 3)

    def animate(self, labelList, step, exp, reverse=False, currentStep=0, kill=False):
        ratio = ((98.0 if reverse else -98.0) / pow(step, exp))
        if currentStep != step:
            fgColor = round(ratio * pow(abs(currentStep - step), exp) + (1 if reverse else 99))
            for label in labelList:
                label.config(fg='gray' + str(fgColor))
            if fgColor == (1 if reverse else 99):
                if kill:
                    self.destroy()
                if reverse:
                    for widget in labelList:
                        widget.destroy()
                return
            self.after(20, self.animate, labelList, step, exp, reverse, currentStep + 1)


class Date(Frame):  # IMPLEMENT SMALL SECONDS
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        # set labels/frames for left side
        self.time = ""
        self.day = ""
        self.month = ""
        self.number = ""
        self.date = self.day + ", " + self.month + "" + self.number
        self.dateFrm = Frame(self, bg="black")
        self.dateFrm.pack(side=TOP, anchor=W)  # i changed this from RIGHt # to TOP
        self.clockFrm = Frame(self, bg="black")
        self.clockFrm.pack(side=TOP, anchor=W)
        self.date_label = Label(self.dateFrm, font=(font, 28), fg="white", bg="black",
                                justify=LEFT)
        self.date_label.pack(side=TOP, anchor=W, padx=30, pady=(30, 0))
        self.clock_label = Label(self.clockFrm, font=(font, 64), fg="white", bg="black",
                                 justify=LEFT, padx=20)
        self.clock_label.pack(side=TOP, anchor=N)
        self.get_date()
        self.get_time()

    def get_date(self):
        day2 = datetime.date.today().strftime("%A")
        month2 = datetime.date.today().strftime("%B")
        number2 = str(datetime.date.today().strftime("%d"))
        date2 = day2 + ", " + month2 + " " + number2

        if self.date != date2:
            self.date = date2
            self.date_label.config(text=date2)

        self.after(600000, self.get_date)

    def get_time(self):
        time1 = time.strftime('%I:%M %p')  # hour in 12h format
        if time1 != self.time:
            self.time = time1
            self.clock_label.config(text=time1)
        self.after(200, self.get_time)


class Weather(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.currently = ''
        self.icon = ''

        # set labels/frames for the right side
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=E)
        self.weatherFrm = Frame(self, bg="black")
        self.weatherFrm.pack(side=TOP, anchor=E)
        self.weatherFrm.grid_propagate(FALSE)
        self.temperature_label = Label(self.degreeFrm, font=(font, xlarge_text_size), fg="white", bg="black")
        self.temperature_label.pack(side=RIGHT, anchor=N, padx=30, pady=(30, 0))
        self.weather_icon = Label(self.degreeFrm, fg="white", bg="black")
        self.weather_icon.pack(side=RIGHT, anchor=N, pady=(30, 0))
        self.current_weather = Label(self.weatherFrm, font=(font, 22), fg="white", bg="black",
                                     padx=30, justify=RIGHT)
        self.current_weather.pack(side=TOP, anchor=E)
        self.current_weather.config(wraplength=350)
        self.get_weather()

    def get_ip(self):
        try:
            ip_url = "http://jsonip.com/"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_weather(self):
        try:
            if latitude is None and longitude is None:
                # retrieve location based off of ip lookup
                location_req = "http://api.ipstack.com/%s?access_key=%s&output=json&legacy=1" % (self.get_ip(), location_api)
                req = requests.get(location_req)
                location_json = json.loads(req.text)
                lat = location_json['latitude']
                lon = location_json['longitude']
                self.location = "%s, %s" % (location_json['city'], location_json['region_code'])

                # get the weather
                weather_req = "https://api.darksky.net/forecast/%s/%s,%s?exclude=%s&units=%s" % (
                    weather_api, lat, lon, exclude_list, weather_unit)
            else:
                # retrieve location using preset Lat/Long
                location2 = ''
                weather_req = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (
                    weather_api, latitude, longitude, weather_lang, weather_unit)

            req = requests.get(weather_req)
            weather_json = json.loads(req.text)
            # set all the weather values and the weather summary
            temperature2 = "%s%s" % (str(int(weather_json['currently']['temperature'])), deg_sign)
            currently2 = "Today: \n" + weather_json['daily']['data'][0].get('summary') + "\n\n" + " Tomorrow: \n" + \
                         weather_json['daily']['data'][1].get('summary')
            icon_id = weather_json['currently']['icon']
            picture = None

            if icon_id in icon_lookup:
                picture = icon_lookup[icon_id]

            if picture is not None:
                if self.icon != picture:
                    self.icon = picture
                    image1 = make_image(100, 100, picture)
                    self.weather_icon.config(image=image1)
                    self.weather_icon.image = image1
                else:
                    # remove the image
                    self.weather_icon.config(image='')

            # set temperature levels, current weather forecast, and future forecast
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperature_label.config(text=temperature2)
            if self.currently != currently2:
                self.currently = currently2
                self.current_weather.config(text=currently2)

        except Exception as e:
            traceback.print_exc()
            print("Error: %s. Cannot get weather." % e)

        self.after(600000, self.get_weather)


def init():
    global main_root
    window = Window()
    right_screen = rightScreen(main_root)
    left_screen = leftScreen(main_root)
    top_screen = topScreen(main_root)
    bot_screen = botScreen(main_root)
    if gesture_control:
        start(window, right_screen, left_screen, top_screen, bot_screen)
    window.root.mainloop()


init()
