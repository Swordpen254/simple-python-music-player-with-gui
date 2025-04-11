import os
import pygame
from mutagen.mp3 import MP3
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import time
import math

playlist = []
current_track_index = 0
is_playing = False
is_paused = False
root = None

def initialize_player():
    try:
        pygame.mixer.init()
        print("Pygame mixer initialized successfully.")
    except pygame.error as e:
        print(f"Error initializing pygame mixer: {e}")

def format_time(seconds):
    if seconds is None or not isinstance(seconds, (int, float)) or seconds < 0:
        return "--:--"
    minutes = math.floor(seconds / 60)
    remaining_seconds = math.floor(seconds % 60)
    return f"{minutes:02d}:{remaining_seconds:02d}"

def get_track_duration(file_path):
    try:
        audio = MP3(file_path)
        length = audio.info.length
        return length
    except Exception as e:
        print(f"Error getting duration: {e}")
        return None

def load_folder():
    global playlist, current_track_index, is_playing, is_paused, _is_internal_update, progress_slider
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    playlist = []
    playlist_box.delete(0, tk.END)
    current_track_index = 0
    is_playing = False
    is_paused = False
    update_track_info_display(None)
    play_pause_button.configure(text="▶ Play")

    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".mp3"):
                full_path = os.path.join(folder_path, filename)
                playlist.append(full_path)
                playlist_box.insert(tk.END, filename)

        if playlist:
            playlist_box.selection_set(0)
            playlist_box.activate(0)
            load_track(playlist[current_track_index])
            print("Tracks loaded successfully")
        else:
            status_label.configure(text="No MP3 files found in selected folder.")
            _is_internal_update = True
            progress_slider.configure(state="disabled")
            progress_slider.set(0)
            _is_internal_update = False

    except Exception as e:
        print(f"Error loading folder: {e}")
        status_label.configure(text=f"Error loading folder.")
        _is_internal_update = True
        progress_slider.set(0)
        _is_internal_update = False


def load_track(file_path):
    global current_track_index, _is_internal_update, progress_slider
    try:
        pygame.mixer.music.load(file_path)
        duration_seconds = get_track_duration(file_path)
        _is_internal_update = True
        progress_slider.set(0)
        if duration_seconds is not None and duration_seconds > 0:
             progress_slider.configure(state="normal")
        else:
             progress_slider.configure(state="disabled")
        _is_internal_update = False
        update_track_info_display(file_path, duration_seconds)
        status_label.configure(text="Track loaded. Press Play.")
    except pygame.error as e:
        print(f"Error loading track {os.path.basename(file_path)}: {e}")
        status_label.configure(text=f"Error loading: {os.path.basename(file_path)}")
        update_track_info_display(None)

def play_music():
    global is_playing, is_paused, current_track_index

    if not playlist:
        status_label.configure(text="No tracks loaded. Please load a folder")
        return

    try:
        if is_paused:
            pygame.mixer.music.unpause()
            is_paused = False
            is_playing = True
            play_pause_button.configure(text="⏸ Pause")
            status_label.configure(text=f"Playing: {os.path.basename(playlist[current_track_index])}")
            current_path = playlist[current_track_index]
            current_duration = get_track_duration(current_path)
            update_track_info_display(current_path, current_duration)
            check_music_end()

        elif not is_playing:
            selected_indices = playlist_box.curselection()
            if selected_indices:
                current_track_index = selected_indices[0]
            else:
                playlist_box.selection_clear(0, tk.END)
                playlist_box.selection_set(current_track_index)
                playlist_box.activate(current_track_index)

            file_path = playlist[current_track_index]
            load_track(file_path)
            pygame.mixer.music.play()
            is_playing = True
            is_paused = False
            play_pause_button.configure(text="⏸ Pause")
            status_label.configure(text=f"Playing: {os.path.basename(file_path)}")
            check_music_end()

    except pygame.error as e:
        print(f"Error playing track: {e}")
        status_label.configure(text="Error playing track")
        is_playing =  False
        is_paused = False
        play_pause_button.configure(text="▶ Play")


