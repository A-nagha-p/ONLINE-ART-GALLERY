from django.test import TestCase
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AdminAuctionTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000"  # Replace this with your base URL
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test_admin_start_auction(self):
        # Open the login page
        self.driver.get(self.base_url + '/accounts/login/')

        # Check if the login page is accessible
        self.assertIn("/accounts/login/", self.driver.current_url)

        # Enter login credentials and click on login button
        username = self.driver.find_element(By.NAME, 'username')
        password = self.driver.find_element(By.NAME, 'password')
        username.send_keys("admin")  # Replace with the correct username
        password.send_keys("admin123")  # Replace with the correct password

        login_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")
        login_button.click()

        # Wait for the login process to complete and redirect to admin dashboard
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/admindash.html")
        )

        # Click on the "Start Auction" link on the left side dashboard
        try:
            start_auction_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'adminauction.html')]"))
            )
            start_auction_link.click()
        except TimeoutException:
            self.fail("Start Auction link not found or clickable.")

        # Wait for the adminauction.html page to load
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be(self.base_url + '/adminauction.html')
        )

        # Select the auction start date and end date (example)
        start_date_input = self.driver.find_element(By.NAME, 'auction_start_datetime')
        start_date_input.send_keys('2024-04-10T08:00')  # Replace with the desired start date and time

        end_date_input = self.driver.find_element(By.NAME, 'auction_end_datetime')
        end_date_input.send_keys('2024-04-20T18:00')  # Replace with the desired end date and time

        # Click on the submit button
        submit_button = self.driver.find_element(By.XPATH, "//button[text()='Submit']")
        submit_button.click()

        # Optionally, you can add assertions to verify the success of the auction creation process
        # For example, you can check for a success message or verify the redirection to another page.

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
