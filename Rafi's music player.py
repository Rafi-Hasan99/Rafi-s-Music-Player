import os
from tkinter import *
from tkinter import filedialog
import pygame
import colorsys

class RafisMusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Rafi's Music Player")
        self.base_color = "#1DB954"  
        self.root.configure(bg=self.base_color)
        
        pygame.init()
        pygame.mixer.init()
        
        self.track = StringVar()
        self.status = StringVar()
        
        self.playlist = []
        self.current_track = 0
        
        self.create_ui()
        self.animate_background()
        
    def create_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        main_frame = Frame(self.root, bg=self.base_color)
        main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Track display
        self.track_label = Label(self.root, textvariable=self.track, font=("Helvetica", 16, "bold"), bg=self.base_color, fg="#000000")
        self.track_label.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        button_style = {
            'font': ("Helvetica", 12, "bold", "italic"),
            'bg': "#000000",
            'fg': "#800080",
            'activebackground': "#1a1a1a",
            'activeforeground': "#800080",
            'relief': RAISED,
            'bd': 3,
            'width': 12,
            'height': 2
        }
        
        # First row of buttons
        playbtn = Button(main_frame, text="PLAY", command=self.playsong, **button_style)
        playbtn.grid(row=0, column=0, padx=5, pady=5)
        
        stopbtn = Button(main_frame, text="STOP", command=self.stopsong, **button_style)
        stopbtn.grid(row=0, column=1, padx=5, pady=5)
        
        loadbtn = Button(main_frame, text="LOAD TRACK", command=self.load_track, **button_style)
        loadbtn.grid(row=0, column=2, padx=5, pady=5)
        
        addtrackbtn = Button(main_frame, text="ADD TRACK", command=self.add_track, **button_style)
        addtrackbtn.grid(row=0, column=3, padx=5, pady=5)
        
        # Second row of buttons
        nextbtn = Button(main_frame, text="NEXT", command=self.next_track, **button_style)
        nextbtn.grid(row=1, column=0, padx=5, pady=5)
        
        prevbtn = Button(main_frame, text="PREVIOUS", command=self.prev_track, **button_style)
        prevbtn.grid(row=1, column=1, padx=5, pady=5)
        
        showplaylistbtn = Button(main_frame, text="SHOW PLAYLIST", command=self.show_playlist, **button_style)
        showplaylistbtn.grid(row=1, column=2, padx=5, pady=5)
    
    def animate_background(self):
        h, s, v = colorsys.rgb_to_hsv(*[x/255 for x in self.root.winfo_rgb(self.base_color)])
        v = (v + 0.01) % 0.2 + 0.8  # Oscillate value between 0.8 and 1.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        new_color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
        self.root.configure(bg=new_color)
        self.track_label.configure(bg=new_color)
        self.root.after(50, self.animate_background)
        
    def load_track(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            self.playlist = [file_path]
            self.current_track = 0
            self.track.set(f"Loaded: {os.path.basename(file_path)}")
        
    def playsong(self):
        if self.playlist:
            self.track.set(os.path.basename(self.playlist[self.current_track]))
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
        
    def stopsong(self):
        pygame.mixer.music.stop()
        self.track.set("Stopped")

    def next_track(self):
        if self.playlist:
            self.current_track = (self.current_track + 1) % len(self.playlist)
            self.playsong()

    def prev_track(self):
        if self.playlist:
            self.current_track = (self.current_track - 1) % len(self.playlist)
            self.playsong()

    def add_track(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            self.playlist.append(file_path)
            self.track.set(f"Added: {os.path.basename(file_path)}")

    def show_playlist(self):
        playlist_window = Toplevel(self.root)
        playlist_window.title("Current Playlist")
        playlist_window.geometry("400x400")
        playlist_window.configure(bg=self.base_color)
        
        playlist_box = Listbox(playlist_window, width=60, height=20, bg="#000000", fg="#1DB954", font=("Helvetica", 10))
        playlist_box.pack(padx=10, pady=10, fill=BOTH, expand=True)
        
        for index, track in enumerate(self.playlist, start=1):
            playlist_box.insert(END, f"{index}. {os.path.basename(track)}")

root = Tk()
root.geometry("800x600")
player = RafisMusicPlayer(root)
root.mainloop()