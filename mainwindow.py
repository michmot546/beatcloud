import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")
        self.title("BeatCloud v1.0")
        self.iconphoto(False, PhotoImage(file="images\logo_BC.png"))
        self.iconwindow()
        self.minsize(640, 480)
        self.maxsize(640, 480)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=3)

        # self.playlists_option_menu : ctk.CTkOptionMenu = ctk.CTkOptionMenu(master=self)
        # self.playlists_option_menu.grid(row=0, column=0, padx=20, pady=(20, 0))

        self.control_frame : ctk.CTkFrame = ctk.CTkFrame(master=self, width=self._current_width, height=120,)
        self.control_frame.grid(row=1, column=0, columnspan=3)

        self.music_slider : ctk.CTkSlider = ctk.CTkSlider(master=self.control_frame, width=self._current_width - 20, 
                                                        progress_color="#45FF86")
        self.music_slider.set(0)
        self.music_slider.place(relx=0.5, rely=0.65, anchor=ctk.S)

        self.play_pause_state : str = "PAUSE"
        self.play_image = ctk.CTkImage(light_image=Image.open("images\\play.png"),
                                dark_image=Image.open("images\\play.png"),
                                size=(30, 30))
        self.pause_image = ctk.CTkImage(light_image=Image.open("images\\pause.png"),
                                dark_image=Image.open("images\\pause.png"),
                                size=(30, 30))
        self.play_pause_button : ctk.CTkButton = ctk.CTkButton(master=self.control_frame, 
                                    width=30, height=30, image=self.play_image, text="", 
                                    command=self.play_pause_clicked, fg_color="transparent")
        self.play_pause_button.place(relx=0.5, rely=0.5, anchor=ctk.S)

        self.next_image = ctk.CTkImage(light_image=Image.open("images\\next.png"),
                                  dark_image=Image.open("images\\next.png"),
                                  size=(20, 20))
        self.next_button : ctk.CTkButton = ctk.CTkButton(master=self.control_frame, 
                                    width=25, height=25, image=self.next_image, text="",
                                    fg_color="transparent")
        self.next_button.place(relx=0.6, rely=0.5, anchor=ctk.S)
    
        self.previous_image = ctk.CTkImage(light_image=Image.open("images\\previous.png"),
                                  dark_image=Image.open("images\\previous.png"),
                                  size=(20, 20))
        self.previous_button : ctk.CTkButton = ctk.CTkButton(master=self.control_frame, 
                                    width=25, height=25, image=self.previous_image, text="",
                                    fg_color="transparent")
        self.previous_button.place(relx=0.4, rely=0.5, anchor=ctk.S)

        self.music_start_label : ctk.CTkLabel = ctk.CTkLabel(master=self.control_frame, text="0:00")
        self.music_start_label.place(relx=0.05, rely=0.92, anchor=ctk.S)

        self.music_end_label : ctk.CTkLabel = ctk.CTkLabel(master=self.control_frame, text="0:00")
        self.music_end_label.place(relx=0.95, rely=0.92, anchor=ctk.S)
        

    def play_pause_clicked(self):
        if self.play_pause_state == "PAUSE":
            self.play_pause_button.configure(image=self.pause_image)
            self.play_pause_state = "PLAY"
        else:
            self.play_pause_button.configure(image=self.play_image)
            self.play_pause_state = "PAUSE"
        
if __name__ == "__main__":
    app = App()
    app.mainloop()