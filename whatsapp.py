import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip
import sys
import os
from whatsapp.config import CHROME_PROFILE_PATH
from whatsapp.config import CHROME_PROFILE_PATH

def send_message_to_group(browser, group, msg, attachment=None):
    try:
        search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'

        search_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, search_xpath))
        )

        search_box.clear()
        search_box.send_keys(group)
        search_box.send_keys(Keys.ENTER)

        time.sleep(2)  # Adjust this time if necessary for page to load

        group_xpath = f'//span[@title="{group}"]'
        group_title = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, group_xpath))
        )
        group_title.click()

        input_xpath = '//div[@contenteditable="true"][@data-tab="1"]'
        input_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, input_xpath))
        )

        input_box.send_keys(msg)
        input_box.send_keys(Keys.ENTER)

        if attachment:
            attachment_box = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]'))
            )
            attachment_box.click()

            image_box = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
            )
            image_box.send_keys(attachment)

            send_btn = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_btn.click()

    except Exception as e:
        print(f"Error sending message to {group}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please provide the group name as the first argument.')
        sys.exit(1)

    group_file = sys.argv[1]
    if not os.path.exists(group_file):
        print(f"File '{group_file}' not found.")
        sys.exit(1)

    msg_file = 'msg.txt'
    if not os.path.exists(msg_file):
        print(f"Message file '{msg_file}' not found.")
        sys.exit(1)

    with open(group_file, 'r', encoding='utf8') as f:
        group = [group.strip() for group in f.readlines()]
        

    with open(msg_file, 'r', encoding='utf8') as f:
        msg = f.read()

    attachment = sys.argv[2] if len(sys.argv) == 3 else None

    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)

    browser = webdriver.Chrome(
        executable_path=r'C:\Users\ASUS\AppData\Local\Google\Chrome\User Data\Default\chromedriver-win64\chromedriver.exe', options=options)

    browser.maximize_window()

    browser.get('https://web.whatsapp.com/')

    for group in group:
        send_message_to_group(browser, group, msg, attachment)

    browser.quit()
