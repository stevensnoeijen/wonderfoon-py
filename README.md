# wonderfoon-py
> :warning: Dit project is in ontwikkeling :warning:

Python implementatie voor wonderfoon.nl 1.4.

Waarom Python? Omdat ik het project werkend wil krijgen op een pi zero en Python wil leren.
Voor de audio gebruik ik: https://nl.aliexpress.com/item/32704994250.html

Ik ben niet de eigenaar van wonderfoon.nl, dit project is ge-forked op wonderfoon 1.4 en implementeerd de software in python.
Zie http://wonderfoon.nl/

## Handmatige installatie

Volg de installatie uit methode 1 of 2 van http://wonderfoon.nl/WONDERFOON-v1.4.pdf

Zorg dat je Rasbian (Raspberry Pi OS) Lite (zonder desktop) hebt geinstalleerd: https://www.raspberrypi.org/downloads/raspberry-pi-os/

Log in de terminal en voer de volgende stappen uit:

1. Pi specifiek:
Open raspi-config `sudo raspi-config`.

Stel audio jack in als default via `Advanced Options` > `A4 Audio` > `1 Headphones`.

Daarna selecteer de optie update.

2. Zorg dat het os up to date is:
```
sudo apt-get -y upgrade && sudo apt-get -y update
```

3. installeer dependencies: 

```
sudo apt-get install -y git python3-pip python3-dev libasound2-dev python3-gpiozero python-pyaudio python3-pyaudio ntfs-3g portaudio19-dev
pip3 install --upgrade pip setuptools
```

4. download code 
```
cd /home/pi/
git clone https://github.com/stevensnoeijen/wonderfoon-py.git
cd wonderfoon-py
chmod +x t65.py run newstuff.sh
```

5. stel audio in volgens https://www.raspberrypi-spy.co.uk/2019/06/using-a-usb-audio-device-with-the-raspberry-pi/

6. installeer requirements: 
```
sudo pip3 install -r requirements.txt
```

7. stel config in `cp config.json-rotator config.json` 

8. handmatig start applicatie:
```
sudo python3 ./t65.py
```
Sluit het af door ctrl+c.

9. Automatisch starten van de applicatie bij het starten van de pi, open `sudo nano /etc/rc.local`.

Voer boven de `exit 0` het volgende stukje code toe `rm -f nohup.out; nohup /home/pi/wonderfoon-py/run &`. 
Dit zorgt ervoor dat het script `run` word uitgevoerd bij het starten van de pi.


## Development

Ik ontwikkel op het moment het script lokaal en sync dir naar de pi.
Op de pi loopt een script om het python script te herstarten als het bestand word opgeslagen:

`while inotifywait -e close_write t65.py; do python3 ./t65.py; done`

Alleen rotator is geimplementeerd atm.
Alleen wav 16bit is op het moment geimplementeerd.

> install https://github.com/inotify-tools/inotify-tools/wiki

limitations:
Alleen maar .wav files voor nu!

Getest op rasberry pi zero 1.3.

Todo: 

- test usb met nieuwe muziek en json's
- test wav audio formats
- fix volume naar 100%
- dhcp uit newstuff.sh?
- gebruikershandleiding maken
- test handmatige installatie
- maak automatische installatie script
- implement mp3 & ogg