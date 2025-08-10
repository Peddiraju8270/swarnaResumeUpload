import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def test_Naukri_update():
    # Chrome options
    options = Options()

    # Detect if running in GitHub Actions (headless mode)
    if os.getenv("GITHUB_ACTIONS") == "true":
        print("Running in GitHub Actions → enabling headless mode")
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
    else:
        options.add_argument("--start-maximized")

    # Create Chrome driver (auto-downloads correct version)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Go to Naukri login page
        driver.get('https://www.naukri.com/nlogin/login')

        # Login
        username_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, 'usernameField'))
        )
        username_field.send_keys('priyaswarna369@gmail.com')

        password_field = driver.find_element(By.ID, 'passwordField')
        password_field.send_keys("Google@1234")

        login_button = driver.find_element(By.XPATH, '//button[text()="Login"]')
        login_button.click()

        # Wait for login success
        WebDriverWait(driver, 20).until(
            EC.url_contains('mnjuser/homepage')
        )

        # Navigate to profile page
        driver.get('https://www.naukri.com/mnjuser/profile?id=&orgn=homepage')

        # Check if resume is already uploaded
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Swarna Priya 6.9Years of exp.pdf')]"))
            )
            print("Resume already present. Deleting...")
            delete_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//i[@title='Click here to delete your resume']"))
            )
            delete_icon.click()
            # Wait for confirmation dialog and click Delete
            confirm_delete_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='lightbox model_open flipOpen']//button[@class='btn-dark-ot'][normalize-space()='Delete']"))
            )
            confirm_delete_btn.click()
            time.sleep(2)
        except:
            print("No existing resume found. Proceeding to upload...")

        # Click Update Resume button if present
        try:
            update_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//em[text()='Update resume'] | //button[contains(text(),'Update Resume')]"))
            )
            update_button.click()
            time.sleep(2)
        except:
            print("⚠ Update Resume button not found, proceeding to file input...")

        # Switch to iframe if needed
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        file_input = None
        for frame in iframes:
            driver.switch_to.frame(frame)
            try:
                file_input = driver.find_element(By.XPATH, "//input[@type='file']")
                if file_input.is_displayed():
                    break
            except:
                driver.switch_to.default_content()

        if not file_input:
            driver.switch_to.default_content()
            file_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", file_input)

        # Resume path
        resume_path = os.path.abspath(
            r"C:\Users\ASUS\OneDrive\Documents\test\naukri_auto_upload-main\Swarna Priya 6.9Years of exp.pdf"
        )
        file_input.send_keys(resume_path)

        # Wait for success message
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Resume uploaded successfully')]"))
        )

        print("✅ Resume updated successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
    finally:
        driver.quit()


if __name__ == "__main__":
    test_Naukri_update()
