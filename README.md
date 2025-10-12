# Jio Recharge Automation

A Python Flask application that automates Jio mobile recharge (₹299 plan) up to the UPI payment trigger step using Selenium WebDriver.

## Features

- Flask REST API with `/recharge` endpoint
- Selenium automation for Jio website interaction
- Automatic navigation to ₹299 plan
- Mobile number and UPI ID entry
- Stops at UPI payment trigger (manual approval required)

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- Chrome WebDriver (will be managed automatically by webdriver-manager)

## Installation

1. Install the required dependencies:

```powershell
pip install -r requirements.txt
```

2. Update the configuration in `jio_recharge_automation.py`:

```python
MOBILE_NUMBER = "your_mobile_number"  # Replace with your 10-digit mobile number
UPI_ID = "your_upi_id@bank"           # Replace with your UPI ID
```

## Usage

### Start the Flask Server

```powershell
python jio_recharge_automation.py
```

The server will start on `http://localhost:5000`

### Trigger Recharge Automation

**Option 1: Using the test script**

```powershell
python test_recharge.py
```

**Option 2: Using curl**

```powershell
curl -X POST http://localhost:5000/recharge
```

**Option 3: Using PowerShell**

```powershell
Invoke-WebRequest -Uri http://localhost:5000/recharge -Method POST
```

**Option 4: Using Postman or any HTTP client**

Send a POST request to `http://localhost:5000/recharge`

## API Endpoints

### GET /

Returns API information and usage instructions.

**Response:**
```json
{
  "message": "Jio Recharge Automation API",
  "usage": "Send a POST request to /recharge to initiate recharge",
  "endpoints": {
    "/recharge": "POST - Initiate ₹299 Jio recharge",
    "/": "GET - This help message"
  }
}
```

### POST /recharge

Triggers the Selenium automation to perform the recharge.

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Recharge initiated. Approve payment in your UPI app."
}
```

**Error Response (400/500):**
```json
{
  "status": "error",
  "message": "Error details here"
}
```

## Automation Flow

1. Launch Chrome browser (non-headless mode)
2. Navigate to Jio prepaid plans page
3. Find and click the ₹299 plan's "Buy" button
4. Enter mobile number
5. Click Submit
6. Wait for payment page
7. Expand UPI options ("See all")
8. Select "Pay via UPI ID"
9. Enter UPI ID
10. Click "Verify & Pay"
11. Stop (UPI payment request triggered)

## Important Notes

- **Browser stays open**: The browser window remains open after the automation for debugging purposes. You can close it manually.
- **Manual payment approval**: The script stops after triggering the UPI request. You must approve the payment manually in your UPI app.
- **Update credentials**: Always update `MOBILE_NUMBER` and `UPI_ID` before running.
- **Chrome required**: This script uses Chrome WebDriver. Ensure Chrome is installed.
- **Internet connection**: Active internet connection required.

## Troubleshooting

### "Could not find ₹299 plan"

- The Jio website structure may have changed
- Check if the URL is still valid
- Try running with a slower internet connection (increase wait times)

### "Timeout waiting for element"

- Increase the wait time in `WebDriverWait(driver, 20)` to a higher value
- Check if elements are being loaded dynamically
- Verify that the website is accessible

### "Element not found"

- Website structure may have changed
- Check the XPath selectors in the code
- Run in non-headless mode to see what's happening

### Chrome Driver Issues

- Ensure Chrome browser is installed
- The script uses automatic driver management via `webdriver-manager`
- If issues persist, download ChromeDriver manually from https://chromedriver.chromium.org/

## Security Warning

⚠️ **Do not share this code with your mobile number and UPI ID filled in!**

- Always use environment variables or secure configuration for sensitive data
- This is a demonstration script - enhance security for production use
- Never commit credentials to version control

## License

This is a demonstration project. Use at your own risk. Ensure compliance with Jio's terms of service.
