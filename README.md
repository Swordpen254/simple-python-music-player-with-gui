# AJ's Music Player

A simple MP3 music player built with Python, Pygame, and CustomTkinter. Play your favorite tracks from a selected folder with a clean, modern interface.


## Features

*   **Load Music:** Select a folder to load all MP3 files within it into the playlist.
*   **Playback Controls:** Play, Pause, Resume, Stop, Next Track, Previous Track.
*   **Volume Control:** Adjust playback volume using a slider.
*   **Playlist Display:** View the loaded tracks in a list.
*   **Track Selection:** Select tracks with a single click, play with a double click.
*   **Progress Display:** See the current playback time and total duration of the track.
*   **Seek Bar:** Click or drag the progress slider to jump to different parts of the track.
*   **Status Bar:** Get feedback on loading, playback status, and errors.
*   **Modern UI:** Uses the CustomTkinter library for themed widgets.

## Requirements

*   Python 3.7+ (f-strings and newer library features recommended)
*   Pygame (`pygame`)
*   Mutagen (`mutagen`)
*   CustomTkinter (`customtkinter`)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ajs-music-player.git # Replace with your repo URL
    cd ajs-music-player
    ```

2.  **Create a virtual environment (Recommended):**
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. 
    Install requirements using pip:
    ```bash
    pip install -r requirements.txt
    ```
    Alternatively, install them directly:
    ```bash
    pip install pygame mutagen customtkinter
    ```

## Usage

1.  Make sure you are in the project directory (`ajs-music-player`) and your virtual environment (if used) is activated.
2.  Run the application:
    ```bash
    python music_app.py
    ```
    *(Replace `music_app.py` if you named your file differently)*
3.  Click the "Load Music Folder" button and select a directory containing MP3 files.
4.  Tracks will appear in the playlist.
5.  Double-click a track to play, or select one and use the playback control buttons.
6.  Use the sliders to control volume and seek through the track.