def seek_music(value):
    global is_playing, is_paused, current_track_index, _is_internal_update, progress_slider

    if _is_internal_update:
        return

    if not playlist or not pygame.mixer.get_init():
        print("Seek failed: No playlist or mixer not initialized.")
        return

    try:
        file_path = playlist[current_track_index]
        duration_seconds = get_track_duration(file_path)
        if duration_seconds is None or duration_seconds <= 0:
            print("Seek failed: Invalid track duration")
            return
    except Exception as e:
        print(f"Seek failed: Error getting duration: {e}")
        return
    except:
        print("Seek failed: Invalid track index")
        return

    seek_time_seconds = (float(value)/100.0) * duration_seconds
    print(f"Seeking to: {format_time(seek_time_seconds)} ({value}%)")

    try:
        was_playing = is_playing
        was_paused = is_paused

        pygame.mixer.music.stop()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play(start=seek_time_seconds)

        is_playing = True
        is_paused = False
        play_pause_button.configure(text="⏸ Pause")

        #global _is_internal_update
        _is_internal_update = True
        update_track_info_display(file_path, duration_seconds)
        progress_slider.set(float(value))
        _is_internal_update = False

        check_music_end()

        if was_paused and not was_playing:
            pygame.mixer.music.pause()
            is_playing = False
            is_paused = True
            play_pause_button.configure(text="▶ Play")

    except pygame.error as e:
        print(f"Error seeking track: {e}")
        status_label.configure(text="Error seeking track")
        is_playing = False
        is_paused = False
        play_pause_button.configure(text="▶ Play")
        progress_slider.set(0)
        progress_slider.configure(state="disabled")


def pause_resume_music():
    global is_playing, is_paused, current_track_index

    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False
        is_paused = True
        play_pause_button.configure(text="▶ Play")
        status_label.configure(text="Playback paused")
    elif is_paused:
        pygame.mixer.music.unpause()
        is_playing = True
        is_paused = False
        play_pause_button.configure(text="⏸ Pause")
        status_label.configure(text=f"Playing: {os.path.basename(playlist[current_track_index])}")
        current_path = playlist[current_track_index]
        current_duration = get_track_duration(current_path)
        update_track_info_display(current_path, current_duration)
        check_music_end()
    elif not is_playing:
        selected_indices = playlist_box.curselection()
        if selected_indices:
            current_track_index = selected_indices[0]
        else:
            playlist_box.selection_clear(0, tk.END)
            playlist_box.selection_set(current_track_index)
            playlist_box.activate(current_track_index)

        file_path = playlist[current_track_index]
        load_track(file_path)
        pygame.mixer.music.play()
        is_playing = True
        is_paused = False
        t_duration = get_track_duration(file_path)
        play_pause_button.configure(text="⏸ Pause")
        status_label.configure(text=f"Playing: {os.path.basename(file_path)}")
        update_track_info_display(file_path, t_duration)
        check_music_end()

def stop_music():
    global is_playing, is_paused, _is_internal_update, progress_slider
    try:
        pygame.mixer.music.stop()
        is_playing = False
        is_paused = False
        play_pause_button.configure(text="▶ Play")
        status_label.configure(text="Playback Stopped")
        _is_internal_update = True

        progress_slider.set(0)
        _is_internal_update = False

        if playlist: # Check if playlist exists before accessing it
             try:
                 update_track_info_display(playlist[current_track_index])
             except IndexError: # Handle case where index might be invalid after removing tracks etc.
                 update_track_info_display(None)
        else:
             update_track_info_display(None)

    except pygame.error as e:
        print(f"Error stopping music: {e}")
        status_label.configure(text="Error stopping playback")
        _is_internal_update = True
        progress_slider.set(0)
        if progress_slider: progress_slider.configure(state="disabled")
        _is_internal_update = False


def next_track():
    global current_track_index, is_playing, is_paused
    if not playlist: return

    current_track_index = (current_track_index + 1) % len(playlist)
    playlist_box.selection_clear(0, tk.END)
    playlist_box.selection_set(current_track_index)
    playlist_box.activate(current_track_index)
    playlist_box.see(current_track_index)

    stop_music()
    is_playing = False
    is_paused = False
    play_music()

