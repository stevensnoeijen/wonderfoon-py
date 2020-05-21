#!/bin/bash


mount /dev/sda /mnt || mount /dev/sda1 /mnt || exit 0
for f in newstuff.sh action.json music.json t65 run volume.json config.json
do
	cp /mnt/$f /home/pi/wonderfoond
done
cp /mnt/*.wav /home/pi/wonderfoond/music
cp /mnt/*.ogg /home/pi/wonderfoond/music
cp /mnt/*.mp3 /home/pi/wonderfoond/music

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
