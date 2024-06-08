# Access the variables used or maintained by the Python
# Functions that interact strongly with the interpreter.
import sys
# Module provides a way of using operating system-dependent
# Functionality like reading or writing to the file system
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from dataPage import Data
from Element import element

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import pytest


class TestOrangeHRM:
    @pytest.fixture
    def boot(self, request):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 5)
        self.driver.maximize_window()
        request.cls.driver = self.driver
        request.cls.wait = self.wait
        yield
        self.driver.quit()

    def login(self, username, password):
        """
        Attempts to log in using the provided username and password.
        """
        try:
            page_element = element.PageElement()
            self.wait.until(EC.visibility_of_element_located((By.NAME, page_element.Username))).send_keys(username)
            self.wait.until(EC.visibility_of_element_located((By.NAME, page_element.Password))).send_keys(password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, page_element.login_button))).click()
            self.wait.until(EC.url_to_be(Data.PageSource().LoginUrl))
            print("The user is logged in successfully")
        except Exception as e:
            print(f"An error occurred during login: {e}")

    def logout(self):
        """
        Logs out from the application by clicking on the user menu and then the logout button.
        """
        try:
            page_element = element.PageElement()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, page_element.userMenu))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, page_element.logout))).click()
        except Exception as e:
            print(f"An error occurred during logout: {e}")

    @pytest.mark.usefixtures("boot")
    def test_case_01(self, request):
        page_source = Data.PageSource()
        self.driver.get(page_source.url)

        username = "Admin"
        password = "admin123"
        self.login(username, password)
        assert self.driver.current_url == page_source.LoginUrl
        print("SUCCESS: Logged in with Admin and the password is admin123")
        self.logout()
        request.node.user_properties.append(("custom_message", "Logged in with Admin and the password is admin123"))

    @pytest.mark.usefixtures("boot")
    def test_case_02(self, request):
        page_source = Data.PageSource()
        self.driver.get(page_source.url)

        username = "Admin"
        password = "Invalid Credentials"
        self.login(username, password)
        assert self.driver.current_url == page_source.url
        print("SUCCESS: Invalid credentials with username - Admin and the password is Invalid Credentials")
        request.node.user_properties.append(
            ("custom_message", "Invalid credentials with username - Admin and the password is Invalid Credentials"))

    @pytest.mark.usefixtures("boot")
    def test_case_pim01(self, request):
        page_source = Data.PageSource()
        page_element = element.PageElement()
        self.driver.get(page_source.url)
        try:
            username = "Admin"
            password = "admin123"
            self.login(username, password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, page_element.PIMMenu))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, page_element.addEmployee))).click()
            self.wait.until(EC.visibility_of_element_located((By.NAME, page_element.FirstName))).send_keys("Robert")
            self.wait.until(EC.visibility_of_element_located((By.NAME, page_element.MiddleName))).send_keys("Downey")
            self.wait.until(EC.visibility_of_element_located((By.NAME, page_element.LastName))).send_keys("Junior")
            self.wait.until(EC.visibility_of_element_located((By.XPATH, page_element.empId))).send_keys("1986")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, page_element.Add_save))).click()
            success_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, page_element.Message)))
            assert "Successfully Saved" in success_message.text, "Employee addition failed"
            request.node.user_properties.append(("custom_message", f"Success message: {success_message.text}"))
        except Exception as e:
            print(f"Test failed: {e}")
        finally:
            self.logout()

    @pytest.mark.usefixtures("boot")
    def test_case_pim02(self, request):
        page_source = Data.PageSource()
        page_element = element.PageElement()
        self.driver.get(page_source.url)
        try:
            username = "Admin"
            password = "admin123"
            self.login(username, password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, page_element.PIMMenu))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, page_element.addEmployee))).click()
            self.wait.until(EC.visibility_of_element_located((By.NAME, page_element.FirstName))).send_keys("Robert")
            self.wait.until(EC.visibility_of_element_located((By.NAME, page_element.MiddleName))).send_keys("Downey")
            self.wait.until(EC.visibility_of_element_located((By.NAME, page_element.LastName))).send_keys("Junior")
            self.wait.until(EC.visibility_of_element_located((By.XPATH, page_element.empId))).send_keys("1986")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, page_element.Add_save))).click()
            success_message = self.wait.until(EC.visibility_of_element_located((By.XPATH, page_element.Message)))
            assert "Successfully Saved" in success_message.text, "Employee addition failed"
            request.node.user_properties.append(("custom_message", f"Success message: {success_message.text}"))
        except Exception as e:
            print(f"Test failed: {e}")
        finally:
            self.logout()

    @pytest.mark.usefixtures("boot")
    def test_case_pim03(self, request):
        page_source = Data.PageSource()
        self.driver.get(page_source.url)
        try:
            username = "Admin"
            password = "admin123"
            self.login(username, password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().PIMMenu))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().delete))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().yes))).click()
            success_message = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, element.PageElement().delete_message)))
            print(f"Success message: {success_message.text}")
            self.wait.until(EC.url_changes(Data.PageSource().url))
            assert "Successfully Deleted" in success_message.text, "Employee deletion"
            request.node.user_properties.append(("custom_message", f"Success message: {success_message.text}"))
            print("Successfully deleted employee")
        except NoSuchElementException as e:
            print("Error in deletion:", e)
        except Exception as e:
            print(f"An error occurred in test_case_pim03: {e}")
        finally:
            self.logout()
