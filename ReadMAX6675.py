import RPi.GPIO as GPIO
import time

#GPIO.cleanup()
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM) # Broadcom pin
GPIO.setwarnings(False)

class Thermocouple:
    def __init__(self, CS, SCK, SO, UNIT):
        self.cs = CS
        self.sck = SCK
        self.so = SO
        self.unit = UNIT
        
        # set pin number for communicate with MAX6675 
        GPIO.setup(self.cs, GPIO.OUT, initial = GPIO.HIGH)
        GPIO.setup(self.sck, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(self.so, GPIO.IN)
 

    def read_temp(self):
        
        GPIO.output(self.cs, GPIO.LOW)
        time.sleep(0.002)
        GPIO.output(self.cs, GPIO.HIGH)
        time.sleep(0.22)

        GPIO.output(self.cs, GPIO.LOW)
        GPIO.output(self.sck, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.sck, GPIO.LOW)
        self.Value = 0
        for i in range(11, -1, -1):
            GPIO.output(self.sck, GPIO.HIGH)
            self.Value = self.Value + (GPIO.input(self.so) * (2 ** i))
            GPIO.output(self.sck, GPIO.LOW)

        GPIO.output(self.sck, GPIO.HIGH)
        error_tc = GPIO.input(self.so)
        GPIO.output(self.sck, GPIO.LOW)

        for i in range(2):
            GPIO.output(self.sck, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(self.sck, GPIO.LOW)

        GPIO.output(self.cs, GPIO.HIGH)

        if self.unit == 0: # Raw data
            self.temp = self.Value  
        if self.unit == 1: # Convert to Celsius
            self.temp = self.Value * 0.23
        if self.unit == 2: # Convert to Fahrenheit
            self.temp = self.Value * 0.23 * 9.0 / 5.0 + 32.0

        if error_tc != 0:
            return -self.cs
        else:
            return round(self.temp, 2)  # return with round 2 decimal places


if __name__ == "__main__":
    # set the pin for communicate with MAX6675
    # GPIO Num
    cs_1 = 12
    sck_1 = 5
    so_1 = 6
    
    cs_2 = 13
    sck_2 = 23
    so_2 = 24
    
    # max6675.set_pin(CS, SCK, SO, unit) [unit : 0 - raw, 1 - Celsius, 2 - Fahrenheit]
    thermo_1 = Thermocouple(cs_1, sck_1, so_1, 1)
    thermo_2 = Thermocouple(cs_2, sck_2, so_2, 1)
    
    try:
        while True:
            # read temperature 
            data_thermo_1 = thermo_1.read_temp()
            data_thermo_2 = thermo_2.read_temp()
            # print temperature
            print (f"Thermocoupler 1: {data_thermo_1} , Thermocoupler 2: {data_thermo_2}")

            time.sleep(2)
    except KeyboardInterrupt:
        pass