def previous_track():
    global current_track_index, is_playing, is_paused
    if not playlist: return

    current_track_index = (current_track_index - 1 + len(playlist)) % len(playlist)
    playlist_box.selection_clear(0, tk.END)
    playlist_box.selection_set(current_track_index)
    playlist_box.activate(current_track_index)
    playlist_box.see(current_track_index)

    stop_music()
    is_playing = False
    is_paused = False
    play_music()

def set_volume(value):
    try:
        volume = float(value) / 100.0
        pygame.mixer.music.set_volume(volume)

    except pygame.error as e:
        print(f"Error setting volume: {e}")
    except ValueError:
        print(f"Invalid volume value received: {value}")

def update_track_info_display(file_path, duration_seconds=None):
    global _is_internal_update, progress_slider
    if file_path:
        filename = os.path.basename(file_path)
        if duration_seconds is None:
            duration_seconds = get_track_duration(file_path)
        duration_str = format_time(duration_seconds)

        current_time_seconds = 0
        if pygame.mixer.get_init() and pygame.mixer.music.get_pos():
           current_time_seconds = pygame.mixer.music.get_pos()/1000.0
        if duration_seconds is not None and current_time_seconds > duration_seconds:
            current_time_seconds = duration_seconds
        if current_time_seconds < 0:
            current_time_seconds = 0
        current_time_str = format_time(current_time_seconds)

        track_info_label.configure(text=f"{filename}")
        time_info_label.configure(text=f"{current_time_str} / {duration_str}")

        if duration_seconds is not None and duration_seconds > 0:
            progress_percent = (current_time_seconds / duration_seconds) * 100
            # Set the internal update flag BEFORE setting the slider value
            _is_internal_update = True
            progress_slider.set(progress_percent)
            # Release the flag AFTER setting the value
            _is_internal_update = False
            if progress_slider.cget("state") == "disabled":
                 progress_slider.configure(state="normal") # Enable if disabled
        else:
            # Disable slider if duration is invalid
             _is_internal_update = True
             progress_slider.set(0)
             progress_slider.configure(state="disabled")
             _is_internal_update = False

    else:
        track_info_label.configure(text="No track loaded")
        time_info_label.configure(text="--:-- / --:--")
        _is_internal_update = True
        progress_slider.set(0)
        progress_slider.configure(state="disabled")
        _is_internal_update = False
    if is_playing and not is_paused:
        root.after(1000, lambda: update_track_info_display(file_path, duration_seconds))


def on_track_select(event):
    global current_track_index
    selected_indices = playlist_box.curselection()
    if selected_indices:
        current_track_index = selected_indices[0]
        file_path = playlist[current_track_index]
        duration_seconds = get_track_duration(file_path)
        update_track_info_display(file_path, duration_seconds)
        if is_playing or is_paused:
            stop_music()
            status_label.configure(text="Track selected. Press Play.")

def on_track_double_click(event):
    global current_track_index, is_playing, is_paused
    selected_indices = playlist_box.curselection()
    if selected_indices:
        current_track_index = selected_indices[0]
        stop_music()
        is_playing = False
        is_paused = False
        play_music()

def check_music_end():
    global root
    if is_playing and not is_paused:
        if not pygame.mixer.music.get_busy():
            print("Track finished, playing next.")
            next_track()
        else:
            root.after(200, check_music_end)


