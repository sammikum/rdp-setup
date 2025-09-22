import pyautogui as pag
import subprocess
import time
import os

# Configuration
AVICA_EXE_PATH = r"C:\Program Files (x86)\Avica\Avica.exe"  # Adjust if needed
BUTTON_IMAGE = "screenshot_button.png"  # Small PNG of the "Screenshot" button
DELAY_AFTER_LAUNCH = 5  # Seconds to wait for app to load
CONFIDENCE = 0.8  # Matching confidence for image detection (0.8 = 80%)

# Safety: Fail-safe to stop script if mouse moves to top-left corner
pag.FAILSAFE = True
pag.PAUSE = 1  # Pause between actions

def launch_avica():
    """Launch Avica.exe using subprocess."""
    try:
        if not os.path.exists(AVICA_EXE_PATH):
            raise FileNotFoundError(f"Avica.exe not found at {AVICA_EXE_PATH}. Check install path.")
        
        subprocess.Popen(AVICA_EXE_PATH)
        print("Avica launched successfully.")
        time.sleep(DELAY_AFTER_LAUNCH)  # Wait for UI to appear
    except Exception as e:
        print(f"Failed to launch Avica: {e}")
        return False
    return True

def click_screenshot_button():
    """Locate and click the 'Screenshot' button using image recognition."""
    try:
        if not os.path.exists(BUTTON_IMAGE):
            raise FileNotFoundError(f"Button image '{BUTTON_IMAGE}' not found. Capture it from Avica UI.")
        
        # Search for the button on screen
        button_location = pag.locateOnScreen(BUTTON_IMAGE, confidence=CONFIDENCE)
        if button_location:
            # Click the center of the button
            pag.click(pag.center(button_location))
            print("Clicked 'Screenshot' button successfully.")
            time.sleep(2)  # Wait for screenshot dialog/action
            return True
        else:
            print("Screenshot button not found. Trying coordinate fallback (adjust coords as needed).")
            # Fallback: Hardcoded coords (example: toolbar position; update based on your screen)
            # pag.click(100, 50)  # Uncomment and set x,y for button center
            return False
    except Exception as e:
        print(f"Failed to click button: {e}")
        return False

def main():
    print("Starting Avica automation...")
    
    # Step 1: Launch Avica
    if not launch_avica():
        return
    
    # Step 2: Click Screenshot button (assumes app is focused)
    # Note: You may need to manually connect to a remote session first for the button to appear
    click_screenshot_button()
    
    print("Automation complete. Check Avica for the screenshot.")

if __name__ == "__main__":
    main()
