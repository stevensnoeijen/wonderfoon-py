# wonderfoon-py
Python implementatie voor wonderfoon.nl 1.4.

Waarom Python? Omdat ik het project werkend wil krijgen op een pi zero en Python wil leren.
Voor de audio gebruik ik: https://nl.aliexpress.com/item/32704994250.html

__Dit project is in ontwikkeling__

Ik ben niet de eigenaar van wonderfoon.nl, dit project is ge-forked op wonderfoon 1.4 en implementeerd de software in python.
Zie http://wonderfoon.nl/

## Handmatige installatie

Volg de installatie uit methode 1 of 2 van http://wonderfoon.nl/WONDERFOON-v1.4.pdf

Zorg dat je Rasbian (Raspberry Pi OS) Lite (zonder desktop) hebt geinstalleerd: https://www.raspberrypi.org/downloads/raspberry-pi-os/

Log in de terminal en voer de volgende stappen uit:

1. installeer python3: https://wolfpaulus.com/raspberry-pi-zero-w-w-python-3/

2. set python als default `alias python='/usr/bin/python3.4'`

3. installeer os dependencies:
```
sudo apt-get install -y python3-dev libasound2-dev

pip3 install --upgrade pip setuptools
```

4. installeer git:
```
sudo apt-get update

sudo apt-get install git
```

5. download code 
```
cd /home/pi/
git clone https://github.com/stevensnoeijen/wonderfoon-py.git
```

6. installeer requirements: 
```
cd wonderfoon-py
sudo pip3 install -r requirements.txt
```

7. handmatig start applicatie:
```
python ./t65.py
```
Sluit het af door ctrl+c.

8. Automatisch starten van de applicatie bij het starten van de pi, open `sudo nano /etc/rc.local`.

Voer boven de `exit 0` het volgende stukje code toe `rm -f nohup.out; nohup /home/pi/wonderfoond/run &`. 
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

- test pulling power-cable
- update startup script
- test handmatige installatie
- maak automatische installatie script
- implement mp3 & ogg