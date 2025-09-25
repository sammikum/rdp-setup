import pyautogui as pag
import time
import requests
import os
import subprocess

# Initial wait time
time.sleep(40)

actions = [
    (516, 405, 4),  # install
    (50, 100, 1),   # launch Avica
    (496, 438, 4),  # later update
    (249, 203, 4),  # allow RDP button (multiple clicks)
    (249, 203, 4),
    (249, 203, 4),
    (249, 203, 4),
    (447, 286, 4),  # ss id & upload (take screenshot and upload)
]

time.sleep(10)

img_filename = 'NewAvicaRemoteID.png'

def upload_image_to_gofile(img_filename):
    url = 'https://store1.gofile.io/uploadFile'
    try:
        with open(img_filename, 'rb') as img_file:
            files = {'file': img_file}
            response = requests.post(url, files=files)
            response.raise_for_status()
            result = response.json()
            if result.get('status') == 'ok':
                download_page = result['data']['downloadPage']
                with open('show.bat', 'a') as bat_file:
                    bat_file.write(f'\necho Avica Remote ID : {download_page}')
                return download_page
            else:
                print("Upload error:", result.get('status'))
                return None
    except Exception as e:
        print(f"Failed to upload image: {e}")
        return None

for x, y, duration in actions:
    pag.click(x, y, duration=duration)
    if (x, y) == (249, 203):
        time.sleep(1)
        pag.click(x, y, duration=duration)

    if (x, y) == (447, 286):
        avica_exe = os.path.join(os.getcwd(), "Avica_setup.exe")
        try:
            # Start Avica from current directory
            subprocess.Popen([avica_exe])
        except Exception as e:
            print(f"Failed to start Avica: {e}")

        time.sleep(5)
        pag.click(249, 203, duration=4)
        time.sleep(10)
        pag.screenshot().save(img_filename)

        gofile_link = upload_image_to_gofile(img_filename)
        if gofile_link:
            print(f"Image uploaded successfully. Link: {gofile_link}")
        else:
            print("Failed to upload the image.")
    
    time.sleep(10)

print('Done!')
