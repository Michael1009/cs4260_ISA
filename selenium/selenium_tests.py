import unittest 
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class JerseyMarketTest(unittest.TestCase):

    def setUp(self):
        time.sleep(10)
        self.driver = webdriver.Remote(
            command_executor='http://selenium-chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
            )
    # Test for logging in:
    def test_log_in(self):
        driver = self.driver
        driver.get("http://web:8000")

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()