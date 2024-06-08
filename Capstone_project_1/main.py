from dataPage import Data
from Element import element

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


class TestCase:
    def __init__(self):
        """
        Initializes the TestCase class with WebDriver and WebDriverWait instances.
        """
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 5)

    def start(self):
        """
        Navigates to the URL specified in Data.PageSource and waits until the URL is fully loaded.
        """
        self.driver.get(Data.PageSource().url)
        self.driver.maximize_window()
        self.wait.until(EC.url_to_be(Data.PageSource().url))

    def close(self):
        """
        Quits the WebDriver instance.
        """
        self.driver.quit()

    def login(self, username, password):
        """
        Attempts to log in using the provided username and password.
        """
        try:
            self.start()
            self.wait.until(EC.visibility_of_element_located((By.NAME,
                                                              element.PageElement().Username))).send_keys(username)
            self.wait.until(EC.visibility_of_element_located((By.NAME,
                                                              element.PageElement().Password))).send_keys(password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                        element.PageElement().login_button))).click()
            self.wait.until(EC.url_to_be(Data.PageSource().LoginUrl))
            print("The user is logged in successfully")
        except TimeoutException:
            print("Invalid Credentials")
        except Exception as e:
            print(f"An error occurred during login: {e}")

    def logout(self):
        """
        Logs out from the application by clicking on the user menu and then the logout button.
        """
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().userMenu))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().logout))).click()
        except NoSuchElementException as e:
            print("Error during logout:", e)
        except Exception as e:
            print(f"An error occurred during logout: {e}")

    def test_case_01(self):
        """
        Executes a test case to log in using valid credentials.
        """
        username = "Admin"
        password = "admin123"
        try:
            self.login(username, password)
            self.wait.until(EC.url_changes(Data.PageSource().url))
        except NoSuchElementException as e:
            print("Error in logging in:", e)
        except Exception as e:
            print(f"An error occurred in test_case_01: {e}")
        finally:
            self.logout()

    def test_case_02(self):
        """
        Executes a test case to log in using invalid credentials.
        """
        username = "Admin"
        password = "Invalid Credentials"
        try:
            self.login(username, password)
            self.wait.until(EC.url_changes(Data.PageSource().url))
        except NoSuchElementException as e:
            print("Error in logging in:", e)
        except Exception as e:
            print(f"An error occurred in test_case_02: {e}")
        finally:
            self.logout()

    def test_case_pim01(self):
        """
        Executes a test case to add a new employee by entering their details.
        """
        username = "Admin"
        password = "admin123"
        try:
            self.login(username, password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().PIMMenu))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().addEmployee))).click()
            self.wait.until(EC.element_to_be_clickable((By.NAME, element.PageElement().FirstName))).send_keys("Robert")
            self.wait.until(EC.element_to_be_clickable((By.NAME, element.PageElement().MiddleName))).send_keys("Downey")
            self.wait.until(EC.element_to_be_clickable((By.NAME, element.PageElement().LastName))).send_keys("Junior")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().empId))).send_keys("1986")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().Add_save))).click()
            success_message = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                                element.PageElement().Message)))
            print(f"Success message: {success_message.text}")
            self.wait.until(EC.url_changes(Data.PageSource().AddEmployee_Url))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().dashboard))).click()
            print("Successfully added employee")
        except NoSuchElementException as e:
            print("Error in employee addition:", e)
        except Exception as e:
            print(f"An error occurred in test_case_pim01: {e}")
        finally:
            self.logout()

    def test_case_pim02(self):
        """
        Executes a test case to edit an existing employee's details.
        """
        username = "Admin"
        password = "admin123"
        try:
            self.login(username, password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().PIMMenu))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().edit))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().EmpID))).send_keys("1212")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().Other_ID))).send_keys("2121")
            dl = self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().Driving_license)))
            dl.clear()
            dl.send_keys("0124533")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().edit_save))).click()
            success_message = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                                element.PageElement().edit_message)))
            print(f"Success message: {success_message.text}")
            self.wait.until(EC.url_changes(Data.PageSource().url))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().dashboard))).click()
            print("Successfully edited employee details")
        except NoSuchElementException as e:
            print("Error in employee detail addition:", e)
        except Exception as e:
            print(f"An error occurred in test_case_pim02: {e}")
        finally:
            self.logout()

    def test_case_pim03(self):
        """
        Executes a test case to delete an existing employee's details.
        """
        username = "Admin"
        password = "admin123"
        try:
            self.login(username, password)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().PIMMenu))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().delete))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, element.PageElement().yes))).click()
            success_message = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                                element.PageElement().delete_message)))
            print(f"Success message: {success_message.text}")
            self.wait.until(EC.url_changes(Data.PageSource().url))
            print("Successfully deleted employee")
        except NoSuchElementException as e:
            print("Error in deletion:", e)
        except Exception as e:
            print(f"An error occurred in test_case_pim03: {e}")
        finally:
            self.logout()
            self.close()


# Create an instance of TestCase and execute the test cases
if __name__ == "__main__":
    obj = TestCase()
    obj.test_case_01()
    obj.test_case_02()
    obj.test_case_pim01()
    obj.test_case_pim02()
    obj.test_case_pim03()
