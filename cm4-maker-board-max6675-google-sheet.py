import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import SpreadsheetNotFound
from ReadMAX6675 import Thermocouple
import time
import csv



# Connect to Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("gs_credentials.json", scope)
client = gspread.authorize(credentials)

spreadsheetName = 'Thermocouple_log' # Enter your spreadsheet name

try:
    # If spreadsheet exists:
    # Open the spreadsheet
    spreadsheet = client.open(spreadsheetName)
    
    # Open the sheet 1 in Google spreadsheet
    worksheet = client.open(spreadsheetName).sheet1
    
    print("Spreadsheet exists")
    
  
except SpreadsheetNotFound:
    # If spreadsheet doesn't exist:
    # Create new spreadsheet
    print("Spreadsheet doesn't exist")
    print("Creating Spreadsheet")
    spreadsheet = client.create(spreadsheetName)
    
    # Open the spreadsheet
    worksheet = client.open(spreadsheetName).sheet1
    
    

# Share the spreadsheet on email
spreadsheet.share("your_email@gmail.com", perm_type="user", role="writer")
#sheet.share("your_email@gmail.com", perm_type="user", role="reader")
    
spreadsheet_url = "https://docs.google.com/spreadsheets/d/%s" % spreadsheet.id
print("Google Spreadsheet url: {}".format(spreadsheet_url))

# Create the first row header name
first_row = ["Time","Thermocouple 1","Thermocouple 2"]

# Read the first row on the google spreadsheet   
values_list = worksheet.row_values(1)

# Compare the value, if not same initalize the spreadsheet and csv file
if values_list != first_row:
    print("Initialize the writing")
    
    # Clear entire worksheet
    worksheet.clear()
    
    # Write first row on the google sheet
    worksheet.append_row(["Time","Thermocouple 1","Thermocouple 2"])
    
    # Write first row on the CSV file
    with open('offline-file.csv', mode='w', newline='') as sensor_file:
        sensor_writer = csv.writer(sensor_file, quoting=csv.QUOTE_MINIMAL)
        sensor_writer.writerow(["Time","Thermocouple 1","Thermocouple 2"])

# set the pin for communicate with MAX6675
# GPIO Num
cs_1 = 12
sck_1 = 5
so_1 = 6

cs_2 = 13
sck_2 = 23
so_2 = 24

# max6675 set pin Thermocoupler(CS, SCK, SO, unit) [unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
thermo_1 = Thermocouple(cs_1, sck_1, so_1, 1)
thermo_2 = Thermocouple(cs_2, sck_2, so_2, 1)

while True:
    # read current time
    time_thermo = time.strftime("%d/%m/%y %I:%M%p")
    
    # read temperature 
    t_1 = thermo_1.read_temp()
    t_2 = thermo_2.read_temp()
    
    # Write append the data on the google sheet
    worksheet.append_row([time_thermo,t_1,t_2])
    
    # Write append the data on the CSV file on current directory
    with open('offline-file.csv', mode='a', newline='') as sensor_file:
        sensor_writer = csv.writer(sensor_file)
        sensor_writer.writerow([time_thermo,t_1,t_2])
        
    print("Appended: {}, {}, {}".format(time_thermo,t_1,t_2))
        
    time.sleep(2)
    

