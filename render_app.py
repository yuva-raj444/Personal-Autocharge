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
        
        # Enhanced Chrome options for cloud deployment
        chrome_options = Options()
        
        # Core headless options
        chrome_options.add_argument('--headless=new')  # Use new headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # Memory and performance optimizations
        chrome_options.add_argument('--memory-pressure-off')
        chrome_options.add_argument('--max_old_space_size=4096')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        
        # Security and stability options  
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # Disable images to save bandwidth
        chrome_options.add_argument('--disable-default-apps')
        
        # Keep JavaScript enabled for Jio website functionality
        # chrome_options.add_argument('--disable-javascript')  # Commented out - Jio needs JS
        
        # Browser window and display settings
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        
        # Anti-detection settings
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User data directory
        chrome_options.add_argument('--user-data-dir=/tmp/chrome-user-data')
        
        # Additional stability options for cloud environment
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        
        print("   ✓ Enhanced Chrome options configured for cloud (HEADLESS MODE)")
        
        # Initialize Chrome with explicit timeout and error handling
        try:
            print("   🚀 Initializing Chrome WebDriver...")
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(30)  # 30 second timeout for page loads
            wait = WebDriverWait(driver, 25)  # Increased wait time
            
            # Test if Chrome is working
            print("   🔍 Testing Chrome initialization...")
            driver.get("data:text/html,<html><body><h1>Chrome Test</h1></body></html>")
            
        except Exception as chrome_error:
            print(f"   ❌ Chrome initialization failed: {str(chrome_error)}")
            
            # Fallback: Try simpler Chrome options
            print("   🔄 Trying fallback Chrome configuration...")
            if driver:
                driver.quit()
            
            fallback_options = Options()
            fallback_options.add_argument('--headless=new')
            fallback_options.add_argument('--no-sandbox')
            fallback_options.add_argument('--disable-dev-shm-usage')
            fallback_options.add_argument('--disable-gpu')
            fallback_options.add_argument('--single-process')
            
            driver = webdriver.Chrome(options=fallback_options)
            driver.set_page_load_timeout(30)
            wait = WebDriverWait(driver, 25)
        
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
        
        # EXACT SAME UPI METHOD AS LOCAL simple_recharge.py
        log_step(7, "ENTERING UPI ID FOR GOOGLE PAY", f"UPI ID: {UPI_ID}")
        print("   ⏳ Waiting for Google Pay form to load...")
        time.sleep(5)  # Increased wait time for form to load
        
        # Debug: Check what's on the page
        print(f"   🔍 Current URL: {driver.current_url}")
        all_inputs = driver.find_elements(By.XPATH, "//input")
        print(f"   📊 Found {len(all_inputs)} total input fields")
        
        # Find UPI input field - we know from debugging it has name='upi' or id='upi'
        print("   🔍 Searching for UPI input field with name='upi' or id='upi'...")
        upi_input = None
        
        try:
            # Try to find by name='upi' or id='upi' (this is what we found in debugging)
            upi_inputs = driver.find_elements(By.XPATH, "//input[@name='upi' or @id='upi']")
            if upi_inputs:
                # Take the first one that's visible
                for inp in upi_inputs:
                    if inp.is_displayed():
                        upi_input = inp
                        print(f"   ✓ Found UPI field: name='{inp.get_attribute('name')}', id='{inp.get_attribute('id')}'")
                        break
        except Exception as e:
            print(f"   ⚠️  Error finding UPI field: {e}")
        
        if not upi_input:
            # Fallback: try the broader search
            print("   🔍 Trying broader VPA/UPI search...")
            try:
                upi_input = wait.until(
                    EC.presence_of_element_located((By.XPATH, 
                        "//input[contains(@placeholder, 'VPA') or contains(@placeholder, 'vpa') or contains(@name, 'vpa') or contains(@id, 'vpa') or "
                        "contains(@placeholder, 'UPI') or contains(@placeholder, 'upi') or contains(@name, 'upi') or contains(@id, 'upi') or "
                        "contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enter vpa') or "
                        "contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enter upi')]"))
                )
                print(f"   ✓ Found VPA ID input field with broader search!")
            except:
                print("   ❌ Could not find UPI input field")
                return False, "Timeout: UPI input field not found"
        
        print(f"   ✓ Placeholder: {upi_input.get_attribute('placeholder')}")
        
        # Just paste the UPI ID directly - no clearing, no extra steps (EXACT SAME AS LOCAL)
        print(f"   ✓ Pasting UPI ID: {UPI_ID}")
        upi_input.send_keys(UPI_ID)
        time.sleep(0.5)
        
        # Verify the value
        entered_value = upi_input.get_attribute('value')
        print(f"   ✓ UPI ID in field: '{entered_value}'")
        print(f"   ✅ UPI ID pasted successfully!")
        
        # Press Enter to submit
        print("   ✓ Pressing Enter to submit...")
        upi_input.send_keys(Keys.RETURN)
        print("   ✅ Enter pressed!")
        time.sleep(1)
        
        log_step(8, "PAYMENT REQUEST INITIATED", "Waiting for payment confirmation screen...")
        print("   ⏳ Waiting for Google Pay payment request to be triggered...")
        time.sleep(5)  # Wait for payment request to be triggered
        print(f"   ✓ Current URL: {driver.current_url}")
        
        log_step(9, "✅ SUCCESS - GOOGLE PAY PAYMENT REQUEST TRIGGERED!", 
                "Check your Google Pay app to approve the payment")
        print("   🎉 Automation completed successfully!")
        print("   📱 Open Google Pay on your phone to approve the ₹299 payment")
        print("   🌐 Headless automation completed - check logs for verification")
        
        # Keep a brief pause for final state
        time.sleep(2)
        
        return True, "Recharge initiated. Approve payment in your UPI app."
        
    except TimeoutException as e:
        error_msg = f"Timeout waiting for element: {str(e)}"
        print(f"   ❌ TIMEOUT: {error_msg}")
        return False, f"Timeout error - {error_msg}"
    except NoSuchElementException as e:
        error_msg = f"Element not found: {str(e)}"
        print(f"   ❌ ELEMENT NOT FOUND: {error_msg}")
        return False, f"Element not found - {error_msg}"
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(f"   ❌ ERROR: {error_msg}")
        return False, f"Automation error - {str(e)}"
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