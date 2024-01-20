# Projekat iz predmeta Projektovanje elektronskih sistema
Merenje potrošnje DC motora pomoću INA219 senzora. DC motor se kontroliše pomoću L298N H-mosta.

## Sadržaj
 - [Datasheet-ovi](#datasheet-ovi)
 - [Poslednja dobra verzija](#poslednja-dobra-verzija)
 - [Povezivanje](#povezivanje)
 - [Potrebne modifikacije](#potrebne-modifikacije)
 - [NodeRed flow](#nodered-flow)
 - [NodeRed dashboard](#nodered-dashboard)
 - [Dodatni pomoćni linkovi](#dodatni-pomocni-linkovi)

## Datasheet-ovi
- [L298 Datasheet](https://www.sparkfun.com/datasheets/Robotics/L298_H_Bridge.pdf)
- [INA219 Datasheet](https://www.ti.com/lit/ds/symlink/ina219.pdf?ts=1703659644578&ref_url=https%253A%252F%252Fwww.google.com%252F)

## Poslednja dobra verzija
[Ovde](https://github.com/andras168/PES_Projekat/blob/main/projekat_l298_ina219_thingspeak_v4.py)

## Povezivanje

<img src="https://github.com/andras168/PES_Projekat/blob/main/Slike/Povezivanje_Raspberry.jpg?raw=true" align="center" width="1000">

## Potrebne modifikacije

Potrebno je bar jedan keramički kondenzator od 0.1uF zalemiti paralelno sa priključcima DC motora. Tako možemo eliminisati elektromagnetske smetnje DC motora u nekoj meri.

Više o tome na [ovom](http://www.stefanv.com/rcstuff/qf200005.html) linku.

## NodeRed flow

<img src="https://github.com/andras168/PES_Projekat/blob/main/Slike/Screenshot_20240113_152050.png?raw=true" align="center" width="1000">

## NodeRed dashboard

<img src="https://github.com/andras168/PES_Projekat/blob/main/Slike/Screenshot_20240114_125452.png?raw=true" align="center" width="1000">

## Dodatni pomoćni linkovi
- [Raspberry Pi INA219 Tutorial ](https://www.rototron.info/raspberry-pi-ina219-tutorial/)
- [Raspberry Pi L298N Interface Tutorial](https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/)
- [Voltage spikes when driving DC motor with N-channel MOSFET](https://electronics.stackexchange.com/questions/143755/voltage-spikes-when-driving-dc-motor-with-n-channel-mosfet)




