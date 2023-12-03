import time
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AddBlogTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000"  # Replace this with your base URL
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def test_add_blog_workflow(self):
        # Login
        self.login()

        # Navigate to artistprofile.html
        self.driver.get(self.base_url + '/artistprofile.html')

        # Wait for the "Add Blog" button to be present and clickable
        add_blog_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Add Blog')]"))
        )

        # Scroll to the element and click it using JavaScript
        self.scroll_to_element(add_blog_button)
        self.driver.execute_script("arguments[0].click();", add_blog_button)

        # Verify if redirected to http://127.0.0.1:8000/blogupload.html
        self.assertIn("http://127.0.0.1:8000/blogupload.html", self.driver.current_url)

        # Add a blog
        self.add_blog()

        # Verify if redirected to http://127.0.0.1:8000/blog.html after adding the blog
        self.assertIn("http://127.0.0.1:8000/blog.html", self.driver.current_url)

    def login(self):
        # Your login code here
        self.driver.get(self.base_url + '/accounts/login/')
        username = self.driver.find_element(By.NAME, 'username')
        password = self.driver.find_element(By.NAME, 'password')
        username.send_keys("anuanagha")  # Replace with a valid username
        password.send_keys("anuanagha@123")  # Replace with a valid password
        login_button = self.driver.find_element(By.XPATH, "//button[text()='Login']")
        login_button.click()

        # Assuming a successful login redirects to the home page
        # Check for the home page URL, handling the case where "http://127.0.0.1:8000/" might not be present
        self.assertIn("http://127.0.0.1:8000/", self.driver.current_url)

    def add_blog(self):
        # Fill in blog details
        title_input = self.driver.find_element(By.NAME, 'title')
        title_input.send_keys("Sample Blog Title")

        publishing_date_input = self.driver.find_element(By.NAME, 'publishingDate')
        publishing_date_input.send_keys("07-12-2023")  # Use the correct format, e.g., "YYYY-MM-DD"

        description_input = self.driver.find_element(By.NAME, 'description')
        description_input.send_keys("A wonderful blog about art.")

        # Upload a sample image (replace the file path with the path to your image)
        image_input = self.driver.find_element(By.NAME, 'image')
        image_input.send_keys(r"D:\djangoproject\art_p\media\blog_images\80.jpg")

        # Wait for the overlay to disappear
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.ID, "loading-spinner")))

        # Wait for the submit button to be clickable
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )

        # Scroll to the element and click it using JavaScript
        self.scroll_to_element(submit_button)
        self.driver.execute_script("arguments[0].click();", submit_button)

        # Wait for the redirect to blog.html
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be("http://127.0.0.1:8000/blog.html")
        )

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()


