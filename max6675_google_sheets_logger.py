# This code for send the thermocouples data to the Google Spreadsheets

import time
import gspread
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.auth.exceptions import TransportError
from datetime import datetime
from ReadMAX6675 import Thermocouple

# Your Google Sheets API credentials JSON file
JSON_FILE = 'your_credentials_file.json'
# The email you want to share the Google Sheet with
SHARE_WITH_EMAIL = 'your_email@example.com'
# The name of the Google Sheet
SPREADSHEET_NAME = 'Thermocouple_Data'
# Set sending interval in seconds (s) to read and save data
SENDING_INTERVAL = 60

# Function to read sensor data 
# def read_sensor():
#     # Dummy sensor data, uncomment this function if no actual sensor
#     return {"Thermocouple 1": 25, "Thermocouple 2": 30}

# Function to read sensor data 
def read_sensor():
    # Set the pin for communicate with MAX6675
    cs_1 = 12
    sck_1 = 5
    so_1 = 6

    cs_2 = 13
    sck_2 = 23
    so_2 = 24

    # max6675 set pin Thermocoupler(CS, SCK, SO, unit) [unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
    thermo_1 = Thermocouple(cs_1, sck_1, so_1, 1)
    thermo_2 = Thermocouple(cs_2, sck_2, so_2, 1)
    
    # read temperature 
    data_thermo_1 = thermo_1.read_temp()
    data_thermo_2 = thermo_2.read_temp()
    
    return {"Thermocouple 1": data_thermo_1, "Thermocouple 2": data_thermo_2}

# Function to connect to Google Sheets using the API credentials
def connect_to_google_sheets():
    creds = service_account.Credentials.from_service_account_file(JSON_FILE,scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    return client

# Function to open the existing one Google Sheet, if it doesn't exist it will create a new
def create_or_open_spreadsheet(client, spreadsheet_name):
    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(spreadsheet_name)

    return spreadsheet

def main():
    client = None
    document_shared = False
    headers_added = False

    while True:
        data = read_sensor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [timestamp, data["Thermocouple 1"], data["Thermocouple 2"]]

        try:
            if not client:
                client = connect_to_google_sheets()
                spreadsheet = create_or_open_spreadsheet(client, SPREADSHEET_NAME)

                print(f"Google Sheet URL: {spreadsheet.url}")  # Print the URL of the Google Sheet

                if not document_shared:
                    spreadsheet.share(SHARE_WITH_EMAIL, perm_type='user', role='writer')  # Share the Google Sheet with the specified email
                    document_shared = True

            sheet = spreadsheet.sheet1

            # Add headers to the Google Sheet only if there is no existing data
            if not headers_added:
                current_data = sheet.get_all_values()
                if len(current_data) == 0:
                    sheet.append_row(["Timestamp", "Thermocouple 1", "Thermocouple 2"])
                headers_added = True

            # Send data to Google Sheets
            sheet.append_row(row)
            print(f'Successfully sent data to Google Sheets')

        except (gspread.exceptions.APIError, TransportError) as e:
            print(f'Error sending data to Google Sheets: {e}')
            client = None

        time.sleep(SENDING_INTERVAL)

if __name__ == '__main__':
    main()

