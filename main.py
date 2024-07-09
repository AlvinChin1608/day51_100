import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv("./vars/.env")

YOUR_EMAIL = os.getenv("X_EMAIL")
YOUR_PASSWORD = os.getenv("X_PASS")
PROMISED_DOWN = 100
PROMISED_UP = 30


class InternetSpeedTwitterBot:
    def __init__(self):
        # No need to download Chromedriver anymore! Selenium will download automatically
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)  # Option to keep Chrome open
        self.driver = webdriver.Chrome(options=options)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        """My aging computer takes about a minute initial the clicks."""
        self.print_message("Loading Speedtest... This might take a minute.")
        self.driver.get("https://www.speedtest.net/")

        # Handle the "Continue" button if it appears
        try:
            # wait until the button is clickable
            continue_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            continue_button.click()
        except Exception as e:
            print("Continue button not found or already clicked:", e)

        # Click the Go button
        go_button = self.driver.find_element(By.CSS_SELECTOR, ".start-button a")
        go_button.click()

        # Start the countdown timer while waiting for the results to load
        self.print_message("Waiting for the speed test to complete...")
        self.countdown_timer(29)  # Adjust the countdown time as needed
        time.sleep(1)
        WebDriverWait(self.driver, 70).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".download-speed"))
        )

        # Get download and upload speeds
        self.down = self.driver.find_element(By.CSS_SELECTOR, ".download-speed").text
        self.up = self.driver.find_element(By.CSS_SELECTOR, ".upload-speed").text
        print(f"Download speed: {self.down} Mbps\n Upload speed: {self.up} Mbps")

    def countdown_timer(self, seconds):
        """
        Displays a countdown timer.
        """
        while seconds > 0:
            # Clear the previous line with carriage return and backspace
            print("\r", end="")
            # Update the remaining time in the message
            print(f"Time remaining for speed test result: {seconds} seconds", end="")
            time.sleep(2)
            seconds -= 1
        print("\nSpeed test completed!")

    def print_message(self, message):
        """Simple print function to avoid issues with selenium printing"""
        print(message)
    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/login")

        # wait until fully loaded then insert email
        email = WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )

        email.send_keys(YOUR_EMAIL, Keys.RETURN)
        time.sleep(5)
        password = self.driver.find_element(By.NAME, "password")
        password.send_keys(YOUR_PASSWORD, Keys.RETURN)

        time.sleep(2)
        password.send_keys(Keys.ENTER)

        time.sleep(15)

        # Compose the tweet
        """Issue: I have some issue composing the tweet. XPATH, CSS selection not working.. 
        If you're seeing my code, and know how to fix please leave a comment. Thanks
        """
        message = f"Ignore. This is an internet speed report bot. Download Speed: {self.down} Mbps, Upload Speed: {self.up} Mbps."

        try:
            tweet_compose = WebDriverWait(self.driver, 40).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Tweet text"]'))
            )
            tweet_compose.click()
            time.sleep(1)
            tweet_compose.send_keys(message)
            time.sleep(3)

            tweet_button = self.driver.find_element(By.XPATH, '//div[@data-testid="tweetButtonInline"]')
            tweet_button.click()
        except Exception as e:
            print(f"Error while composing tweet: {e}")


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()
