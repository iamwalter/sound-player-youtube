from tkinter import *

import _thread
import os
import pygame
import time
import urllib.request

song_volume = song_timer_min = song_timer_sec = song_path = song_paused = song_controls = 0

# Draw on screen
def draw():
    song_display_volume_slider = list(50*' ')
    volume = int(song_volume * 100)

    os.system('cls')

    # Title
    print("{} | ".format(song_path), end='')

    # Timer - Count up
    if song_timer_sec < 10:
        print("{}:0{} | ".format(song_timer_min, song_timer_sec), end='')
    else:
        print("{}:{} | ".format(song_timer_min, song_timer_sec), end='')

    # Volume
    print("{}%".format(volume))

    x_index = int((volume * 50) / 100)

    if x_index == 50:
        x_index = 49

    song_display_volume_slider[x_index] = 'X'
    print("0% | ", end='')
    for x in song_display_volume_slider:
        print(x, end='')
    print(" | 100%")
    # Song Controls

    print("{}".format(song_controls))
# Timer
def timer():
    global song_timer_sec
    global song_timer_min

    while True:
        if not song_paused:
            song_timer_sec += 1
            if (song_timer_sec >= 60):
                song_timer_sec = 0
                song_timer_min += 1

        # Draw every time a second is over
        draw()
        time.sleep(1)
# Play the song from song_path and start timer thread w/ timer function
def play():
    pygame.mixer.init(44100, 16, 2, 4096)
    pygame.init()

    try :
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(song_volume)
    except:
        print("Could not open file {}, try another file path.".format(song_path))

    try:
        _thread.start_new_thread(timer, ())
    except:
        print("Could not start timer thread.")
# Update the song volume and title
def update_song(vol, title):
    pygame.mixer.music.set_volume(vol)
    pygame.display.set_caption(title)
# Download a song from url, and store it in song_path.
def download_song(song_url):
    global song_path

    while True:
        try:
            song_path, headers = urllib.request.urlretrieve(song_url)
            print("Downloading {}...".format(song_url))
            print("Saved temp mp3 file to " + song_path)
            break
        except:
            print("Could not get the file specified at clipboard: {}, please "
                  "restart the program with a valid link in clipboard.".format(song_url))
            time.sleep(7)

            exit_prog()
# Get from clipboard
def get_clipboard():
    # Get data from clipboard
    root = Tk()
    # Stop window from showing
    root.withdraw()
    # Return clipboard
    return root.clipboard_get()
# Pause/unpause song
def pause_unpause():
    global song_paused

    if song_paused:
        pygame.mixer.music.unpause()
        song_paused = False
    else:
        pygame.mixer.music.pause()
        song_paused = True
# Cleanup and exit
def exit_prog():
    pygame.mixer.quit()
    pygame.quit()

    try:
     os.remove(song_path)
    except FileNotFoundError:
        pass

    exit(0)
# Init all song_* vars, also pygame
def init():
    global song_controls, song_volume, song_timer_min, song_timer_sec, song_path, song_paused

    song_controls = """
T   - Volume +
R   - Volume -
P   - (un)pause
Esc - Exit
"""

    song_volume = 1
    song_timer_min = 0
    song_timer_sec = 0
    song_path = 'Sound Player - No Audio File'
    song_paused = False

    pygame.init()
    pygame.display.set_mode((500, 50))
    pygame.display.set_caption(song_path)
# Get events and draw if there is an event
def update():
    global song_volume, song_path

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_prog()

        if event.type == pygame.KEYDOWN:
            # Volume
            if event.key == pygame.K_t:
                if not song_volume > 1: song_volume += 0.01
            if event.key == pygame.K_r:
                if not song_volume < 0: song_volume -= 0.01
            if event.key == pygame.K_ESCAPE:
                exit_prog()

            # Pausing
            if event.key == pygame.K_p:
                pause_unpause()


        #Draw & update every time an event is done
        update_song(song_volume, song_path)
        draw()

        pygame.display.update()
# Start the program
def start():
    global song_volume, song_path

    # Init pygame and global vars
    init()
    # Download the song from clipboard
    download_song(get_clipboard())
    # Start the song
    play()

    update_song(song_volume, song_path)

    # While song is playing
    while pygame.mixer.music.get_busy():
        try:
            update()
        except:
            exit_prog()

    exit_prog()

start()

