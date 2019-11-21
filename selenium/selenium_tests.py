import unittest 
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class JerseyMarketTest(unittest.TestCase):

    def setUp(self):
        self.driver = None
        while self.driver is None:
            
            try:
                self.driver = webdriver.Remote(
                    command_executor='http://selenium-chrome:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.CHROME,
                )
            except:
                pass
            
    def test_python(self):
        driver = self.driver
        driver.get("https://www.python.org")
        self.assertIn("Python",driver.title)

    # Test for registerring:
    def test_log_in(self):
        driver = self.driver
        driver.get("http://web:8000")
        self.assertIn("Welcome to the Home Page",driver.page_source)
        # Navigate to register page
        print(driver.page_source)
        register_link = driver.find_element_by_id('register_button')
        register_link.click()

        # get form elements
        first_name = driver.find_element_by_id('id_first_name')
        last_name = driver.find_element_by_id('id_last_name')
        email = driver.find_element_by_id('id_email')
        password = driver.find_element_by_id('id_password')
        shirt_size = driver.find_element_by_id('id_shirt_size')
 
        # input info
        first_name.send_keys("Jane")
        last_name.send_keys("Doe")
        email.send_keys("JaneDoe@isa.com")
        password.send_keys("$3cureUS")
        shirt_size.click()
        driver.find_element_by_xpath('//*[@id="id_shirt_size"]/option[3]')

        # submit
        driver.find_element_by_xpath('/html/body/div[5]/div/div/form/input[6]').click()
        assert "Hi Jane!" in driver.page_source




    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    time.sleep(30)
    unittest.main()