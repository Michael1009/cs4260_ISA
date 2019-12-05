import unittest 
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests


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
            
    # Test for registerring:
    def test_create_accounts(self):
        driver = self.driver
        driver.get("http://web:8000")
        self.assertIn("Welcome to the Home Page",driver.page_source)
        # Navigate to register page
        driver.find_element_by_id('register_button').click()

        # get form elements
        time.sleep(1)
        driver.find_element_by_id('id_first_name').send_keys('Jane')
        time.sleep(1)
        driver.find_element_by_id('id_last_name').send_keys('Doe')
        time.sleep(1)
        driver.find_element_by_id('id_email').send_keys('JaneDoe@isa.com')
        time.sleep(1)
        driver.find_element_by_id('id_password').send_keys('$3cureUS')
        time.sleep(1)
        driver.find_element_by_id('id_shirt_size').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="id_shirt_size"]/option[3]').click()
        time.sleep(1)

        # submit
        driver.find_element_by_xpath('/html/body/div[5]/div/div/form/input[6]').click()
        time.sleep(1)
        self.assertIn("Hello Jane!",driver.page_source)

    def test_log_in_log_out(self):
        driver = self.driver
        driver.get("http://web:8000")

        # navigate to log in
        driver.find_element_by_xpath('//*[@id="login_button"]').click()
        time.sleep(1)
        # get form elements
        driver.find_element_by_id('id_email').send_keys('JaneDoe@isa.com')
        time.sleep(1)
        driver.find_element_by_id('id_password').send_keys('$3cureUS')
        time.sleep(1)


        # submit
        driver.find_element_by_xpath('/html/body/div[5]/div/div/form/input[4]').click()
        time.sleep(1)
        self.assertIn("Hello Jane!",driver.page_source)

        #navigate to log out
        driver.find_element_by_xpath('/html/body/div[2]/a').click()
        self.assertNotIn("Hello Jane!",driver.page_source)

    def test_log_in_create_item(self):
        driver = self.driver
        driver.get("http://web:8000")

        # navigate to log in
        driver.find_element_by_xpath('//*[@id="login_button"]').click()
        time.sleep(1)
        # get form elements
        driver.find_element_by_id('id_email').send_keys('JaneDoe@isa.com')
        time.sleep(1)
        driver.find_element_by_id('id_password').send_keys('$3cureUS')
        time.sleep(1)
        # submit
        driver.find_element_by_xpath('/html/body/div[5]/div/div/form/input[4]').click()
        time.sleep(1)
        self.assertIn("Hello Jane!",driver.page_source)

        driver.find_element_by_xpath('/html/body/div[3]/a').click()
        time.sleep(1)

        driver.find_element_by_id('id_team').send_keys('Leicester City')
        time.sleep(1)
        driver.find_element_by_id('id_number').send_keys('7')
        time.sleep(1)
        driver.find_element_by_id('id_player').send_keys('Jamie Vardy')
        time.sleep(1)
        driver.find_element_by_id('id_primary_color').send_keys('blue')
        time.sleep(1)
        driver.find_element_by_id('id_secondary_color').send_keys('white')
        time.sleep(1)

        driver.find_element_by_xpath('/html/body/div[5]/div/div/form/input[7]').click()
        time.sleep(1)

        self.assertIn("Jamie Vardy",driver.page_source)


    def test_search(self):
        driver = self.driver
        driver.get("http://web:8000")

        # navigate to log in
        driver.find_element_by_xpath('//*[@id="login_button"]').click()
        time.sleep(1)
        # get form elements
        driver.find_element_by_id('id_email').send_keys('JaneDoe@isa.com')
        time.sleep(1)
        driver.find_element_by_id('id_password').send_keys('$3cureUS')
        time.sleep(1)
        # submit
        driver.find_element_by_xpath('/html/body/div[5]/div/div/form/input[4]').click()
        time.sleep(1)
        self.assertIn("Hello Jane!",driver.page_source)

        driver.find_element_by_xpath('/html/body/div[4]/div/form/input').send_keys('Jamie', Keys.ENTER)
        time.sleep(5)
        self.assertIn("Jamie",driver.page_source)

        # This will call a microservice that deletes the created jersey and the created user. I just have this run at the end of the last test
        # Probably not the best way of doing this but I unfortunately don't care enought to do anything about it
        url = "http://models:8000/jersey/api/v1/User/JaneDoe@isa.com/delete_user_by_email"
        requests.delete(url)



        
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    print("main method")
    unittest.main()