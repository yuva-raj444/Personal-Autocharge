# Personal-Autocharge - Jio Recharge Automation

A Python automation project that automates Jio mobile recharge (₹299 plan) up to the UPI payment trigger step using Selenium WebDriver.

## Features  

- Standalone Python script (no Flask dependency)
- Selenium automation for Jio website interaction
- Automatic navigation to ₹299 plan
- Mobile number and UPI ID entry
- Google Pay integration with UPI payment trigger
- Cloud-ready version for Render hosting

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- Chrome WebDriver (will be managed automatically by webdriver-manager)

## Installation

1. Install the required dependencies:

```powershell
pip install -r requirements.txt
```

2. Update the configuration in `simple_recharge.py`:

```python
MOBILE_NUMBER = "your_mobile_number"  # Replace with your 10-digit mobile number
UPI_ID = "your_upi_id@bank"           # Replace with your UPI ID
```

## Usage

### Local Usage - Simple Version

```powershell
python simple_recharge.py
```

This will:
- Open Chrome browser (visible mode)
- Navigate through the Jio recharge flow
- Stop at UPI payment trigger for manual approval

### Cloud Hosting - Render Version  

```powershell
python render_app.py
```

For cloud deployment, use environment variables:
- `MOBILE_NUMBER`: Your mobile number
- `UPI_ID`: Your UPI ID

## API Endpoints (Render Version)

### GET /

Returns API information and usage instructions.

### POST /recharge

Triggers the Selenium automation to perform the recharge.

**Success Response (200):**
```json
{
  "status": "success", 
  "message": "Recharge initiated. Approve payment in your UPI app."
}
```

## Automation Flow

1. Launch Chrome browser
2. Navigate to Jio prepaid plans page
3. Find and click the ₹299 plan's "Buy" button
4. Enter mobile number
5. Click Submit
6. Wait for payment page
7. Select Google Pay payment option
8. Enter UPI ID and press Enter
9. Payment request initiated
10. Stop (Manual UPI approval required)

## Important Notes

- **Browser visibility**: Local version keeps browser open, cloud version runs headless
- **Manual payment approval**: Script stops after triggering UPI request
- **Update credentials**: Always update `MOBILE_NUMBER` and `UPI_ID` before running
- **Chrome required**: This script uses Chrome WebDriver

## Cloud Deployment (Render)

1. Upload files to your repository
2. Create a new Web Service on Render
3. Set environment variables:
   - `MOBILE_NUMBER`: Your mobile number
   - `UPI_ID`: Your UPI ID
4. Deploy and use the `/recharge` endpoint

## Security Warning

⚠️ **Do not commit credentials to version control!**

- Use environment variables for sensitive data
- The mobile number and UPI ID are hardcoded for demo purposes
- Remove credentials before sharing code

## License

This is a demonstration project. Use at your own risk. Ensure compliance with Jio's terms of service.
