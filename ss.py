import pyautogui as pag
import requests
import time
import os
from datetime import datetime
import win32gui
import win32con

# Configuration
SCREENSHOT_DIR = "screenshots"
SCREENSHOT_PREFIX = "screenshot"
GOFILE_API_URL = "https://store1.gofile.io/uploadFile"
DELAY = 0.5  # Reduced delay for faster execution

# Ensure screenshot directory exists
if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

# Minimize specific windows by title
def minimize_windows():
    try:
        def minimize_window(title_contains):
            hwnd = win32gui.FindWindow(None, None)
            while hwnd:
                title = win32gui.GetWindowText(hwnd)
                if title_contains.lower() in title.lower() and win32gui.IsWindowVisible(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
                    print(f"Minimized window: {title}")
                    return True
                hwnd = win32gui.GetWindow(hwnd, win32con.GW_HWNDNEXT)
            return False

        # Minimize Command Prompt and PowerShell
        minimized_cmd = minimize_window("Command Prompt") or minimize_window("cmd.exe")
        minimized_ps = minimize_window("PowerShell")
        
        if not minimized_cmd:
            print("Command Prompt window not found.")
        if not minimized_ps:
            print("PowerShell window not found.")
        
    except Exception as e:
        print(f"Failed to minimize windows: {e}")

# Take a screenshot and save it
def take_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SCREENSHOT_DIR, f"{SCREENSHOT_PREFIX}_{timestamp}.png")
    try:
        screenshot = pag.screenshot()
        screenshot.save(filename)
        if os.path.exists(filename):
            print(f"Screenshot saved as {filename}.")
            return filename
        else:
            raise Exception("Screenshot file not created.")
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
        return None

# Upload the screenshot to Gofile
def upload_to_gofile(filepath):
    try:
        with open(filepath, 'rb') as file:
            files = {'file': file}
            response = requests.post(GOFILE_API_URL, files=files, timeout=10)
            response.raise_for_status()

            result = response.json()
            if result['status'] == 'ok':
                download_page = result['data']['downloadPage']
                print(f"Screenshot uploaded successfully. Link: {download_page}")
                return download_page
            else:
                print(f"Upload error: {result.get('status')}")
                return None
    except Exception as e:
        print(f"Failed to upload screenshot: {e}")
        return None

# Main function
def main():
    try:
        # Minimize windows
        minimize_windows()
        time.sleep(DELAY)  # Brief pause to ensure windows are minimized

        # Take screenshot
        screenshot_filename = take_screenshot()
        if not screenshot_filename:
            print("Exiting due to screenshot failure.")
            return

        # Upload to Gofile
        gofile_link = upload_to_gofile(screenshot_filename)
        
        # Clean up only if upload was successful
        if gofile_link and os.path.exists(screenshot_filename):
            os.remove(screenshot_filename)
            print(f"Temporary screenshot file {screenshot_filename} removed.")
        elif not gofile_link:
            print(f"Keeping screenshot file {screenshot_filename} due to upload failure.")

    except Exception as e:
        print(f"Script failed: {e}")

if __name__ == "__main__":
    main()
