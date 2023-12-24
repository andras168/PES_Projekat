import os
from time import sleep
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
power_a.start(10) ##### WARNING! ##### Do not set it above 40, for 3V DC motor and 6V power supply. It will damage the motor!

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

#--- MQTT server parameters ---
SERVER = '192.168.1.125'
#------------------------------

#--- INA219 parameters ---
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 3
ADDRESS = 0x40
#-------------------------

client = mqtt.Client()
client.connect(SERVER, 1883, 60)

#https://github.com/chrisb2/pi_ina219/blob/master/README.md
# ina = INA219(busnum=1, shunt_ohms=SHUNT_OHMS, max_expected_amps=MAX_EXPECTED_AMPS, address=ADDRESS)
# ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)

# def read():
#     ina_v = round(ina.voltage(),2)
#     ina_c = round(ina.current(),2)
#     ina_p = round(ina.power(),2)
#     
#     print("Bus Voltage    : %.2f V" % ina.voltage())
#     print("Bus Current    : %.2f mA" % ina.current())
#     print("Supply Voltage : %.2f V" % ina.supply_voltage())
#     print("Shunt voltage  : %.2f mV" % ina.shunt_voltage())
#     print("Power          : %.2f mW" % ina.power())
#     print("______________________________")
#     
#     return ina_v, ina_c, ina_p
# 
# def send_mqtt_data():
#     client.publish('ina_voltage', str(ina_v))
#     client.publish('ina_current', str(ina_c))
#     client.publish('ina_power', str(ina_p))
    
while(True):
    user_input = input()
    
    if user_input == 'f':
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        sleep(1)
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    
    elif user_input == 'b':
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)       
        sleep(1)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        
    elif user_input == 's':
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        print("Motor stopped.")
    
    elif user_input == 'm':
        power_a.start(40)
    elif user_input == 'l':
        power_a.start(10)
    elif user_input == 'h':
        power_a.start(25)


        
#     ina_v, ina_c, ina_p = read()
#     send_mqtt_data()
    sleep(1)

