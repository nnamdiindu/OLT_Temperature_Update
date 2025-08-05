import os
import smtplib
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
ip_addresses = ["http://10.0.04.142/", "http://10.0.4.90/", "http://10.0.4.103/", "http://10.0.4.40/", "http://10.0.4.44/", "http://10.0.4.43/", "http://10.0.4.60/"]
olt_locations = ["LOS-SUNSHINEESTATE-FD1700S-001", "LOS-IKONECTT-SUNSHINEESTATE-001", "LOS-UNITYHOMESESTATE-FD1700S-002",
            "LOS-UNITYHOMESESTATE-FD1700S-001", "LOSCEDARCOUNTY-OLT-FD1700S-001", "LOSCEDARCOUNTY-OLT-FD1700S-002", "LOS-IKONECTT-AVERA-OLT-FD1700S-001"]
count = 0
for ip_address in ip_addresses:
    driver.get(f"{ip_address}")

    time.sleep(3)
    username = driver.find_element(By.XPATH, value="/html/body/div/div[2]/div[2]/div/div[2]/div[1]/input")
    username.send_keys(os.environ.get("USER"))

    password = driver.find_element(By.XPATH,value="/html/body/div/div[2]/div[2]/div/div[2]/div[2]/input")
    password.send_keys(os.environ.get("PASSWORD_"))

    login_button = driver.find_element(By.XPATH,value="/html/body/div/div[2]/div[2]/div/div[2]/div[3]/button")
    login_button.click()

    time.sleep(3)
    temperature_div = driver.find_element(By.XPATH,value="/html/body/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[1]")
    temperature = temperature_div.text
    print(olt_locations[count], temperature)
    count = count + 1

    # Sends details via email
    # with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    #     connection.starttls()
    #     connection.login(user=os.environ.get("MY_EMAIL"), password=os.environ.get("EMAIL_PASSWORD"))
    #     connection.sendmail(
    #         from_addr=os.environ.get("MY_EMAIL"),
    #         to_addrs=os.environ.get("MY_EMAIL"),
    #         msg=f"Subject:New Message CMS\n\n"
    #             f"OLT: \n"
    #             f"Temperature: {temperature.split("℃")[0]}\n"
    #     )


driver.quit()
