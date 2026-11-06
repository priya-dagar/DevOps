"""Selenium automated browser test for the Lab 3 app (Q6)."""
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5004"
SHOT = "/home/abhinav/devops-lab-3/docs/screenshots/q6-selenium-beta-page.png"

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
try:
    # 1) health endpoint returns UP
    driver.get(BASE_URL + "/health")
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "UP")
    )
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "UP" in body and "status" in body, f"unexpected health body: {body}"
    print("PASS  /health returned:", body)

    # 2) beta feature flag is enabled on this instance
    driver.get(BASE_URL + "/beta")
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "beta")
    )
    body = driver.find_element(By.TAG_NAME, "body").text
    assert '"enabled":true' in body, f"beta flag not enabled: {body}"
    print("PASS  /beta flag enabled:", body)

    driver.save_screenshot(SHOT)
    print("PASS  screenshot saved:", SHOT)
finally:
    driver.quit()
