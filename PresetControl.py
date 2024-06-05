# 192.168.1.8/pages/login.asp
# 192.168.1.8/pages/main.asp

#Neither textbox can be "Focused" when logging in!

#camera controls are in live.js

# To login:
# $('#edtUserName').textbox('setValue', 'USERNAME');
# $('#edtPassword').textbox('setValue', 'PASSWORD');
# loginClick();

# To change camera preset:
# postPTZCtrl('preset_call', number)

# postPTZCtrl is defined in pages/live.asp in common.js

# turns out I don't need to login to change presets, just need to be on the live page

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# have not made error handling.
def change_preset(IP, PRESET):
    driver = webdriver.Firefox()
    driver.get(f'http://{IP}/pages/live.asp')
    driver.execute_script(f"postPTZCtrl('preset_call', {PRESET});")
    driver.quit()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Camera Controller')
    parser.add_argument('--IP', action="store", dest='IP', default=0)
    parser.add_argument('--PRESET', action="store", dest='PRESET', default=0)
    args = parser.parse_args()

    change_preset(args.IP, args.PRESET)
