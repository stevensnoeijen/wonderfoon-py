#!/bin/bash

mount /dev/sda /mnt || mount /dev/sda1 /mnt || mount -t exfat /dev/sda /mnt || mount -t exfat /dev/sda1 /mnt || mount -t ntfs /dev/sda /mnt || mount -t ntfs /dev/sda1 /mnt || exit 0

aplay music/usb-stick-detected.wav
for f in volume.json
do
	cp /mnt/$f /home/pi/wonderfoon-py
done
cp /mnt/*.wav /home/pi/wonderfoon-py/music

wifi=0
if test -f /mnt/wpa_supplicant.conf
then
	cp /mnt/wpa_supplicant.conf /etc/wpa_supplicant
	wifi=1
fi
umount /mnt
aplay music/verwijder.wav
sleep 1
aplay music/verwijder.wav
sleep 1
aplay music/verwijder.wav
sleep 1

if test $wifi -eq 1
then
	sleep 3
	sync
	reboot
fi
