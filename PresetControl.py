# This script can be used independently to change the preset of a camera using input arguments or from another script.
# Usage: python PresetControl.py --IP="127.0.0.1" --PRESET=[NUMBER]

# As is, the camera takes 3 seconds to change the preset, and 8.5 seconds to return.

# To login:
# $('#edtUserName').textbox('setValue', 'USERNAME');
# $('#edtPassword').textbox('setValue', 'PASSWORD');
# loginClick();

# To change camera preset:
# postPTZCtrl('preset_call', number)

# postPTZCtrl is defined in pages/live.asp in common.js

# turns out I don't need to login to change presets, just need to be on the live page

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

def change_preset(IP, PRESET):
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--log-level=3')
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(2)

    try:
        driver.get(f'http://{IP}/pages/live.asp')
    except WebDriverException as e:
        driver.close()
        raise ValueError("failed to connect to camera")
    
    try:
        driver.execute_script(f"postPTZCtrl('preset_call', {PRESET});")
    except WebDriverException as e:
        driver.close()
        raise ValueError("failed to change preset")
    
    driver.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Camera Controller')
    parser.add_argument('--IP', action="store", dest='IP', default=0)
    parser.add_argument('--PRESET', action="store", dest='PRESET', default=0)
    args = parser.parse_args()

    change_preset(args.IP, args.PRESET)
