import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from ExtractData import Value as facultyValue
from selenium.webdriver.support.ui import Select


Credentials = {
    "email": "narendra.maden@sifal.deerwalk.edu.np",
    "password": "admin1234!",
}


class Automate:
    def __init__(self, browser, url, delay=3):
        self.browser = browser
        self.delay = delay
        self.url = url

    def start(self):
        try:
            self.browser.get(self.url)
            # work
            self.login()
            self.facultyOperation()
        except Exception as e:
            print("Error Opening: ", e)
            exit(-1)

    # find element until specified delay
    def _findElement(self, method, name):
        try:
            _elem = WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((method, name))
            )
            return _elem
        except Exception as e:
            print("Error: ", e)
            exit(-1)

    # click an element

    def _click(self, _elem):
        _elem.click()

    # send input to element (key value example: sends username value to username input)
    def _sendInput(self, method, name, value):
        try:
            _elem = self._findElement(method, name)
            self._click(_elem)
            _elem.send_keys(value)

            return _elem

        except Exception as e:
            print("Error: ", e)
            exit(-1)

    def _checkFacultyExistsOrNot(self):
        existing_names = []
        updateIds = []
        insertIds = []
        _elem = self._findElement(
            By.XPATH,
            '//*[@id="app"]/div/div/div[2]/nav/div[7]/div/button'
        )
        self._click(_elem)
        _allFaculty = self._findElement(
            By.XPATH,
            '//*[@id="app"]/div/div/div[2]/nav/div[7]/div[3]/div/div/button[2]'
        )
        self._click(_allFaculty)

        _table = self._findElement(
            By.XPATH,
            '//*[@id="app"]/div/div/div[3]/main/div[2]/div/div/div/table/tbody'
        )
        _tableRows = _table.find_elements(By.TAG_NAME, "tr")
        # extracting name
        for row in _tableRows:
            col = row.find_elements(By.TAG_NAME, "td")
            name = col[0].text
            existing_names.append(name)

        # extracting ids for already existing data
        updated = False
        for faculty in facultyValue:
            for name in existing_names:
                if name.replace(" ", "").lower() == facultyValue[faculty]['name'].replace(" ", "").lower():
                    updateIds.append(faculty)
                    updated = True
            if updated == False:
                insertIds.append(faculty)
            updated = False

        return insertIds, updateIds

    def login(self):
        _input = self._sendInput(By.NAME, 'email', Credentials['email'])
        _password = self._sendInput(
            By.NAME, 'password', Credentials['password'])

        _password.submit()

    def facultyOperation(self):
        # extracting update and insert ids
        updateIds, insertIds = self._checkFacultyExistsOrNot()
        print(updateIds, insertIds)
        _elem = self._findElement(
            By.XPATH, '//*[@id="app"]/div/div/div[2]/nav/div[7]/div/button')
        self._click(_elem)

        _addFaculty = self._findElement(
            By.XPATH,
            '//*[@id="app"]/div/div/div[2]/nav/div[7]/div[3]/div/div/button[1]'
        )
        self._click(_addFaculty)

        # inserting values
        _ = self._sendInput(By.NAME, 'name_en', test['name'])
        _ = self._sendInput(By.NAME, 'description_en', test['description'])
        _ = self._sendInput(By.NAME, 'name_np', test['nepali_name'])
        _ = self._sendInput(By.NAME, 'description_np', test['description'])

        # drop down values
        _facultyDropDown = self._findElement(By.TAG_NAME, "Option")
        _faculties = self.browser.find_elements(By.TAG_NAME, value="Option")

        facultyFound = False

        for faculty in _faculties:
            if (faculty.text.replace(" ", "").lower() == test['department'].replace(" ", "").lower()):
                self._click(faculty)
                facultyFound = True
            else:
                continue

        if facultyFound == False:
            print("Faculty option you mentioned not found")
        facultyFound = False


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
URL = "https://deerwalk.edu.np/sifalschool/login"
test = facultyValue[1]


automate = Automate(driver, URL, 5)
automate.start()

time.sleep(5)
