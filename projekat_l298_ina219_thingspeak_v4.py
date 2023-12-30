import os
from time import sleep
import threading
from ina219 import INA219
import paho.mqtt.client as mqtt
import json
import RPi.GPIO as GPIO
import requests

GPIO.setwarnings(False)

in1 = 17 #GPIO 17
in2 = 27 #GPIO 27
en_a = 4 #GPIO 4

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

# Shared variable to control motor start/stop
motor_control_command = None

def on_pwm_control(client, userdata, msg):
    pwm_value = int(msg.payload)
    #print(f"Received PWM control value: {pwm_value}")
    print(f"[PWM] -> {pwm_value}")
    power_a.ChangeDutyCycle(pwm_value)

def on_start_motor(client, userdata, msg):
    global motor_control_command
    #print("Received start command. Starting the motor.")
    motor_control_command = 'start'

def on_stop_motor(client, userdata, msg):
    global motor_control_command
    #print("Received stop command. Stopping the motor.")
    motor_control_command = 'stop'

def on_forward_motor(client, userdata, msg):
    global motor_control_command
    #print("Motor turning forward.")
    motor_control_command = 'forward'


def on_backward_motor(client, userdata, msg):
    global motor_control_command
    #print("Motor turning backward.")
    motor_control_command = 'backward'

def read_ina():
    while True:
        ina_v, ina_c, ina_p = read()
        send_mqtt_data(ina_v, ina_c, ina_p)
        client.loop()  # Process incoming MQTT messages
        sleep(1)

def motor_control():
    global motor_control_command
    while motor_running:
        if motor_control_command == 'start':
            # Start motor, turning forward
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            power_a.ChangeDutyCycle(10)
            motor_control_command = None  # Reset the command
            print('[Motor] -> START')
        elif motor_control_command == 'stop':
            # Stop motor
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            motor_control_command = None  # Reset the command
            print('[Motor] -> STOP')
        
        elif motor_control_command == 'forward':
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            sleep(1)
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            motor_control_command = None
            print('[Motor] -> TURN FORWARD - CW')
        
        elif motor_control_command == 'backward':
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            sleep(1)
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            motor_control_command = None
            print('[Motor] -> TURN BACKWARD - CCW')


def read():
    ina_v = round(ina.voltage(), 2)
    ina_c = round(ina.current(), 2)
    ina_p = round(ina.power(), 2)

    # print("Bus Voltage    : %.2f V" % ina.voltage())
    # print("Bus Current    : %.2f mA" % ina.current())
    # print("Supply Voltage : %.2f V" % ina.supply_voltage())
    # print("Shunt voltage  : %.2f mV" % ina.shunt_voltage())
    # print("Power          : %.2f mW" % ina.power())
    # print("______________________________")
    ina_c_ampere = round(ina_c / 1000, 2);
    ina_p_watt = round(ina_p / 1000,2);

    thingspeak_url_voltage = f'https://api.thingspeak.com/update?api_key=7PUEH5VLH8DQZ1Q4&field1={ina_v}&field2={ina_c_ampere}&field3={ina_p_watt}'

    try:
        response = requests.get(thingspeak_url_voltage)
        print(f"Data sent to ThingSpeak: {ina_v}")
        print(f"Data sent to ThingSpeak: {ina_c_ampere}")
        print(f"Data sent to ThingSpeak: {ina_p_watt}")

    except requests.RequestException as e:
        print(f"Error sending data to ThingSpeak: {e}")

    return ina_v, ina_c_ampere, ina_p_watt

def send_mqtt_data(ina_v, ina_c, ina_p):
    client.publish('ina_voltage', str(ina_v))
    client.publish('ina_current', str(ina_c))
    client.publish('ina_power', str(ina_p))


# Set up MQTT message handlers
client.on_message = on_pwm_control
client.message_callback_add('start_motor', on_start_motor)
client.message_callback_add('stop_motor', on_stop_motor)
client.message_callback_add('motor_forward', on_forward_motor)
client.message_callback_add('motor_backward', on_backward_motor)

# Subscribe to the relevant topics
client.subscribe('pwm_control')
client.subscribe('start_motor')
client.subscribe('stop_motor')
client.subscribe('motor_forward')
client.subscribe('motor_backward')

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
