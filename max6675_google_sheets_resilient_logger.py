# This code for send the thermocouples data to the Google Spreadsheets with additional feature
# to avoid data lost during connection error or high traffic server
# by saving the data in the CSV file before uploading to the Google Spreadsheets and resume upload when connection restored
# Also using different thread for each read data then save to CSV file and upload to Google Spreadsheets
# to increase the consistent time interval to read the thermocouple sensor.

import time
import csv
import gspread
from google.oauth2 import service_account
from datetime import datetime
from ReadMAX6675 import Thermocouple
from requests.exceptions import ConnectionError
import threading

# Your Google Sheets API credentials JSON file
JSON_FILE = 'your_credentials_file.json'
# The email you want to share the Google Sheet with
SHARE_WITH_EMAIL = 'your_email@example.com'
# The name of the Google Sheet
SPREADSHEET_NAME = 'Thermocouple_Data'
# The name of the local CSV file
CSV_FILE = 'thermocouple_data.csv'
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
    
    # Read temperature 
    data_thermo_1 = thermo_1.read_temp()
    data_thermo_2 = thermo_2.read_temp()
    
    return {"Thermocouple 1": data_thermo_1, "Thermocouple 2": data_thermo_2}

# Function to append data to a local CSV file
def append_data_to_csv(data):
    with open(CSV_FILE, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)
        print(f'Write row to csv: {data}')

# Function to connect to Google Sheets using the API credentials
def connect_to_google_sheets():
    creds = service_account.Credentials.from_service_account_file(JSON_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    return client

# Function to create a new Google Sheet if it doesn't exist, or open the existing one
def create_or_open_spreadsheet(client, spreadsheet_name):
    try:
        spreadsheet = client.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(spreadsheet_name)

    return spreadsheet

def send_data_from_csv_to_google_sheets(client, spreadsheet_name, csvfile, last_send_row):
    with open(csvfile, 'r') as f:
        csv_data = [row for row in csv.reader(f)]

    spreadsheet = client.open(spreadsheet_name)
    sheet = spreadsheet.sheet1

    # Add the data rows after the last send row
    for row in csv_data[last_send_row:]:
        sheet.append_row(row)
        last_send_row += 1
        print(f'Successfully sent data to Google Sheets')
    return last_send_row
        
def save_data_to_csv():
    # Check if the CSV file has headers and add them if not
    with open(CSV_FILE, 'a+', newline='') as csvfile:
        csvfile.seek(0)  # Move to the start of the file
        if not len(csvfile.readline()):  # Check if the file is empty
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Timestamp", "Thermocouple 1", "Thermocouple 2"])  # Write headers
            
    while True:
        data = read_sensor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [timestamp, data["Thermocouple 1"], data["Thermocouple 2"]]
        append_data_to_csv(row)  # Append data to local CSV file
        time.sleep(SENDING_INTERVAL)  # Adjust the time interval


def upload_data_to_google_sheets():
    client = None
    document_shared = False
    headers_added = False
    check_row = False
    last_send_row = 1
    
    
    while True:
        try:
            # Connect to Google Sheets API
            if not client:
                client = connect_to_google_sheets()
                spreadsheet = create_or_open_spreadsheet(client, SPREADSHEET_NAME)

                # Share the Google Sheet with the specified email
                if not document_shared:
                    spreadsheet.share(SHARE_WITH_EMAIL, perm_type='user', role='writer')
                    print(f"Google Sheet URL: {spreadsheet.url}")  # Print the URL of the Google Sheet
                    document_shared = True
                    
            # Access the first sheet in the Google Sheet
            sheet = spreadsheet.sheet1

            # Add headers to the Google Sheet if there is no existing data
            if not headers_added:
                current_data = sheet.get_all_values()
                if len(current_data) == 0:
                    sheet.append_row(["Timestamp", "Thermocouple 1", "Thermocouple 2"])
                headers_added = True
                
            # Find length spreadsheet, compare to csv, update the last_send_row    
                if not check_row:
                    with open(CSV_FILE, 'a+', newline='') as csvfile:
                        csv_row = len(csvfile.readline())
                    spreasheet_row = len(sheet.get_all_values()) # Get number of rows in spreadsheet
                    if spreasheet_row != csv_row:
                        last_send_row = spreasheet_row
                    check_row = True

            # Send data from the CSV file to Google Sheets update last send row
            last_send_row = send_data_from_csv_to_google_sheets(client, SPREADSHEET_NAME, CSV_FILE, last_send_row)

            # Sleep for a specified interval before trying again
            time.sleep(SENDING_INTERVAL)
        except ConnectionError:
            print("Connection error, will retry...")
            time.sleep(5)  # Adjust the time interval for retrying
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)  # Adjust the time interval for retrying

def main():
    # Create threads for saving data to CSV and uploading data to Google Sheets
    save_data_thread = threading.Thread(target=save_data_to_csv)
    upload_data_thread = threading.Thread(target=upload_data_to_google_sheets)

    # Start the threads
    save_data_thread.start()
    upload_data_thread.start()

    # Wait for the threads to finish
    save_data_thread.join()
    upload_data_thread.join()

if __name__ == '__main__':
    main()

