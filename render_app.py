"""
Jio Recharge Automation - Web Service for Render
Headless Chrome automation that can run on cloud platforms
"""
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time
import traceback

app = Flask(__name__)

# Configuration - Update these values
MOBILE_NUMBER = os.environ.get('MOBILE_NUMBER', '9976954671')
UPI_ID = os.environ.get('UPI_ID', 'gyuvaraj444@oksbi')
JIO_URL = "https://www.jio.com/selfcare/plans/mobility/prepaid-plans-list/?category=Popular%20Plans&categoryId=UG9wdWxhciBQbGFucw==&subcategory=MS41IEdCL2RheSBQbGFucw=="

def log_step(step_num, description, details=""):
    """Helper function to log steps"""
    print(f"\n📍 STEP {step_num}: {description}")
    if details:
        print(f"   {details}")

def perform_recharge():
    """
    Performs the Jio recharge automation using Selenium (Headless for Cloud)
    Returns: tuple (success: bool, message: str)
    """
    driver = None
    try:
        log_step(0, "INITIALIZING HEADLESS BROWSER", "Setting up Chrome for cloud deployment")
        
        # Setup Chrome options for cloud deployment (headless)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Required for cloud hosting
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        print("   ✓ Chrome options configured for cloud (HEADLESS MODE)")
        
        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)
        
        print("   ✓ Headless Chrome browser launched successfully!")
        
        log_step(1, "NAVIGATING TO JIO PLANS PAGE")
        driver.get(JIO_URL)
        print(f"   ✓ Page loaded: {driver.title}")
        time.sleep(3)
        
        log_step(2, "SEARCHING FOR ₹299 PLAN")
        plan_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'planDetailsCard_container') or contains(@class, 'Details_planCard')]")
        print(f"   ✓ Found {len(plan_cards)} plan cards")
        
        plan_found = False
        buy_button = None
        
        for idx, card in enumerate(plan_cards):
            try:
                card_text = card.text
                if '299' in card_text or '₹299' in card_text:
                    print(f"   ✓ Found ₹299 plan in card {idx + 1}")
                    buy_button = card.find_element(By.XPATH, ".//button[contains(@class, 'j-button') and (contains(., 'Buy') or contains(., 'buy'))]")
                    plan_found = True
                    break
            except:
                continue
        
        if not plan_found or not buy_button:
            return False, "Could not find ₹299 plan or Buy button"
        
        log_step(3, "CLICKING BUY BUTTON")
        driver.execute_script("arguments[0].scrollIntoView(true);", buy_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", buy_button)
        print("   ✓ Buy button clicked")
        time.sleep(3)
        
        log_step(4, "ENTERING MOBILE NUMBER")
        mobile_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='tel'] | //input[@type='text' and (contains(@placeholder, 'mobile') or contains(@placeholder, 'number'))] | //input[contains(@id, 'mobile') or contains(@name, 'mobile')]"))
        )
        mobile_input.clear()
        mobile_input.send_keys(MOBILE_NUMBER)
        print(f"   ✓ Entered mobile: {MOBILE_NUMBER}")
        time.sleep(1)
        
        log_step(5, "CLICKING SUBMIT")
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'SUBMIT', 'submit'), 'submit')] | //button[@type='submit'] | //button[contains(translate(., 'CONTINUE', 'continue'), 'continue')]"))
        )
        driver.execute_script("arguments[0].click();", submit_button)
        print("   ✓ Submit clicked")
        time.sleep(5)
        
        log_step(6, "SELECTING GOOGLE PAY")
        google_pay_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Google Pay') or contains(text(), 'GPay') or contains(text(), 'google pay')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", google_pay_option)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", google_pay_option)
        print("   ✓ Google Pay selected")
        time.sleep(3)
        
        log_step(7, "ENTERING UPI ID")
        upi_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//input[contains(@placeholder, 'VPA') or contains(@placeholder, 'vpa') or contains(@name, 'vpa') or contains(@id, 'vpa') or "
                "contains(@placeholder, 'UPI') or contains(@placeholder, 'upi') or contains(@name, 'upi') or contains(@id, 'upi')]"))
        )
        upi_input.send_keys(UPI_ID)
        print(f"   ✓ Entered UPI ID: {UPI_ID}")
        time.sleep(0.5)
        
        log_step(8, "SUBMITTING PAYMENT")
        upi_input.send_keys(Keys.RETURN)
        print("   ✓ Payment submitted")
        time.sleep(5)
        
        print("   🎉 Automation completed successfully!")
        return True, "Recharge initiated. Check your Google Pay app to approve the payment."
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"   ❌ {error_msg}")
        return False, error_msg
    finally:
        if driver:
            driver.quit()

@app.route('/')
def home():
    return jsonify({
        "message": "Jio Recharge Automation API",
        "endpoints": {
            "/": "GET - This help page",
            "/recharge": "POST - Trigger recharge automation",
            "/health": "GET - Health check"
        },
        "usage": "Send POST to /recharge to start automation"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "jio-recharge-automation"})

@app.route('/recharge', methods=['POST'])
def recharge():
    try:
        print(f"\n🚀 Recharge request received at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Mobile: {MOBILE_NUMBER}")
        print(f"   UPI ID: {UPI_ID}")
        
        success, message = perform_recharge()
        
        if success:
            return jsonify({
                "status": "success",
                "message": message,
                "mobile": MOBILE_NUMBER,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": message,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}",
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)