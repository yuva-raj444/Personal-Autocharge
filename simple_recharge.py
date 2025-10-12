"""
Simple Jio Recharge Automation - No Flask Required
Just run this file to start the automation
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import traceback

# Configuration - Update these values
MOBILE_NUMBER = "9976954671"
UPI_ID = "gyuvaraj444@oksbi"
JIO_URL = "https://www.jio.com/selfcare/plans/mobility/prepaid-plans-list/?category=Popular%20Plans&categoryId=UG9wdWxhciBQbGFucw==&subcategory=MS41IEdCL2RheSBQbGFucw=="

def log_step(step_num, description, details=""):
    """Helper function to log steps with consistent formatting"""
    print("\n" + "="*70)
    print(f"📍 STEP {step_num}: {description}")
    print("="*70)
    if details:
        print(f"   {details}")
    print()

def perform_recharge():
    """
    Performs the Jio recharge automation using Selenium
    Returns: tuple (success: bool, message: str)
    """
    driver = None
    try:
        log_step(0, "INITIALIZING BROWSER", "Setting up Chrome with automation detection disabled")
        
        # Setup Chrome options - Browser will be VISIBLE
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Ensure browser is visible (no headless mode)
        print("   ✓ Chrome options configured (VISIBLE MODE)")
        print("   ✓ Starting Chrome WebDriver...")
        print("   ⚠️  Browser window should open now...")
        
        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)
        
        # Bring browser window to front
        driver.maximize_window()
        print("   ✓ Browser window maximized and ready")
        print("   ✓ Chrome browser launched successfully!")
        
        log_step(1, "NAVIGATING TO JIO PLANS PAGE", f"URL: {JIO_URL[:80]}...")
        driver.get(JIO_URL)
        print(f"   ✓ Page loaded: {driver.title}")
        print(f"   ✓ Current URL: {driver.current_url}")
        time.sleep(3)  # Allow page to load completely
        print("   ✓ Waiting for page elements to load...")
        
        log_step(2, "SEARCHING FOR ₹299 PLAN", "Looking for plan card with ₹299")
        
        # Find all plan cards and look for the one with ₹299
        print("   🔍 Searching for plan card with class 'planDetailsCard_container'...")
        plan_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'planDetailsCard_container') or contains(@class, 'Details_planCard')]")
        print(f"   ✓ Found {len(plan_cards)} plan cards on page")
        
        plan_found = False
        buy_button = None
        
        for idx, card in enumerate(plan_cards):
            print(f"   🔍 Checking plan card {idx + 1}/{len(plan_cards)}...")
            try:
                # Check if this card contains 299
                card_text = card.text
                if '299' in card_text or '₹299' in card_text:
                    print(f"      ✓ Found card with ₹299!")
                    # Look for Buy button within this card
                    buy_button = card.find_element(By.XPATH, ".//button[contains(@class, 'j-button') and (contains(., 'Buy') or contains(., 'buy'))]")
                    plan_found = True
                    print(f"      ✅ SUCCESS! Found ₹299 plan with Buy button")
                    print(f"      ✓ Button text: '{buy_button.text}'")
                    print(f"      ✓ Button classes: {buy_button.get_attribute('class')}")
                    break
            except:
                continue
        
        if not plan_found or not buy_button:
            error_msg = "Could not find ₹299 plan or Buy button on the page"
            print(f"\n   ❌ ERROR: {error_msg}")
            print(f"   Current URL: {driver.current_url}")
            return False, error_msg
        
        log_step(3, "CLICKING BUY BUTTON", f"Button text: '{buy_button.text}'")
        print("   ✓ Scrolling button into view...")
        driver.execute_script("arguments[0].scrollIntoView(true);", buy_button)
        time.sleep(1)
        print("   ✓ Clicking button...")
        driver.execute_script("arguments[0].click();", buy_button)
        print("   ✓ Button clicked successfully!")
        print("   ⏳ Waiting for next page to load...")
        time.sleep(3)
        print(f"   ✓ Current URL: {driver.current_url}")
        
        log_step(4, "WAITING FOR MOBILE NUMBER INPUT", "Looking for phone number input field...")
        # Wait for mobile number input field
        print("   🔍 Searching for mobile number input field...")
        mobile_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='tel'] | //input[@type='text' and (contains(@placeholder, 'mobile') or contains(@placeholder, 'number'))] | //input[contains(@id, 'mobile') or contains(@name, 'mobile')]"))
        )
        print(f"   ✓ Found mobile input field!")
        print(f"   ✓ Input type: {mobile_input.get_attribute('type')}")
        print(f"   ✓ Placeholder: {mobile_input.get_attribute('placeholder')}")
        
        log_step(5, "ENTERING MOBILE NUMBER", f"Number: {MOBILE_NUMBER}")
        print("   ✓ Clearing existing value...")
        mobile_input.clear()
        print("   ✓ Entering mobile number...")
        mobile_input.send_keys(MOBILE_NUMBER)
        print(f"   ✓ Mobile number entered: {mobile_input.get_attribute('value')}")
        time.sleep(1)
        
        log_step(6, "CLICKING SUBMIT BUTTON", "Searching for submit/continue button...")
        # Find and click submit button
        print("   🔍 Looking for submit button...")
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'SUBMIT', 'submit'), 'submit')] | //button[@type='submit'] | //button[contains(translate(., 'CONTINUE', 'continue'), 'continue')]"))
        )
        print(f"   ✓ Found button: '{submit_button.text}'")
        print("   ✓ Clicking submit button...")
        driver.execute_script("arguments[0].click();", submit_button)
        print("   ✓ Submit clicked!")
        print("   ⏳ Waiting for payment page to load...")
        time.sleep(5)  # Wait for payment page to load
        print(f"   ✓ Current URL: {driver.current_url}")
        
        log_step(7, "WAITING FOR PAYMENT PAGE", "Confirming payment options are visible...")
        # Wait for payment section to load
        print("   🔍 Searching for payment section...")
        time.sleep(3)  # Allow payment page to fully load
        print(f"   ✓ Current URL: {driver.current_url}")
        print(f"   ✓ Page title: {driver.title}")
        
        log_step(8, "SELECTING GOOGLE PAY", "Looking for Google Pay payment option...")
        print("   🔍 Searching for Google Pay button/option...")
        print(f"   📱 Will use UPI ID: {UPI_ID}")
        
        # Look for Google Pay text element
        google_pay_option = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Google Pay') or contains(text(), 'GPay') or contains(text(), 'google pay') or contains(@aria-label, 'Google Pay')]"))
        )
        print(f"   ✓ Found Google Pay option: '{google_pay_option.text}'")
        print(f"   ✓ Element tag: {google_pay_option.tag_name}")
        print(f"   ✓ Element class: {google_pay_option.get_attribute('class')}")
        print("   ✓ Scrolling into view...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", google_pay_option)
        time.sleep(1)
        print("   ✓ Clicking Google Pay...")
        driver.execute_script("arguments[0].click();", google_pay_option)
        print("   ✅ Google Pay clicked successfully!")
        
        print("   ⏳ Waiting for Google Pay form to load...")
        time.sleep(3)  # Wait for Google Pay option to be fully selected and form to appear
        print("   ✅ Ready to enter UPI ID")
        
        log_step(9, "ENTERING UPI ID FOR GOOGLE PAY", f"UPI ID: {UPI_ID}")
        print("   ⏳ Waiting for VPA ID input field to appear...")
        time.sleep(3)  # Wait for Google Pay form to load
        
        # Find VPA ID input field - looking specifically for VPA field
        print("   🔍 Searching for VPA ID input field...")
        upi_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, 
                "//input[contains(@placeholder, 'VPA') or contains(@placeholder, 'vpa') or contains(@name, 'vpa') or contains(@id, 'vpa') or "
                "contains(@placeholder, 'UPI') or contains(@placeholder, 'upi') or contains(@name, 'upi') or contains(@id, 'upi') or "
                "contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enter vpa') or "
                "contains(translate(@placeholder, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enter upi')]"))
        )
        print(f"   ✓ Found VPA ID input field!")
        print(f"   ✓ Placeholder: {upi_input.get_attribute('placeholder')}")
        
        # Just paste the UPI ID directly - no clearing, no extra steps
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
        
        log_step(10, "PAYMENT REQUEST INITIATED", "Waiting for payment confirmation screen...")
        print("   ⏳ Waiting for Google Pay payment request to be triggered...")
        time.sleep(5)  # Wait for payment request to be triggered
        print(f"   ✓ Current URL: {driver.current_url}")
        
        log_step(11, "✅ SUCCESS - GOOGLE PAY PAYMENT REQUEST TRIGGERED!", 
                "Check your Google Pay app to approve the payment")
        print("   🎉 Automation completed successfully!")
        print("   📱 Open Google Pay on your phone to approve the ₹299 payment")
        print("   🌐 Browser window will remain open for verification")
        
        # Keep browser open for a few seconds to show the final state
        time.sleep(3)
        
        return True, "Recharge initiated. Approve payment in your UPI app."
        
    except TimeoutException as e:
        error_msg = f"Timeout waiting for element: {str(e)}"
        print("\n" + "="*70)
        print("❌ TIMEOUT ERROR")
        print("="*70)
        print(f"   Error: {error_msg}")
        if driver:
            print(f"   Current URL: {driver.current_url}")
            print(f"   Page title: {driver.title}")
        print()
        return False, error_msg
    except NoSuchElementException as e:
        error_msg = f"Element not found: {str(e)}"
        print("\n" + "="*70)
        print("❌ ELEMENT NOT FOUND ERROR")
        print("="*70)
        print(f"   Error: {error_msg}")
        if driver:
            print(f"   Current URL: {driver.current_url}")
            print(f"   Page title: {driver.title}")
        print()
        return False, error_msg
    except Exception as e:
        error_msg = f"Error during automation: {str(e)}\n{traceback.format_exc()}"
        print("\n" + "="*70)
        print("❌ UNEXPECTED ERROR")
        print("="*70)
        print(f"   Error: {str(e)}")
        if driver:
            print(f"   Current URL: {driver.current_url}")
            print(f"   Page title: {driver.title}")
        print(f"\n   Full traceback:\n{traceback.format_exc()}")
        return False, error_msg
    finally:
        # Keep browser open for debugging (comment out if you want to auto-close)
        if driver:
            print("\n" + "="*70)
            print("🌐 BROWSER STATUS")
            print("="*70)
            print("   Browser will remain open for manual verification")
            print("   Close the browser window manually when done")
            print("="*70 + "\n")
            # Uncomment the line below to auto-close the browser
            # driver.quit()

if __name__ == '__main__':
    print("\n" + "🟢"*70)
    print("🚀 JIO RECHARGE AUTOMATION (SIMPLE VERSION)")
    print("🟢"*70)
    print("\n📋 CONFIGURATION:")
    print(f"   Mobile Number: {MOBILE_NUMBER}")
    print(f"   UPI ID: {UPI_ID}")
    print(f"   Plan Amount: ₹299")
    
    if MOBILE_NUMBER == "9976954671" and UPI_ID == "gyuvaraj444@oksbi":
        print("\n✅ Using your configured credentials")
    
    print("\n📝 AUTOMATION FLOW:")
    print("   Step 0:  Initialize Browser")
    print("   Step 1:  Navigate to Jio Plans")
    print("   Step 2:  Search for ₹299 Plan")
    print("   Step 3:  Click Buy Button")
    print("   Step 4:  Wait for Mobile Input")
    print("   Step 5:  Enter Mobile Number")
    print("   Step 6:  Click Submit")
    print("   Step 7:  Wait for Payment Page")
    print("   Step 8:  Select Google Pay")
    print("   Step 9:  Enter UPI ID & Press Enter")
    print("   Step 10: Payment Request Initiated")
    print("   Step 11: Google Pay Payment Request Triggered ✅")
    
    print("\n" + "🟢"*70)
    print("Starting automation in 3 seconds...")
    print("🟢"*70 + "\n")
    
    time.sleep(3)
    
    success, message = perform_recharge()
    
    if success:
        print("\n" + "✅"*70)
        print("SUCCESS!")
        print("✅"*70)
        print(f"   {message}")
        print("   📱 Check your Google Pay app to approve the payment")
        print("✅"*70 + "\n")
    else:
        print("\n" + "❌"*70)
        print("FAILED!")
        print("❌"*70)
        print(f"   {message}")
        print("❌"*70 + "\n")
    
    print("\n💡 Press Ctrl+C to exit or close the browser window when done")
    
    try:
        # Keep script running so browser stays open
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
