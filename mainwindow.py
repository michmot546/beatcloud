import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image
from pygame import mixer
from glob import glob
from mutagen.mp3 import MP3
from datetime import timedelta
import math

songs = glob("music\*.mp3")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self._set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        self.running : bool = True
        self.song_loaded : bool = False
        self.current_song_length : int = 1
        self.last_song_position : int = 0
        self.position_diff : int = 0

        self.title("BeatCloud v1.0")
        self.iconphoto(False, PhotoImage(file="images\logo_BC.png"))
        self.iconwindow()

        self.song_name : str = ""

        self.minsize(640, 480)
        self.maxsize(1920, 1080)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #--content_frame
        self.menu_frame : ctk.CTkFrame = ctk.CTkFrame(master=self, width=self._current_width)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frame.configure(fg_color="black")
        #--end

        #--music_manip_frame
        self.control_frame : ctk.CTkFrame = ctk.CTkFrame(master=self, width=self._current_width)
        self.control_frame.grid(row=1, column=0, sticky="ew")

        self.control_frame.grid_rowconfigure(0, weight=1)
        self.control_frame.grid_columnconfigure((0,1,2,3,4), weight=1)
        #--end

        #--music info
        self.music_info : ctk.CTkLabel = ctk.CTkLabel(master=self.control_frame, text=self.song_name)
        self.music_info.grid(row=0, column=0, columnspan=3)
        #--end

        #--volume slider
        self.music_volume_slider : ctk.CTkSlider = ctk.CTkSlider(master=self.control_frame, width= 20, command=self.volume_slider_callback)
        self.music_volume_slider.set(0.5)
        self.music_volume_slider.grid(row=0, column=4, columnspan=1, sticky="ew")
        #--end

        #--slider
        self.music_slider : ctk.CTkSlider = ctk.CTkSlider(master=self.control_frame, width=self._current_width - 20, 
                                                        progress_color="#45FF86", command=self.progress_slider_callback)
        self.music_slider.set(0)
        self.music_slider.grid(row=2, column=0, columnspan=5, sticky="ew")
        #--end

        #--play_pause
        self.play_pause_state : str = "PAUSE"
        self.play_image = ctk.CTkImage(light_image=Image.open("images\\play.png"),
                                dark_image=Image.open("images\\play.png"),
                                size=(30, 30))
        self.pause_image = ctk.CTkImage(light_image=Image.open("images\\pause.png"),
                                dark_image=Image.open("images\\pause.png"),
                                size=(30, 30))
        self.play_pause_button : ctk.CTkButton = ctk.CTkButton(master=self.control_frame, 
                                    width=30, height=30, image=self.play_image, text="", 
                                    command=self.play_pause_song, fg_color="transparent")
        self.play_pause_button.grid(row=1, column=2, columnspan=1, sticky="ew")
        #--end

        #--next_song
        self.next_image = ctk.CTkImage(light_image=Image.open("images\\next.png"),
                                  dark_image=Image.open("images\\next.png"),
                                  size=(20, 20))

        self.next_button : ctk.CTkButton = ctk.CTkButton(master=self.control_frame, 
                                    width=25, height=25, image=self.next_image, text="",
                                    fg_color="transparent", command=self.next_song)
        self.next_button.grid(row=1, column=3, columnspan=1, sticky="ew")
        #--end

        #--previous_song
        self.previous_image = ctk.CTkImage(light_image=Image.open("images\\previous.png"),
                                  dark_image=Image.open("images\\previous.png"),
                                  size=(20, 20))
        self.previous_button : ctk.CTkButton = ctk.CTkButton(master=self.control_frame, 
                                    width=25, height=25, image=self.previous_image, text="",
                                    fg_color="transparent", command=self.prev_song)
        self.previous_button.grid(row=1, column=1, columnspan=1, sticky="ew")
        #--end

        #--left_time_label
        self.music_start_label : ctk.CTkLabel = ctk.CTkLabel(master=self.control_frame, text="00:00")
        self.music_start_label.grid(row=3, column=0, columnspan=1, sticky="ew")
        #--end

        #--right_time_label
        self.music_end_label : ctk.CTkLabel = ctk.CTkLabel(master=self.control_frame, text="00:00")
        self.music_end_label.grid(row=3, column=4, columnspan=1, sticky="ew")
        #--end

        self.i = -1
        
    def load_music(self, file : str):
            mixer.init()
            mixer.music.load(file)

            self.song_name = MP3(file).filename
            self.music_info.configure(text=self.song_name)

            song_length : int = math.floor(MP3(file).info.length)
            self.current_song_length = song_length

            formated_time : list[str] = get_formated_time(self.current_song_length)
            self.music_end_label.configure(text=(f"{formated_time[1]}:{formated_time[2]}"))

            self.song_loaded = True
            self.play_pause_button.configure(image=self.pause_image)
            self.play_pause_state = "PLAY"

            self.song_restart()
            
    def next_song(self):
        if self.i < len(songs) - 1:
            self.i+=1
            self.load_music(songs[self.i])
            
    def prev_song(self):
        if self.music_slider.get() < 0.05:
            if self.i > 0:
                self.i-=1
                self.load_music(songs[self.i])
            else:
                self.song_restart()
        else:
            self.song_restart()

    def song_restart(self):
        mixer.music.play(start=0)
        self.last_song_position = 0
        
    def play_pause_song(self):     
        if not self.song_loaded:
            return
        if self.play_pause_state == "PAUSE":
            self.play_pause_button.configure(image=self.pause_image)
            self.play_pause_state = "PLAY"

            self.last_song_position += self.position_diff
            mixer.music.play(start=self.last_song_position)                
        else:
            self.play_pause_button.configure(image=self.play_image)
            self.play_pause_state = "PAUSE"             

            slider_new_value : int = math.floor(self.music_slider.get() * self.current_song_length + 1)        
            self.position_diff = slider_new_value - self.last_song_position

            mixer.music.pause()

    def close(self):
        self.running = False    

    def update(self):
        super().update()
        
        if mixer.get_init():
            print(mixer.find_channel())
        
        if self.play_pause_state == "PLAY":
            seconds : float = self.music_slider.get() * self.current_song_length
            formated_time : list[str] = get_formated_time(math.floor(seconds))
            self.music_start_label.configure(text=f"{formated_time[1]}:{formated_time[2]}")
            self.music_slider.set((self.last_song_position + mixer.music.get_pos() / 1000) / self.current_song_length)

        if self.music_slider.get() == 1:
            self.next_song()

    def progress_slider_callback(self, value : float):  
        if not self.song_loaded:
            self.music_slider.set(0)
            return
        self.play_pause_button.configure(image=self.play_image)
        self.play_pause_state = "PAUSE"
        mixer.music.pause()

        slider_new_value : int = math.floor(value * self.current_song_length)        
        self.position_diff = slider_new_value - self.last_song_position

        seconds : float = self.music_slider.get() * self.current_song_length
        formated_time : list[str] = get_formated_time(math.floor(seconds))
        self.music_start_label.configure(text=f"{formated_time[1]}:{formated_time[2]}")

    def volume_slider_callback(self, value : float):
        if not self.song_loaded:
            self.music_volume_slider.set(0.5)
            return
        mixer.music.set_volume(value)

        
def get_formated_time(seconds : int) -> list[str]:
    td_str = str(timedelta(seconds=seconds))
    return td_str.split(':')
    
        
if __name__ == "__main__":
    app = App()
    while app.running:
        app.protocol("WM_DELETE_WINDOW", app.close)
        app.update()