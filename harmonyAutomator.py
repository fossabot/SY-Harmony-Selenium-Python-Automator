import time
import keyring
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

harmony_url = "http://harmonyurl"
windows_vault_service_name = "eHarmony"
default_start_work = "09:00"
default_end_work = "18:00"
default_background = 0
cmd_format = ">python harmonyAutomator.py <username> <Start Work XX:XX> <End Work XX:XX> " \
             "<Execute in Background 0-No 1-Yes>"


def main(u, p, sw, ew, b):
    if b == 1:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
        driver = webdriver.Chrome()
    driver.get(harmony_url)
    assert "eHarmony" in driver.title
    # seconds
    delay = 30
    try:
        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "Div1")))
        login(driver, u, p)

        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "dailyReportingControlDiv")))
        attendance_button = driver.find_element_by_id("attendance")
        attendance_button.click()

        WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, "attendanceGridSelf_active_cell")))

        update_rows(driver, sw, ew)

        time.sleep(5)
        print("Harmony Updated !")
    except TimeoutException:
        print("Loading took too much time!")
    driver.close()
    print("END !")


def login(d, u, pwd):
    username_input = d.find_element_by_class_name("employeeNoNameInputText")
    username_input.clear()
    username_input.send_keys(u)

    password_input = d.find_element_by_name("password")
    password_input.clear()
    password_input.send_keys(pwd)
    password_input.send_keys(Keys.RETURN)


def update_rows(d, sw, ew):
    rows = d.find_elements_by_xpath("//*[@id='attendanceGridSelf']/div[2]/table/tbody/tr[*]")
    print(str(len(rows)))
    for i, row in enumerate(rows):
        array = []
        columns = row.find_elements_by_tag_name("td")
        if len(columns) == 14:
            images = row.find_elements_by_tag_name("img")
            add = True
            for image in images:
                url = image.get_attribute("src")
                if "green" in url or "calandar" in url:
                    add = False
            if add:
                print(str(i))
                array.append(row)
        for j, a in enumerate(array):
            a.find_element_by_class_name("Time_startAW").click()
            while len(d.find_elements_by_class_name("k-edit-cell")) == 0:
                a.find_element_by_class_name("Time_startAW").click()
            a.find_element_by_name("Time_startAW").send_keys(sw)

            a.find_element_by_class_name("Time_endAW").click()
            while len(d.find_elements_by_class_name("k-edit-cell")) == 0:
                a.find_element_by_class_name("Time_endAW").click()
            a.find_element_by_name("Time_endAW").send_keys(ew)

            a.find_element_by_class_name("check_row").click()
    save_button = d.find_element_by_id("actionSaveButton")
    save_button.click()


if 2 <= len(sys.argv) <= 5:
    username = sys.argv[1]
    password = keyring.get_password(windows_vault_service_name, username)
    if len(sys.argv) >= 3:
        start_work = sys.argv[2]
    else:
        start_work = default_start_work

    if len(sys.argv) >= 4:
        end_work = sys.argv[3]
    else:
        end_work = default_end_work

    if len(sys.argv) >= 5:
        background = sys.argv[4]
    else:
        background = default_background
    try:
        background = int(background)
        if background < 0 or background > 1:
            background = default_background
    except ValueError:
        background = default_background

    main(username, password, start_work, end_work, background)
else:
    if len(sys.argv) < 2:
        print("Missing args : " + cmd_format)
    else:
        print("Too many args : " + cmd_format)
