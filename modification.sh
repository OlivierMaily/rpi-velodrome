#!/bin∕bash
cd '/media/f24a4949-f4b2-4cad-a780-a138695079ec/home/pi' 
sudo rm cpia_velodrome.py
sudo wget https://raw.githubusercontent.com/Regulvar-OM/rpi-velodrome/775cee379eaaaea8119ea7d65801b855cb7607cd/cpia_velodrome.py
sudo umount /dev/mmcblk0p1
sudo umount /dev/mmcblk0p2
