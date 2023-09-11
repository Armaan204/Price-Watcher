import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create a Chrome WebDriver instance
driver = webdriver.Chrome()

product_url = 'your-amazon-link'

# Define the target price you want to track
target_price = 0 # Set it to your your-target-price

# Gmail email and password (use an app password if you have two-factor authentication enabled)
email_sender = 'your-email-address'
email_password = 'your-passkey'
email_receiver = 'your-email-address'

# Function to extract the current price from the Amazon product page
def get_current_price():
    driver.get(product_url)
    try:
        # Wait for the price element to become available (maximum wait time: 30 seconds)
        price_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'a-price-whole'))
        )
        price = price_element.text
        return float(price.replace('$', '').replace(',', ''))  # Convert price to a float
    except Exception as e:
        print(f"Failed to get price: {str(e)}")
        return None

# Function to send an email notification
def send_email(subject, body):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, email_password)

        # Create the email message
        message = MIMEMultipart()
        message['From'] = email_sender
        message['To'] = email_receiver
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(email_sender, email_receiver, message.as_string())
        server.quit()
        print('Email notification sent successfully.')
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Main tracking loop
while True:
    current_price = get_current_price()
    if current_price is not None:
        print(f'Current Price: ${current_price:.2f}')
        if current_price < target_price:
            message_subject = 'Price Alert'
            message_body = f'The price is below your target price of ${target_price:.2f}.'
            send_email(message_subject, message_body)
            break  # Exit the loop if the price is below the target
        elif current_price > target_price:
            print('The price is higher than your target price. Retrying in 2 hours.')
            time.sleep(7200)  # Sleep for 2 hours before checking again
        else:
            print('The price matches your target price. Retrying in 2 hours.')
            time.sleep(7200)  # Sleep for 2 hours before checking again
    else:
        print('Price not found. Retrying in 1 hour.')
        time.sleep(3600)  # Sleep for 1 hour before checking again

# Close the WebDriver
driver.quit()
