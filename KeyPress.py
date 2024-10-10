from imaplib import Commands
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
from pynput import keyboard

# Initialize pygame for audio
pygame.mixer.init()

#Global variables
key_press_count = 0
trigger_count = 0
audio_file_path = ""
target_key = ""
max_triggers = 0
press_limit = 0

# Function to play the selected audio
def play_audio():
    if audio_file_path:
        pygame.mixer.Sound(audio_file_path).play()

# Function to handle key presses
def on_press(key):
    global key_press_count, trigger_count, target_key, press_limit, max_triggers

    try:
        if key.char == target_key:
            key_press_count += 1
            if key_press_count >= press_limit:
                play_audio()
                trigger_count += 1
                key_press_count = 0

                if trigger_count >= max_triggers:
                    listener.stop() # Stop the listener once the target is met
                    messagebox.showinfo("Application Shutdown", f"Application has shut down after {max_triggers} triggers.")
    except AttributeError:
        pass # Ignore special keys

# Function to select the audio file
def select_audio_file():
    global audio_file_path
    audio_file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.mp3 *.wav")])
    if audio_file_path:
        audio_file_label.config(text=os.path.basename(audio_file_path))

# Function to start the key listener and the application
def start_application():
    global target_key, press_limit, max_triggers

    try:
        target_key = key_entry.get().lower() # Store the chosen key
        press_limit = int(press_entry.get())  # Number of presses to trigger the sound
        max_triggers = int(trigger_entry.get())  # Maximum number of triggers before shutdown

        if not audio_file_path or not target_key:
            messagebox.showwarning("Input Error", "Please select an audio file and specify the target key")
            return

        # Start the key listener
        global listener
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        messagebox.showinfo("Application Running", f"Application started! Listening for {target_key.upper()} key press.")

    except ValueError:
        messagebox.showwarning("Input Error", "Please enter valid numbers for key presses and trigger limit.")

# Function to exit the application
def exit_application():
    root.quit()

# GUI setup
root = tk.Tk()
root.title("Key Trigger Application")
root.geometry("400x300")

# Audio file selection
audio_file_label = tk.Label(root, text="No file selected")
audio_file_label.pack(pady=10)
audio_button = tk.Button(root, text="Select Audio File", command=select_audio_file)
audio_button.pack()

# Key press settings
key_label = tk.Label(root, text="Key to Listen For:")
key_label.pack()
key_entry = tk.Entry(root)
key_entry.pack()

press_label = tk.Label(root, text="Presses to Trigger Audio:")
press_label.pack()
press_entry = tk.Entry(root)
press_entry.pack()

trigger_label = tk.Label(root, text="Max Audio Triggers:")
trigger_label.pack()
trigger_entry = tk.Entry(root)
trigger_entry.pack()

# Start and exit buttons
start_button = tk.Button(root, text="Start Application", command=start_application)
start_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack(pady=10)

root.mainloop()