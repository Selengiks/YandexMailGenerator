import os
import shutil
import secrets
import loguru

from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from transliterate import translit
from datetime import datetime

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def login():  # Get login cookies from AppsFlyer
    driver.get("https://admin.yandex.ru/users?uid=1130000059899194")
    with open("login.txt", "r") as login_data:
        login = login_data.readline()
        password = login_data.readline()

    usernameField = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="passp-field-login"]')))
    usernameField.send_keys(login)
    try:
        driver.find_element(By.XPATH, '//*[@id="passp:sign-in"]').click()
    except:
        pass
    passwordField = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="passp-field-passwd"]')))
    passwordField.send_keys(password)
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


def create_account(firstname, lastname):
    addEmp = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/main/div[3]/div[2]/div/button')))
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
            (By.XPATH, '/html/body/div[6]/div[1]/div/div/button[2]')))
        print("agree click")
        agree.click()
    except:
        pass
    WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.XPATH, '/html/body/div[3]/div[1]/div/div')))

    with open("output.txt", "a") as res:
        res.write(f'Name: {firstname} {lastname}, Mail: {mail}, Pass: {password}\n')


state = True
datestamp = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
counter = 0
first_name = []
last_name = []
if os.path.exists("output.txt"):
    shutil.move("output.txt", f"history/output/{datestamp}.txt")
else:
    pass
while state:
    cycle = True
    mode = input('Запустить скрипт через консоль (введи 1), или через файл (введи 2)?\n')
    while cycle:
        if mode == "1":
            logger.info('По очереди вводи данные людей, которых хочесь создать, после введи next, чтобы продолжить\n')
            tmp1 = input('Введи имя пользователя')
            if tmp1 != "next":
                first_name.append(tmp1)
            elif tmp1 == "next":
                cycle = False
            else:
                logger.info("Дебил, тебе же сказали что и как вводить. Давай ещё раз.\n")
            tmp2 = input('Введи фамилию пользователя')
            if tmp2 != "next":
                last_name.append(tmp1)
            elif tmp2 == "next":
                cycle = False
            else:
                logger.info("Дебил, тебе же сказали что и как вводить. Давай ещё раз.\n")
        elif mode == "2":
            with open("input.txt", 'r', encoding='UTF-8') as file:
                while line := translit(file.readline().rstrip(), "ru", reversed=True):
                    counter += 1
                    first_name.append(line.split()[0])
                    last_name.append(line.split()[1])
                print("Total record is: " + str(counter))
        else:
            logger.info("Дебил, тебе же сказали что вводить. Давай ещё раз.\n")
    login()
    for t in range(counter):
        create_account(first_name[t], last_name[t])
    state = False
shutil.move("input.txt", f"history/input/{datestamp}.txt")
driver.close()
