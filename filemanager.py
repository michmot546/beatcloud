import glob as g
import pygame as py
from mutagen.mp3 import MP3


files = g.glob("music\*.mp3")



py.mixer.music.load(files[0])
py.mixer.music.play()
audio = MP3(files[0])


while True:
    print(py.mixer.music.get_pos())
    