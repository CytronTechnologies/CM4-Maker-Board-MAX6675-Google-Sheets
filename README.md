# CM4-Maker-Board-MAX6675-Google-Sheets


If you want to log temperature sensor data to Google Sheets using CM4 Maker Board, you are in the right place! Here you will find all the information you need to set up your hardware and software and start data logging with the CM4 Maker Board and Google Sheets.

<img src="https://github.com/CytronTechnologies/CM4-Maker-Board-MAX6675-Google-Sheets/blob/main/Pictures/3_flow_diagram_simple_thermocouple_cm4_maker_board.jpg" width="600">  

You can visit [Log Thermocouple Sensor Data to Google Sheets using CM4 Maker Board](https://cytron.io/tutorial/log-thermocouple-sensor-data-to-google-sheets-using-cm4-maker-board) to learn more about it.  

## Requirements  
To get started, you will need the following hardware and software:  

**Hardware:**  
* [CM4 Maker Board](https://cytron.io/p-cm4-maker-board-and-kits)  
* [Rapberry Pi CM4 Lite](https://cytron.io/p-raspberry-pi-cm4-wireless-4gb-ram-lite-no-emmc-and-kits) or [Rapberry Pi CM4 with eMMC](https://cytron.io/p-raspberry-pi-cm4-wireless-8gb-ram-8gb-emmc-and-kits)  
* [MAX6675 K-Thermocouple](https://cytron.io/p-max6675-k-thermocouple-to-digital-converter-module)  


**Software:**  
Raspberry Pi OS with installed Python. If you want to know how to install the Raspberry Pi OS on the CM4 Maker Board, you can visit this tutorial on [Boot up Raspberry Pi CM4 on CM4 Maker Board](https://cytron.io/tutorial/boot-up-raspberry-pi-cm4-on-cm4-maker-board).  

## Installation  
To begin, connect the MAX6675 thermocouples to the Grove port on the CM4 Maker Board. In this example, we will use two thermocouples.

<img src="https://github.com/CytronTechnologies/CM4-Maker-Board-MAX6675-Google-Sheets/blob/main/Pictures/2_thermocouple_connection_to_cm4_maker_board.jpg" width="600"> 

Install Required Libraries on Raspberry Pi CM4.
```
pip install gspread
pip install oauth2client
pip install python-csv
```
Download the code from Github to your home directory.
```
git clone https://github.com/CytronTechnologies/CM4-Maker-Board-MAX6675-Google-Sheets
```
Place the downloaded credentials in the same folder from GitHub. Visit our full tutorial if you want to know how to create [Google Credentials](https://cytron.io/tutorial/log-thermocouple-sensor-data-to-google-sheets-using-cm4-maker-board).
Inside python file max6675_google_sheets_logger.py, edit the name for your json file, email, spreadsheet name and sending interval:
 
```python
# Your Google Sheets API credentials JSON file
JSON_FILE = 'your_credentials_file.json'
# The email you want to share the Google Sheet with
SHARE_WITH_EMAIL = 'your_email@example.com'
# The name of the Google Sheet
SPREADSHEET_NAME = 'Thermocouple_Data'
# Set sending interval in seconds (s) to read and save data
SENDING_INTERVAL = 60
```
Run your code and you can access the data log from the sheet URL in the Python code or find it in the "Shared with me" section of Google Drive. 

**Resilient Data Logger**  
For a more advanced approach, use the max6675_google_sheets_resilient_logger.py script to avoid data loss during connection errors or high-traffic server events. It saves data in a CSV file before uploading it to Google Sheets and resumes the upload once the connection is restored. This script also uses different threads to save data to a CSV file and upload it to Google Sheets, ensuring a more consistent time interval when reading the thermocouple sensor.

<img src="https://github.com/CytronTechnologies/CM4-Maker-Board-MAX6675-Google-Sheets/blob/main/Pictures/4_flow_diagram_advanced_thermocouple_cm4_maker_board.jpg" width="600"> 

## Documentation  
For more information on the CM4 Maker Board, check out the datasheet here:  
* [CM4 Maker Board Datasheet](https://docs.google.com/document/d/1XmZSR81IN70pndZ2odBmlZgAufiIBawVdKZ71C7101Y/edit#)  

## Support  
You can visit [Log Thermocouple Sensor Data to Google Sheets using CM4 Maker Board](https://cytron.io/tutorial/log-thermocouple-sensor-data-to-google-sheets-using-cm4-maker-board) to learn more about it. 

If you need further assistance, we welcome you to our [technical forum](http://forum.cytron.io) or you can contact us through email support@cytron.io where our team will be happy to assist you. 

Let's start building with CM4 Maker Board!
