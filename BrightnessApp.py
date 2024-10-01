import tkinter as tk
from tkinter import ttk
import screen_brightness_control as sbc

# Function to update brightness for a specific display
def update_brightness(display_index, val):
    brightness_level = int(val)
    sbc.set_brightness(brightness_level, display=display_index)
    labels[display_index].config(text=f"Display {display_index + 1} Brightness: {brightness_level}%")

# Function to update brightness for all displays
def update_master_brightness(val):
    brightness_level = int(val)
    for i in range(len(displays)):
        sliders[i].set(brightness_level)
    master_label.config(text=f"Master Brightness: {brightness_level}%")

# Create the root window
root = tk.Tk()
root.title("Multi-Display Brightness Control")

# Detect all connected displays
displays = sbc.list_monitors()

# Calculate window height based on the number of displays
num_displays = len(displays)
window_height = (100 + num_displays * 80)+150  # 100px for static parts, 80px per display

# Set geometry of the window
root.geometry(f"500x{window_height}")
root.configure(bg="#f0f0f0")

# Style configuration
style = ttk.Style(root)
style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0", foreground="#333333")
style.configure("TScale", background="#f0f0f0", troughcolor="#cccccc", sliderlength=30)
style.configure("TButton", font=("Helvetica", 10), background="#e0e0e0", foreground="#333333")

# Create a frame for display controls
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=20, pady=10, fill='both', expand=True)

# Create a list to hold the sliders and labels
sliders = []
labels = []

# Add a slider and label for each display
for i, display in enumerate(displays):
    current_brightness = sbc.get_brightness(display=i)[0]
    
    # Create a frame for each display's controls
    display_frame = tk.Frame(frame, bg="#f0f0f0")
    display_frame.pack(pady=10, fill='x')

    # Create a label to show the current brightness percentage for this display, above the slider
    label = tk.Label(display_frame, text=f"Display {i + 1} Brightness: {current_brightness}%",
                     bg="#f0f0f0", font=("Helvetica", 12))
    label.pack(pady=(0, 5))  # Padding below the label
    
    # Create a slider widget for this display
    slider = tk.Scale(display_frame, from_=0, to=100, orient='horizontal', length=400,
                      command=lambda val, i=i: update_brightness(i, val), bg="#f0f0f0",
                      troughcolor="#cccccc", sliderlength=30, highlightbackground="#f0f0f0")
    slider.set(current_brightness)
    slider.pack()

    # Add the slider and label to their respective lists
    sliders.append(slider)
    labels.append(label)

# Add a master frame for the master slider and its label
master_frame = tk.Frame(root, bg="#f0f0f0")
master_frame.pack(pady=(10, 20), fill='x')  # Reduced top padding, increased bottom padding

master_slider = tk.Scale(master_frame, from_=0, to=100, orient='horizontal', length=400,
                        command=update_master_brightness, bg="#f0f0f0", troughcolor="#cccccc",
                        sliderlength=30, highlightbackground="#f0f0f0")
master_slider.set(min(sbc.get_brightness()))  # Set it to the minimum brightness of all displays
master_slider.pack(pady=5)  # Reduced padding

# Add a label for the master slider
master_label = tk.Label(master_frame, text=f"Master Brightness: {min(sbc.get_brightness())}%",
                        bg="#f0f0f0", font=("Helvetica", 14, 'bold'))
master_label.pack(pady=(5, 10))  # Reduced top padding, increased bottom padding

# Start the Tkinter event loop
root.mainloop()