def setup_gui():
    global root, playlist_box, track_info_label, time_info_label, status_label, play_pause_button, volume_slider, progress_slider
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.title("AJ's Music Player")
    root.geometry("550x600")
    playlist_frame = ctk.CTkFrame(root)
    playlist_frame.pack(pady=20, padx=20, fill="both",expand=True)

    info_frame = ctk.CTkFrame(root)
    info_frame.pack(pady=10, padx=20, fill="x")

    progress_frame = ctk.CTkFrame(root)
    progress_frame.pack(pady=(0,5), padx=20, fill="x")

    controls_frame = ctk.CTkFrame(root)
    controls_frame.pack(pady=10, padx=20, fill="x")


    status_frame = ctk.CTkFrame(root)
    status_frame.pack(pady=10, padx=20, fill="x")

    load_button = ctk.CTkButton(playlist_frame, text="Load Music Folder", command=load_folder)
    load_button.pack(pady=10)

    playlist_box = tk.Listbox(playlist_frame,
                              bg="#2B2B2B",        # Background color (dark grey)
                              fg="white",         # Text color
                              selectbackground="#1F6AA5", # Background color when selected (CTk blue)
                              selectforeground="white", # Text color when selected
                              activestyle='none',   # No underline on active item
                              borderwidth=0,      # No border
                              highlightthickness=0, # No focus border
                              font=("Roboto", 12)) # Font
    playlist_box.pack(pady=10, padx=10, fill="both", expand=True)
    # Bind events to the listbox:
    # <ButtonRelease-1> is generally better than <Button-1> for selection
    playlist_box.bind('<ButtonRelease-1>', on_track_select)
    # <Double-Button-1> for double-click action
    playlist_box.bind('<Double-Button-1>', on_track_double_click)


    # --- Track Info Section ---
    # Label to display the current track's filename
    track_info_label = ctk.CTkLabel(info_frame, text="No track loaded", font=ctk.CTkFont(size=14, weight="bold"))
    track_info_label.pack(pady=(5, 0)) # Padding top

    # Label to display current time / total duration
    time_info_label = ctk.CTkLabel(info_frame, text="--:-- / --:--", font=ctk.CTkFont(size=12))
    time_info_label.pack(pady=(0, 5)) # Padding bottom

    progress_slider = ctk.CTkSlider(progress_frame, from_=0, to=100, number_of_steps=1000, command=seek_music)
    progress_slider.set(0)
    progress_slider.pack(fill="x", padx=5, pady=(0, 10))
    progress_slider.configure(state="disabled")


    # --- Controls Section ---
    # Configure the grid layout for the controls frame (3 columns)
    controls_frame.columnconfigure((0, 1, 2), weight=1) # Make columns expand equally

    # Previous Track Button
    prev_button = ctk.CTkButton(controls_frame, text="⏮ Prev", command=previous_track, width=80)
    prev_button.grid(row=0, column=0, padx=5, pady=5) # Place in grid

    # Play/Pause Button (toggles functionality)
    play_pause_button = ctk.CTkButton(controls_frame, text="▶ Play", command=pause_resume_music, width=100)
    # We use pause_resume_music which decides whether to play or pause
    play_pause_button.grid(row=0, column=1, padx=5, pady=5)

    # Next Track Button
    next_button = ctk.CTkButton(controls_frame, text="Next ⏭", command=next_track, width=80)
    next_button.grid(row=0, column=2, padx=5, pady=5)

    # Stop Button
    stop_button = ctk.CTkButton(controls_frame, text="⏹ Stop", command=stop_music, width=80)
    stop_button.grid(row=1, column=1, padx=5, pady=10) # Place below play/pause

    # Volume Label
    volume_label = ctk.CTkLabel(controls_frame, text="Volume:", font=ctk.CTkFont(size=12))
    volume_label.grid(row=2, column=0, padx=(10,0), pady=5, sticky="e") # Align right


    # Volume Slider
    volume_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, command=set_volume, number_of_steps=100)
    volume_slider.set(70) # Set default volume to 70%
    # Call set_volume initially to set the actual pygame volume
    set_volume(volume_slider.get())
    volume_slider.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew") # Span 2 columns, stretch horizontally


    # --- Status Bar Section ---
    # Label to display status messages (Loading, Playing, Paused, Stopped, Errors)
    status_label = ctk.CTkLabel(status_frame, text="Welcome! Load a folder to start.", anchor="w") # Align text left
    status_label.pack(fill="x", padx=5, pady=2)

if __name__ == "__main__":
    initialize_player()
    setup_gui()
    root.mainloop()
    pygame.mixer.quit()
    print("Player closed.")
