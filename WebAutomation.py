from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from ExtractData import Value as facultyValue
from selenium.webdriver.support.ui import Select

test = facultyValue[1]
URL = "https://deerwalk.edu.np/sifalschool/login"

Credentials = {
    "email": "narendra.maden@sifal.deerwalk.edu.np",
    "password": "admin1234!",
}
delay = 5


def openBrowser():
    try:
        driver = webdriver.Chrome()
        profile = webdriver.ChromeOptions()
        profile.add_argument('--ignore-certificate-errors')
        return driver
    except Exception as e:
        print("error opening")
        exit(-1)


def findElement(browser, method, name):
    try:
        _elem = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((method, name)))
        return _elem
    except Exception as e:
        print("error: ", e)
        exit(-1)


def click(_elem):
    _elem.click()


def selectDropdown(browser, method, name):
    select = Select(findElement(browser, method, name))
    return select


def sendInput(browser, method, name, value):
    try:
        _elem = findElement(browser, method, name)
        click(_elem)
        _elem.send_keys(value)
        return _elem
    except Exception as e:
        print("error: ", e)
        exit(-1)


def login(browser):
    _input = sendInput(browser, By.NAME, 'email', Credentials['email'])
    _password = sendInput(browser, By.NAME, 'password',
                          Credentials['password'])
    _password.submit()


def facultyOperation(browser):
    _elem = findElement(browser, By.XPATH,
                        '//*[@id="app"]/div/div/div[2]/nav/div[7]/div/button')
    click(_elem)

    _addFaculty = findElement(
        browser, By.XPATH, '//*[@id="app"]/div/div/div[2]/nav/div[7]/div[3]/div/div/button[1]')
    click(_addFaculty)

    _ = sendInput(browser, By.NAME, 'name_en', test['name'])
    _ = sendInput(browser, By.NAME, 'description_en', test['description'])
    _ = sendInput(browser, By.NAME, 'name_np', test['nepali_name'])
    _ = sendInput(browser, By.NAME, 'description_np', test['description'])

    _facultyDropDown = findElement(browser, By.TAG_NAME, 'Option')
    click(_facultyDropDown)
    _faculties = browser.find_elements(By.TAG_NAME, value="Option")

    facultyFound = False
    for faculty in _faculties:
        if (faculty.text.replace(" ", "").lower() == test['department'].replace(" ", "").lower()):
            click(faculty)
            facultyFound = True
        else:
            continue
    if facultyFound == False:
        print("Faculty option you mentioned not found")


def start(URL, Credentials):
    browser = openBrowser()
    browser.get(URL)
    try:
        login(browser)
        facultyOperation(browser)
        sleep(5)
    except Exception as e:
        print("error: ", e)
        exit(-1)


x = start(URL, Credentials)
