import time
from datetime import datetime
import board
import busio
import adafruit_adxl34x
from pymongo import MongoClient, errors
from gpiozero import LED, Button
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# GPIO Pin and Mongo URL setup
LED_PIN = 17
BUTTON_PIN = 18  
MONGO_URI = "mongodb+srv://joushuaW:connectiab330@cluster0.3xsua.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize GPIO, I2C and sensor
led = LED(LED_PIN)
button = Button(BUTTON_PIN)
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_adxl34x.ADXL343(i2c)

# Start MongoDB connection
try:
    client = MongoClient(MONGO_URI)
    db = client["HAR_db"]
    data_collection = db["acce_data"]
    logging.info("Connected to MongoDB successfully.")
except errors.ConnectionError as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    exit(1)

# MongoDB Transmission state
state = "INACTIVE"

# Grab accelerometer data from the sensor
def collect_data():
    measurements = {"x_values": [], "y_values": [], "z_values": []}
    start_time = datetime.now()
    
    try:
        for i in range(60):  #Collect 60 samples
            x, y, z = sensor.acceleration
            measurements["x_values"].append(x)
            measurements["y_values"].append(y)
            measurements["z_values"].append(z)
            time.sleep(1/20)  # Collect at 20Hz
        logging.info("Data collection completed.")
    except Exception as e:
        logging.error(f"Error collecting data from sensor: {e}")
        return None, None
    
    return measurements, start_time

# Upload accelerometer data
def upload_data(measurements, start_time):
    if measurements is None:
        logging.warning("No data to upload due to previous errors.")
        return

    document = {
        "timestamp": start_time,
        "x_values": measurements["x_values"],
        "y_values": measurements["y_values"],
        "z_values": measurements["z_values"],
        "User": user,
        "Movement_label": movementID,
        "Session_ID": sessionID,
    }
    
    try:
        data_collection.insert_one(document)
        logging.info("Data uploaded to MongoDB successfully.")
    except Exception as e:
        logging.error(f"Error uploading data to MongoDB: {e}")


# Detect button press
def handle_button_press():
    global state
    if state == "INACTIVE":
        state = "ACTIVE"
        led.on()
        logging.info("Transitioned to ACTIVE state.")
    else:
        state = "INACTIVE"
        led.off()
        logging.info("Transitioned to INACTIVE state.")

# Setup session
user = input("Who is starting the current session?\n")
sessionID = input("What is the current session?\n")
movementID = input("What is the movement type being performed?\n")

# Component Validation
logging.info("Commencing Component Validation\n")

if input("Skip validation(Y or N)").upper() == "N":
    logging.info("LED TESTING")
    for i in range(3):
        time.sleep(0.5)
        led.on()
        time.sleep(0.5)
        led.off()

    logging.info("SENSOR TESTING")
    for 
    collect_data()


    print("Please begin ")

# Initialize button
button.when_pressed = handle_button_press

# Main loop: on button press, light LED and send accelerometer data to MongoDB
try:
    while True:
        if state == "ACTIVE":
            start_time = time.time()
            measurements, window_start_time = collect_data()
            
            # Ensure 3 seconds has passed
            while time.time() - start_time < 3.0:
                time.sleep(0.1)
            
            upload_data(measurements, window_start_time)
        else:
            time.sleep(0.1)

except KeyboardInterrupt:
    logging.info("Program terminated by user.")
except Exception as e:
    logging.error(f"Unexpected error: {e}")
finally:
    led.off()
    logging.info("Program exited gracefully.")