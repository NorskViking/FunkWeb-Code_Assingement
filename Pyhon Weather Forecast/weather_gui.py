import customtkinter
from Weather_Forecast import Place, Forecast
import datetime as dt
import json

USER_AGENT = "Weather_ForeCast jorgen@funkweb.org"

nor_cities = open("./data/nor.json")
# Convert JSON object to dict
nor_data = json.load(nor_cities)
# Close JSON file
nor_cities.close()
norwegian_citys = []
for city in nor_data:
    norwegian_citys.append(Place(city["city"], float(city["lat"]), float(city["lon"])))
    
oslo_city = None
city_names = []
for town in norwegian_citys:
    city_names.append(town.name)
    if town.name == "Oslo":
        oslo_city = town

#print(oslo_city)
forecast = Forecast(oslo_city, USER_AGENT)
forecast.update()

def get_forecast(choice):
            for city in norwegian_citys:
                if city.name == choice:
                    new_forecast = Forecast(city, USER_AGENT)
                    new_forecast.update()
                    forecast = new_forecast

class ScrollFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.forecast = forecast
        
        self._label = customtkinter.CTkLabel(self, text=self.forecast.place.name, font=('Arial bold', 25))
        self._label.grid(row=0, column=0, padx=20)
        
        #self.hour_label = customtkinter.CTkLabel(self, text=)
        
class CheckBoxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.temperatur = customtkinter.CTkCheckBox(self, text="Temperatur")
        self.temperatur.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.regn = customtkinter.CTkCheckBox(self, text="Regn")
        self.regn.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.vind = customtkinter.CTkCheckBox(self, text="Vind")
        self.vind.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Weather Forecast v0.0.1")
        self._set_appearance_mode("System")
        #self.set_default_color_theme("blue")
        #self.geometry("480x380")
        self.resizable(True, True)
        
        """
        self.forecast = Forecast(oslo_city, USER_AGENT)
        
        def get_forecast(choice):
            for city in norwegian_citys:
                if city.name == choice:
                    self.forecast = Forecast(city, USER_AGENT)
                    self.forecast.update()
            print(choice)
        """
        self.city_chooser = customtkinter.CTkComboBox(self, values=city_names, command=get_forecast)
        self.city_chooser.grid(row=0, column=1, padx=20, pady=20)
        
        self.scroll_frame = ScrollFrame(master=self, width=300, height=200)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=20)
        
        self.checkbox_frame = CheckBoxFrame(self)
        self.checkbox_frame.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        #self.button = customtkinter.CTkButton(self, text="Test", command=self.button_callback)
        #self.button.pack(padx=20, pady=20)
        
        
app = App()
app.mainloop()
        