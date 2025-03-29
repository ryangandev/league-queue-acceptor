import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5  # Small delay between PyAutoGUI calls (optional)

print("🎮 League Queue Auto-Acceptor running...")

while True:
    try:
        print("🔍 Scanning for accept button...")
        button_location = pyautogui.locateOnScreen("accept_button.png", confidence=0.8)

        if button_location:
            print("✅ Accept button found!")
            pyautogui.moveTo(pyautogui.center(button_location), duration=0.2)
            pyautogui.click()
            print("🖱️ Clicked accept! Waiting before next scan...")
            time.sleep(10)  # Wait to avoid multiple clicks

        else:
            time.sleep(1)  # Button not found, check again in 1 sec

    except pyautogui.ImageNotFoundException:
        print("❌ Image not found (exception). Retrying...")
        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        time.sleep(1)
