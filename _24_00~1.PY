from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

# constants:
email = "YOUR_EMAIL"

# function to log messages:
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{timestamp} - {message}")

def init_driver():
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    log_message("webdriver initialized.")
    return driver

def click_element(driver, by, value, description):
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value)))
        element.click()
        log_message(f"{description} clicked successfully.")
        return True
    except TimeoutException:
        log_message(f"{description} not clickable or not found.")
        return False


from selenium.webdriver.common.action_chains import ActionChains

def enter_email_at_cursor(driver, email):
    try:
        active_element = driver.switch_to.active_element
        actions = ActionChains(driver)
        actions.move_to_element(active_element).click().send_keys(email).send_keys(Keys.ENTER).perform()
        log_message(f"Text '{email}' entered at cursor position.")
    except Exception as e:
        log_message(f"Failed to enter text: {e}")


def login_sequence(driver):
    # Click decline button
    click_element(driver, By.XPATH, "//div[contains(text(), 'I decline')]", "decline button")

    # Click main login button
    if click_element(driver, By.CLASS_NAME, "l17p5q9z", "main login button"):
        # Select English language
        if click_element(driver, By.XPATH, "//span[contains(text(), 'English')]", "english language option"):
            # Click additional login button if present
            click_element(driver, By.CSS_SELECTOR, "a[href*='tinder.onelink.me'] div.l17p5q9z", "additional login button")

            # Continue with Google login attempt
            if click_element(driver, By.CSS_SELECTOR, "span.nsm7Bb-HzV7m-LgbsSe-BPrWId", "continue with google button"):
                enter_email_at_cursor(driver, email)  # Pass email to function

def main():
    driver = init_driver()
    driver.get("https://tinder.com/")
    log_message("navigated to tinder's login page.")

    login_sequence(driver)

    input("press enter to exit...\n")
    driver.quit()

if __name__ == "__main__":
    main()
