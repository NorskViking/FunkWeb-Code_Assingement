import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Weather Forecast v0.0.1")
        self._set_appearance_mode("System")
        #self.set_default_color_theme("blue")
        self.geometry("480x380")
        self.resizable(True, True)
        
        
        self.button = customtkinter.CTkButton(self, text="Test", command=self.button_callback)
        self.button.pack(padx=20, pady=20)
        
    def button_callback(self):
        print("button tested")
        
app = App()
app.mainloop()
        