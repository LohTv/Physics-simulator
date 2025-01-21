import tkinter as tk
from tkinter import ttk

def open_settings_window(parent, current_settings, save_callback):

    def save_and_close():
        # Update settings and close the settings window
        new_settings = {
            "language": language_var.get(),
            "volume": volume_slider.get()
        }
        save_callback(new_settings)
        settings_window.destroy()

    # Create a new window for settings
    settings_window = tk.Toplevel(parent)
    settings_window.title("Settings")

    # Language Dropdown Menu
    language_label = tk.Label(settings_window, text="Select Language:")
    language_label.pack(pady=5)

    languages = ["English", "Spanish", "French", "German", "Chinese"]
    language_var = tk.StringVar(value=current_settings.get("language", languages[0]))

    language_menu = ttk.Combobox(settings_window, textvariable=language_var, values=languages, state="readonly")
    language_menu.pack(pady=5)

    # Music Volume Slider
    volume_label = tk.Label(settings_window, text="Music Volume:")
    volume_label.pack(pady=5)

    volume_slider = tk.Scale(settings_window, from_=0, to=100, orient="horizontal")
    volume_slider.set(current_settings.get("volume", 50))
    volume_slider.pack(pady=5)

    # Save button
    save_button = tk.Button(settings_window, text="Save", command=save_and_close)
    save_button.pack(pady=10)
