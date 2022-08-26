import os
import shutil
import secrets

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from transliterate import translit
from datetime import datetime


def create_account(firstname, lastname):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://admin.yandex.ru/users?uid=1130000059899194")
    with open("login.txt", "r") as login_data:
        login = login_data.readline()
        passw = login_data.readline()

    usernameField = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="passp-field-login"]')))
    usernameField.send_keys(login)
    driver.find_element(By.XPATH, '//*[@id="passp:sign-in"]').click()
    passwordField = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="passp-field-passwd"]')))
    passwordField.send_keys(passw)
    driver.find_element(By.XPATH, '//*[@id="passp:sign-in"]').click()
    try:
        notNowbtn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/form/div[3]/button')))
        notNowbtn.click()
    except:
        pass

    checkOrg = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/main/div/div/div[1]')))
    checkOrg.click()
    addEmp = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/main/div[3]/div[2]/div/button[2]')))
    addEmp.click()

    driver.find_element(By.XPATH, '//*[@name="first_name"]').send_keys(firstname)
    driver.find_element(By.XPATH, '//*[@name="last_name"]').send_keys(lastname)
    nickname = str(firstname).lower() + '.' + str(lastname).lower()
    driver.find_element(By.XPATH, '//*[@name="nickname"]').send_keys(nickname)
    mail = nickname + "@traffbraza.com"
    password = secrets.token_urlsafe(12)
    driver.find_element(By.XPATH, '//*[@name="password_field_1"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@name="password_field_2"]').send_keys(password)

    driver.find_element(By.XPATH, '//*[@type="submit"]').click()
    #################################################################################
    try:
        agree = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'Button2 Button2_size_xl Button2_view_action _2RKFk2rFL9R7k8jYhOaglv')))
        print("agree click")
        agree.click()
    except:
        pass
    WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.XPATH, '/html/body/div[3]/div[1]/div/div')))

    with open("output.txt", "a") as res:
        res.write(f'Name: {firstname} {lastname}, Mail: {mail}, Pass: {password}\n')

    driver.close()


datestamp = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
counter = 0
first_name = []
last_name = []

if os.path.exists("output.txt"):
    shutil.move("output.txt", f"history/output/{datestamp}.txt")
else:
    pass

with open("input.txt", 'r', encoding='UTF-8') as file:
    while line := translit(file.readline().rstrip(), "ru", reversed=True):
        counter += 1
        first_name.append(line.split()[0])
        last_name.append(line.split()[1])
    print("Total record is: " + str(counter))

# shutil.move("input.txt", f"history/input/{datestamp}.txt")

for t in range(counter):
    create_account(first_name[t], last_name[t])
