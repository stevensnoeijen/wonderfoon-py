# wonderfoon-py
Python implementatie voor wonderfoon.nl 1.4.

Waarom Python? Omdat ik het project werkend wil krijgen op een pi zero en Python wil leren.

__Dit project is in ontwikkeling__

Ik ben niet de eigenaar van wonderfoon.nl, dit project is ge-forked op wonderfoon 1.4 en implementeerd de software in python.

> Manual voor http://wonderfoon.nl/WONDERFOON-v1.4.pdf

## Run

### Installatie

https://wolfpaulus.com/raspberry-pi-zero-w-w-python-3/

`alias python='/usr/bin/python3.4'`

```
pip3 install --upgrade pip setuptools
pip3 install wheel
pip3 install pydub
pip3 install ffmpeg-python
sudo apt-get install -y python3-dev libasound2-dev
pip3 install simpleaudio
```

### Development

Ik ontwikkel op het moment het script lokaal en sync dir naar de pi.
Op de pi loopt een script om het python script te herstarten als het bestand word opgeslagen:

`while inotifywait -e close_write t65.py; do python3 ./t65.py; done`

Alleen rotator is geimplementeerd atm.
Alleen wav 16bit is op het moment geimplementeerd.

> install https://github.com/inotify-tools/inotify-tools/wiki

Todo: 

- implement volume.json
- check cpu usage
- test pulling power-cable
- remove start message?
- update startup script
- maak install manual
- implement mp3 & ogg