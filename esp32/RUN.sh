#!/bin/bash
PORT='/dev/ttyUSB0'
PUSHCMD="ampy --port $PORT put "
CURDIR=$(pwd)
TOPDIR=${CURDIR%/*}

# Enter your path to your WLAN configuration file here, see ../wlan/wlanconfig.py for example
echo "Loading configs"
$PUSHCMD ~/secrets/wlanconfig.py
echo "Loading software"
$PUSHCMD ssd1306.py
$PUSHCMD textout.py
$PUSHCMD wlan.py
$PUSHCMD main.py

echo "Resetting board"
timeout 2  ampy --port $PORT run reset.py
