import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import pyautogui
import json
import os
import random
from datetime import datetime
from PIL import Image, ImageTk

CONFIG_FILE = "config.json"
DEFAULT_IMAGE = "accept_button.png"
DEFAULT_CONFIDENCE = 0.85


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return {"image_path": DEFAULT_IMAGE}


def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


config = load_config()
running = False


def log_event(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_text.insert(tk.END, f"{timestamp} {message}\n")
    log_text.see(tk.END)


# --- Scanning Logic ---
def toggle_scanning():
    global running
    running = not running
    if running:
        log_event("Started scanning...")
        toggle_button.config(text="⏹ Stop")
        threading.Thread(target=scan_loop, daemon=True).start()
    else:
        log_event("Stopped scanning.")
        toggle_button.config(text="▶ Start")


def move_human_like(to_x, to_y):
    from_x, from_y = pyautogui.position()
    steps = random.randint(10, 20)
    for step in range(steps):
        intermediate_x = (
            from_x + (to_x - from_x) * (step / steps) + random.uniform(-3, 3)
        )
        intermediate_y = (
            from_y + (to_y - from_y) * (step / steps) + random.uniform(-3, 3)
        )
        pyautogui.moveTo(intermediate_x, intermediate_y, duration=0.01)
    pyautogui.moveTo(to_x, to_y, duration=0.1)


def scan_loop():
    while running:
        try:
            location = pyautogui.locateOnScreen(
                config["image_path"], confidence=DEFAULT_CONFIDENCE
            )
            if location:
                log_event("Queue found.")
                rand_delay = round(random.uniform(2, 6), 2)
                time.sleep(rand_delay)

                offset_x = random.randint(5, location.width - 5)
                offset_y = random.randint(5, location.height - 5)
                target_x = location.left + offset_x
                target_y = location.top + offset_y

                move_human_like(target_x, target_y)
                pyautogui.click()
                log_event(f"Accepted match (after {rand_delay}s delay).")
                time.sleep(10)
            else:
                time.sleep(1)
        except Exception as e:
            # Error would be if the image is not found, so continue scanning
            time.sleep(1)


# --- Image Settings ---
def select_image():
    file_path = filedialog.askopenfilename(
        title="Select Accept Button Image That Fits Your Resolution",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")],
    )
    if file_path:
        config["image_path"] = file_path
        save_config()
        update_image_preview()
        log_event(f"Custom image set: {file_path}")


def reset_image():
    config["image_path"] = DEFAULT_IMAGE
    save_config()
    update_image_preview()
    log_event("Reset to default accept button image.")


def update_image_preview():
    try:
        img = Image.open(config["image_path"])
        img.thumbnail((150, 150))
        img_tk = ImageTk.PhotoImage(img)
        image_preview_label.config(image=img_tk)
        image_preview_label.image = img_tk
    except Exception as e:
        print("Error loading image preview:", e)


# --- UI Setup ---
window = tk.Tk()
window.title("League Queue Auto-Acceptor")
window.geometry("1000x500")

# --- Disclaimer Popup ---
messagebox.showwarning(
    "Disclaimer",
    "This tool may violate Riot's Terms of Service and could result in a ban.\nUse it at your own risk.",
)

main_frame = tk.Frame(window, width=250)
main_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
main_frame.pack_propagate(False)

log_frame = tk.Frame(window)
log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Top button
toggle_button = tk.Button(main_frame, text="▶ Start", command=toggle_scanning, width=20)
toggle_button.pack(pady=10)

# Center container for image-related widgets
center_frame = tk.Frame(main_frame)
center_frame.pack(expand=True)

image_preview_label = tk.Label(center_frame)
image_preview_label.pack(pady=10)
update_image_preview()

select_image_button = tk.Button(
    center_frame, text="Set Accept Button Image", command=select_image
)
select_image_button.pack(pady=5)

reset_image_button = tk.Button(
    center_frame, text="Reset to Default Image", command=reset_image
)
reset_image_button.pack(pady=5)

note_label = tk.Label(
    center_frame,
    text="Note:\nDefault image is for 1600x900 League client resolution.\nReplace it if your client resolution differs.",
    fg="gray",
    justify="left",
    wraplength=230,
)
note_label.pack(pady=20)

# Exit button
exit_button = tk.Button(main_frame, text="❌ Exit", command=window.quit, width=20)
exit_button.pack(side=tk.BOTTOM, pady=20)

# Logging
log_label = tk.Label(log_frame, text="Activity Log")
log_label.pack(anchor="w")

log_text = tk.Text(log_frame, height=20, state="normal")
log_text.pack(fill=tk.BOTH, expand=True)

log_event("Click Start to begin auto-accepting queues.")

window.mainloop()
