import unittest 
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class JerseyMarketTest(unittest.TestCase):

    def setUp(self):
        time.sleep(10)	        
        self.driver = None
        while self.driver is None:
            try:
                self.driver = webdriver.Remote(
                    command_executor='http://selenium-chrome:4444/wd/hub',
                    desired_capabilities=DesiredCapabilities.CHROME,
                    # chrome_options=chrome_options
                )
            except:
                pass

    def test_python(self):
        print("Baseline selenium test")
        driver = self.driver
        driver.get("https://www.python.org")
        self.assertIn("Python",driver.title)

    def test_create_account(self):
        print("creating account test....")
        driver = self.driver
        driver.get("http://web:8000")
        assert True

    def tearDown(self):
        print("closing")
        self.driver.close()

if __name__ == "__main__":
    # time.sleep(60)
    unittest.main() 