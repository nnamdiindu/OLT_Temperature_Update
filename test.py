import os
import smtplib
import time
import logging
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OLTTemperatureMonitor:
    def __init__(self):
        load_dotenv()
        self.ip_addresses = [
            "http://10.0.04.142/", "http://10.0.4.90/", "http://10.0.4.103/", "http://10.0.4.40/", "http://10.0.4.44/",
            "http://10.0.4.43/", "http://10.0.4.60/","http://10.0.4.86/", "http://10.0.4.87/", "http://10.0.4.41/",
            "http://10.0.4.21/","http://10.0.4.162/","http://10.0.4.160/", "http://10.0.4.161/", "http://10.0.4.138/",
            "http://10.0.4.129/", "http://10.0.4.75/","http://10.0.4.96/", "http://10.0.4.97/", "http://10.0.4.149/",
            "http://10.0.4.150/", "http://10.0.4.136/","http://10.0.4.91/", "http://10.0.4.130/", "http://10.0.4.134/",
            "http://10.0.4.128/", "http://10.0.4.125/","http://10.0.4.126/", "http://10.0.4.129/", "http://10.0.4.69/",
            "http://10.0.4.140/", "http://10.0.4.132/","http://10.0.4.133/", "http://10.0.4.131/", "http://10.0.4.117/",
            "http://10.0.4.118/", "http://10.0.4.123/", "http://10.0.4.124/", "http://10.0.4.110/", "http://10.0.4.17/",
            "http://10.0.4.90/", "http://10.0.4.91/", "http://10.0.4.106/", "http://10.0.4.107/", "http://10.0.4.108/",
            "http://10.0.4.109/", "http://10.0.4.42/", "http://10.0.4.63/", "http://10.0.4.43/", "http://10.0.4.44/",
            "http://10.0.4.50/", "http://10.0.4.40/", "http://10.0.4.103/", "http://10.0.4.48/", "http://10.0.4.93/",
            "http://10.0.4.92/", "http://10.0.4.23/", "http://10.0.4.80/", "http://10.0.4.82/", "http://10.0.4.83/",
            "http://10.0.4.84/", "http://10.0.4.61/", "http://10.0.4.88/", "http://10.0.4.89/", "http://10.0.4.74/",
            "http://10.0.4.62/", "http://10.0.4.85/", "http://10.0.4.20/", "http://10.0.4.65/", "http://10.0.4.66/",
            "http://10.0.4.67/", "http://10.0.4.71/", "http://10.0.4.72/", "http://10.0.4.45/", "http://10.0.4.46/",
            "http://10.0.4.47/", "http://10.0.4.52/", "http://10.0.4.60/", "http://10.0.4.59/", "http://10.0.4.64/",
            "http://10.0.4.51/", "http://10.0.4.78/", "http://10.0.4.79/", "http://10.0.4.144/", "http://10.0.4.145/",
            "http://10.0.4.132/", "http://10.0.4.133/", "http://10.0.4.148/"
        ]
        self.olt_locations = [
            "LOS-SUNSHINEESTATE-FD1700S-001", "LOS-IKONECTT-SUNSHINEESTATE-001", "LOS-UNITYHOMESESTATE-FD1700S-002",
            "LOS-UNITYHOMESESTATE-FD1700S-001", "LOSCEDARCOUNTY-OLT-FD1700S-001", "LOSCEDARCOUNTY-OLT-FD1700S-002",
            "LOS-IKONECTT-AVERA-OLT-FD1700S-001", "LOS-LekkiGardensPH5-OLT-001", "LOS-LekkiGardensPH5-OLT-002",
            "LOS-EricmoreOLT", "L0S-SpringbayOLT", "los29-olt-001", "LOS-BEACHFRONT-OLT-001", "LOS-ATLANTICVILLE-001",
            "LOS-IKONECTT-LEKKIGARDENS2-001", "LOSOAMS-ILUPEJU-OLT-001", "LOS-NEWHORIZON_OFFICE-OLT-001",
            "LOS-JORAESTATE-OLT-001", "LOS-JORAESTATE-OLT-002", "LOS-YABACLUSTER3-OLT-001", "LOS-YABACLUSTER3-OLT-002",
            "LOS-DIVINEESTATE-OLT-001", "LOS-SILVERPOINTESTATE-OLT-002", "LOS-SILVERPOINTESTATE-OLT-001",
            "LOSDOLPHINESTATE-OLT-001", "LOS-SEASIDEESTATE-OLT-003", "LOS-MANORESTATE-OLT-001", "LOS-MANORESTATE-OLT-002",
            "LOS-OAM-ILUPEJU-001", "LOS-IKONECCT-MIJIL", "LOS-MIJIL-OLT-002", "LOS-INFINITY-001","LOS-INFINITY-002",
            "LOS-RACKCENTER", "LOS-SOUTHDRIFTESTATE-OLT-001", "LOS-SOUTHDRIFTESTATE-OLT-002", "LOS-OLALEYE-OLT-001",
            "LOS-OLALEYE-OLT-002", "LOS-ATUNRASE-OLT-1", "Bashorun-Wacs Redundancy Leg", "LOS-SunshineEstate-OLT-001",
            "LOS-SunshineEstate-OLT-002", "LOS-MILLENIUMGBAGADA-OLT-001", "LOS-MILLENIUMGBAGADA-OLT-002",
            "LOS-MILLENIUMGBAGADA-OLT-003", "LOS-MILLENIUMGBAGADA-OLT-004", "LOS-IKONNECT-OCEANPALM-001",
            "LOS-IKONNECT-OCEANPALM-002", "LOS-IKONNECT-CEDARCOUNTY-001", "LOS-IKONNECT-CEDARCOUNTY-002", "LOS-dideolu-OLT-002",
            "LOS-UNITYHOMES-OLT-001", "LOS-UNITYHOMES-OLT-002", "LOS-IKONNECTT-BUENAVISTA-002", "LOS-OloriMojisolaOnikoyi-001",
            "LOS-ACADIA MEWS Outdoor-OLT", "LOS-CWG-OLT", "LOS-Chevvy Estate-OLT-001", "LOS-United Estates-OLT-001",
            "LOS-UnitedEstates-OLT-002", "LOS-UnitedEstates-OLT-003", "LOS-OguduGRAOLT", "LOS-ChevvyEstate-OLT-002",
            "LOS-ChevvyEstate-OLT-003", "LOS-OguduGRAOLT-002", "LOS-WhiteOaks-OLT", "LOS-Bashorun-OLT", "LOS-ACA-OLT",
            "LOS-IDS-OLT-001", "LOS-IDS-OLT-002", "LOS-IDS-OLT-003", "LOS-IDS-OLT-004", "LOS-OfficeOLT-001",
            "LOS-Computervillage-OLT-001", "LOS-Computervillage-OLT-002", "LOS-IKONNECTT-BUENAVISTA-001", "LOS-PeacevilleOLT",
            "LOS-AveraOLT-002", "LOS01-OLT-001(OADC)", "LOS-karimu-OLT-001", "LOS-Oriola", "LOS-OsborneOLT",
            "LOS-Millenium(Cobranet)OLT", "LOS-IKONNECTT-GREENVILLE-002", "LOS-IKONNECTT-GREENVILLE-003",
            "LOS-IKONNECTT-INFINITYESTATE-001", "LOS-IKONNECTT-INFINITYESTATE-002", "LOS-ACADIAGROOVE-001"
        ]
        self.driver = None
        self.temperature_data = []

    def setup_driver(self):
        """Initialize Chrome driver with proper options"""
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")  # Run in background
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            logger.info("Chrome driver initialized successfully")
        except WebDriverException as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise

    def login_to_device(self, ip_address):
        """Login to OLT device web interface"""
        try:
            self.driver.get(ip_address)

            # Wait for login form to load
            wait = WebDriverWait(self.driver, 10)

            # More flexible element selection (try multiple strategies)
            username_selectors = [
                "//input[@type='text']",
                "//input[contains(@name, 'user')]",
                "//input[contains(@id, 'user')]",
                "/html/body/div/div[2]/div[2]/div/div[2]/div[1]/input"
            ]

            password_selectors = [
                "//input[@type='password']",
                "//input[contains(@name, 'pass')]",
                "//input[contains(@id, 'pass')]",
                "/html/body/div/div[2]/div[2]/div/div[2]/div[2]/input"
            ]

            login_selectors = [
                "//button[@type='submit']",
                "//input[@type='submit']",
                "//button[contains(text(), 'Login')]",
                "/html/body/div/div[2]/div[2]/div/div[2]/div[3]/button"
            ]

            # Try to find and fill username
            username_element = None
            for selector in username_selectors:
                try:
                    username_element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    break
                except TimeoutException:
                    continue

            if not username_element:
                raise Exception("Could not find username field")

            username_element.clear()
            username_element.send_keys(os.environ.get("USER"))

            # Try to find and fill password
            password_element = None
            for selector in password_selectors:
                try:
                    password_element = self.driver.find_element(By.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue

            if not password_element:
                raise Exception("Could not find password field")

            password_element.clear()
            password_element.send_keys(os.environ.get("PASSWORD_"))

            # Try to find and click login button
            login_button = None
            for selector in login_selectors:
                try:
                    login_button = self.driver.find_element(By.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue

            if not login_button:
                raise Exception("Could not find login button")

            login_button.click()

            # Wait for page to load after login
            time.sleep(3)
            logger.info(f"Successfully logged into {ip_address}")
            return True

        except Exception as e:
            logger.error(f"Failed to login to {ip_address}: {e}")
            return False

    def get_temperature(self, ip_address):
        """Extract temperature from device interface"""
        try:
            # Multiple possible selectors for temperature element
            temperature_selectors = [
                "//div[contains(text(), '℃')]",
                "//span[contains(text(), '℃')]",
                "//div[contains(@class, 'temperature')]",
                "/html/body/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[1]"
            ]

            wait = WebDriverWait(self.driver, 10)

            for selector in temperature_selectors:
                try:
                    temperature_element = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                    temperature_text = temperature_element.text
                    if '℃' in temperature_text:
                        return temperature_text.split("℃")[0].strip()
                except TimeoutException:
                    continue

            # If no temperature found, try to get any numeric value
            numeric_elements = self.driver.find_elements(By.XPATH,
                                                         "//div[contains(text(), '°') or contains(text(), 'C')]")
            for element in numeric_elements:
                text = element.text
                if any(char.isdigit() for char in text):
                    return text.strip()

            logger.warning(f"Could not find temperature element for {ip_address}")
            return "N/A"

        except Exception as e:
            logger.error(f"Error extracting temperature from {ip_address}: {e}")
            return "ERROR"

    def collect_temperatures(self):
        """Collect temperature data from all OLT devices"""
        self.setup_driver()

        try:
            for i, ip_address in enumerate(self.ip_addresses):
                location = self.olt_locations[i]
                logger.info(f"Processing {location} at {ip_address}")

                if self.login_to_device(ip_address):
                    temperature = self.get_temperature(ip_address)
                    self.temperature_data.append({
                        'location': location,
                        'ip': ip_address,
                        'temperature': temperature,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    logger.info(f"{location}: {temperature}℃")
                else:
                    self.temperature_data.append({
                        'location': location,
                        'ip': ip_address,
                        'temperature': 'LOGIN_FAILED',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

                time.sleep(2)  # Brief pause between requests

        except Exception as e:
            logger.error(f"Error during temperature collection: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                logger.info("Browser driver closed")

    def save_to_file(self, filename="olt_temperature.txt"):
        """Save temperature data to file"""
        try:
            with open(filename, "w") as file:  # Use 'w' to overwrite previous data
                file.write(f"OLT Temperature Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("=" * 60 + "\n")
                for data in self.temperature_data:
                    file.write(f"{data['location']}: {data['temperature']}℃ (Time: {data['timestamp']})\n")
            logger.info(f"Temperature data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to file: {e}")

    def send_email_report(self):
        """Send temperature report via email"""
        try:
            # Format email content
            subject = f"OLT Temperature Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            body = "OLT Temperature Monitoring Report\n"
            body += "=" * 40 + "\n\n"

            for data in self.temperature_data:
                status = "⚠️ ALERT" if data['temperature'] == 'ERROR' or data[
                    'temperature'] == 'LOGIN_FAILED' else "✅ OK"
                body += f"{data['location']}:\n"
                body += f"  Temperature: {data['temperature']}℃\n"
                body += f"  IP: {data['ip']}\n"
                body += f"  Status: {status}\n"
                body += f"  Timestamp: {data['timestamp']}\n\n"

            body += f"\nReport generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Send email
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(
                    user=os.environ.get("MY_EMAIL"),
                    password=os.environ.get("EMAIL_PASSWORD")
                )
                connection.sendmail(
                    from_addr=os.environ.get("MY_EMAIL"),
                    to_addrs=os.environ.get("MY_EMAIL"),
                    msg=f"Subject:{subject}\n\n{body}".encode('utf-8')
                )

            logger.info("Email report sent successfully")

        except Exception as e:
            logger.error(f"Error sending email: {e}")

    def run_monitoring(self):
        """Main method to run the complete monitoring process"""
        logger.info("Starting OLT temperature monitoring")
        self.collect_temperatures()
        self.save_to_file()
        self.send_email_report()
        logger.info("OLT temperature monitoring completed")


def main():
    monitor = OLTTemperatureMonitor()
    monitor.run_monitoring()


if __name__ == "__main__":
    main()