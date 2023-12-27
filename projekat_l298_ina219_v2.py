import os
from time import sleep
import threading
from ina219 import INA219
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

in1 = 17
in2 = 27
en_a = 4

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en_a, GPIO.OUT)

power_a = GPIO.PWM(en_a, 100)
power_a.start(10)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

# MQTT server parameters
SERVER = '192.168.1.125'

# INA219 parameters
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 3
ADDRESS = 0x40

# Initialize INA sensor
ina = INA219(busnum=1, shunt_ohms=SHUNT_OHMS, max_expected_amps=MAX_EXPECTED_AMPS, address=ADDRESS)
ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)

# MQTT client
client = mqtt.Client()
client.connect(SERVER, 1883, 60)

# Flag to control the motor thread
motor_running = True

def on_pwm_control(client, userdata, msg):
    pwm_value = int(msg.payload)
    print(f"Received PWM control value: {pwm_value}")
    power_a.ChangeDutyCycle(pwm_value)

def on_start_motor(client, userdata, msg):
    print("Received start command. Starting the motor.")
    power_a.start(10) #Setting duty cycle to initial value of 10
    user_inbut = 'b';

def on_stop_motor(client, userdata, msg):
    print("Received stop command. Stopping the motor.")
    power_a.stop()
    user_input = 's';



def read_ina():
    while True:
        ina_v, ina_c, ina_p = read()
        send_mqtt_data(ina_v, ina_c, ina_p)
        client.loop()  # Process incoming MQTT messages
        sleep(1)

def motor_control():
    while motor_running:
        user_input = input()
        
        if user_input == 'f':
            # Motor forward logic
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            sleep(1)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
        
        elif user_input == 'b':
            # Motor backward logic
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)       
            sleep(1)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            
        elif user_input == 's':
            # Stop motor
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            print("Motor stopped.")
        
        elif user_input == 'm':
            power_a.start(40)
        elif user_input == 'l':
            power_a.start(10)
        elif user_input == 'h':
            power_a.start(25)

def read():
    ina_v = round(ina.voltage(), 2)
    ina_c = round(ina.current(), 2)
    ina_p = round(ina.power(), 2)
    
    print("Bus Voltage    : %.2f V" % ina.voltage())
    print("Bus Current    : %.2f mA" % ina.current())
    print("Supply Voltage : %.2f V" % ina.supply_voltage())
    print("Shunt voltage  : %.2f mV" % ina.shunt_voltage())
    print("Power          : %.2f mW" % ina.power())
    print("______________________________")
    
    return ina_v, ina_c, ina_p

def send_mqtt_data(ina_v, ina_c, ina_p):
    client.publish('ina_voltage', str(ina_v))
    client.publish('ina_current', str(ina_c))
    client.publish('ina_power', str(ina_p))

# Set up MQTT message handlers
client.on_message = on_pwm_control
client.message_callback_add('start_motor', on_start_motor)
client.message_callback_add('stop_motor' , on_stop_motor)

# Subscribe to the PWM control topic
client.subscribe('pwm_control')
client.subscribe('start_motor')
client.subscribe('stop_motor')


# Create threads
ina_thread = threading.Thread(target=read_ina)
motor_thread = threading.Thread(target=motor_control)

# Start threads
ina_thread.start()
motor_thread.start()

# Wait for threads to finish
ina_thread.join()
motor_running = False
motor_thread.join()
