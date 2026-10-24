
import os
import unittest
from urllib.request import urlopen
from urllib.error import URLError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = os.getenv("BASE_URL", "http://localhost:8081")


class PortfolioTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        remote_url = os.getenv("SELENIUM_REMOTE_URL")
        
        if remote_url:
            cls.driver = webdriver.Remote(
            command_executor=remote_url,
            options=options
            )
        else:
            cls.driver = webdriver.Chrome(options=options)
            
        cls.driver.set_page_load_timeout(20)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_homepage_loads(self):
        self.driver.get(BASE_URL)

        self.assertIn("Sravan", self.driver.title)
        self.assertTrue(
            self.driver.find_element(By.ID, "home").is_displayed()
        )

    def test_required_sections_exist(self):
        self.driver.get(BASE_URL)

        for section in ["about", "skills", "projects", "contact"]:
            with self.subTest(section=section):
                self.assertTrue(
                    self.driver.find_element(By.ID, section).is_displayed()
                )

    def test_project_heading(self):
        self.driver.get(BASE_URL)

        projects = self.driver.find_element(By.ID, "projects")
        self.assertIn("Featured Projects", projects.text)

    def test_navigation_links(self):
        self.driver.get(BASE_URL)

        links = self.driver.find_elements(
            By.CSS_SELECTOR, ".nav-links a"
        )
        self.assertGreaterEqual(len(links), 5)

        for link in links:
            self.assertTrue(link.get_attribute("href").endswith(
                "#" + link.text.lower()
            ))


if __name__ == "__main__":
    unittest.main(verbosity=2)
