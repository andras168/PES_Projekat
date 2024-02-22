# Projekat iz predmeta Projektovanje elektronskih sistema
<div align="justify"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Projekat ima kao osnovni cilj da iskoristi potencijal Raspberry Pi 4 mini računara, NodeRED i Thingspeak platforme u merenju potrošnje elektromotora jednosmerne struje. Integracija ove kombinacije tehnologija omogućava efikasno praćenje i analizu energetske efikasnosti elektromotora u raznim aplikacijama.</div> <br>
<div align="justify"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Raspberry Pi 4 mini računar, kao glavna komponenta projekta, pruža mogućnost integracije različitih senzora i pokretačkih kola. Ključni elementi sistema uključuju INA219 senzor za merenje struje i napona potrošača, omogućavajući precizno i kontinuirano praćenje potrošnje energije elektromotora. Pored toga, L298N drajver se koristi za kontrolu elektromotora - kontrolu smera okretanja i prilagođavanje brzine rada. Node-RED i Thingspeak platforma se koristi za jednostavnu implementaciju logike upravljanja i vizualizaciju podataka.</div>
 
## Sadržaj
 - [Datasheet-ovi](#datasheet-ovi)
 - [Poslednja dobra verzija](#poslednja-dobra-verzija)
 - [Povezivanje](#povezivanje)
 - [Potrebne modifikacije](#potrebne-modifikacije)
 - [NodeRed flow](#nodered-flow)
 - [NodeRed dashboard](#nodered-dashboard)
 - [Dodatni pomoćni linkovi](#dodatni-pomoćni-linkovi)

## Datasheet-ovi
- [L298 Datasheet](https://www.sparkfun.com/datasheets/Robotics/L298_H_Bridge.pdf)
- [INA219 Datasheet](https://www.ti.com/lit/ds/symlink/ina219.pdf?ts=1703659644578&ref_url=https%253A%252F%252Fwww.google.com%252F)

## Poslednja dobra verzija
[Ovde](https://github.com/andras168/PES_Projekat/blob/main/projekat_l298_ina219_thingspeak_v4.py)

## Povezivanje

<img src="https://github.com/andras168/PES_Projekat/blob/main/Slike/Povezivanje_Raspberry.jpg?raw=true" align="center" width="1000">

## Potrebne modifikacije

Potrebno je bar jedan blok kondenzator od 0.1uF zalemiti paralelno sa priključcima DC motora. Tako možemo eliminisati elektromagnetske smetnje DC motora u nekoj meri.

Više o tome na [ovom](http://www.stefanv.com/rcstuff/qf200005.html) linku.

## NodeRed flow

<img src="https://github.com/andras168/PES_Projekat/blob/main/Slike/Screenshot_20240113_152050.png?raw=true" align="center" width="1000">

## NodeRed dashboard

<img src="https://github.com/andras168/PES_Projekat/blob/main/Slike/Screenshot_20240114_125452.png?raw=true" align="center" width="1000">

## Korisni linkovi
- [NodeRed Documentation](https://nodered.org/docs/)
- [Raspberry Pi INA219 Tutorial ](https://www.rototron.info/raspberry-pi-ina219-tutorial/)
- [Raspberry Pi L298N Interface Tutorial](https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/)
- [Voltage spikes when driving DC motor with N-channel MOSFET](https://electronics.stackexchange.com/questions/143755/voltage-spikes-when-driving-dc-motor-with-n-channel-mosfet)




