import os
from time import sleep
from ina219 import INA219
import paho.mqtt.client as mqtt
import json

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
ina = INA219(busnum=1, shunt_ohms=SHUNT_OHMS, max_expected_amps=MAX_EXPECTED_AMPS, address=ADDRESS)
ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)

def read():
    ina_v = round(ina.voltage(),2)
    ina_c = round(ina.current(),2)
    ina_p = round(ina.power(),2)
    
    print("Bus Voltage    : %.2f V" % ina.voltage())
    print("Bus Current    : %.2f mA" % ina.current())
    print("Supply Voltage : %.2f V" % ina.supply_voltage())
    print("Shunt voltage  : %.2f mV" % ina.shunt_voltage())
    print("Power          : %.2f mW" % ina.power())
    print("______________________________")
    
    return ina_v, ina_c, ina_p

def send_mqtt_data():
    client.publish('ina_voltage', str(ina_v))
    client.publish('ina_current', str(ina_c))
    client.publish('ina_power', str(ina_p))
    
while 1:
    ina_v, ina_c, ina_p = read()
    send_mqtt_data()
    sleep(1)

