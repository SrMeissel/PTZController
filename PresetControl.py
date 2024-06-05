# This script can be used independently to change the preset of a camera using input arguments or from another script.
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# have not implemented error handling error handling.
def change_preset(IP, PRESET):
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--log-level=3')
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(f'http://{IP}/pages/live.asp')
    except WebDriverException as e:
        driver.close()
        raise ValueError("failed to connect to camera")
    try:
        driver.execute_script(f"postPTZCtrl('preset_call', {PRESET});")
        pass
    except WebDriverException as e:
        driver.close()
        raise ValueError("failed to change preset")
    
    driver.quit()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Camera Controller')
    parser.add_argument('--IP', action="store", dest='IP', default=0)
    parser.add_argument('--PRESET', action="store", dest='PRESET', default=0)
    args = parser.parse_args()

    change_preset(args.IP, args.PRESET)
