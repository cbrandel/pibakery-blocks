#!/usr/bin/python

import sys, os, time

openWifi = """

network={
    ssid="WIFI-SSID"
    scan_ssid=1
    key_mgmt=NONE
}
WIFI-COUNTRY"""

wepWifi = """

network={
    ssid="WIFI-SSID"
    scan_ssid=1
    key_mgmt=NONE
    wep_key0="WIFI-PSK"
}
WIFI-COUNTRY"""

wpaWifi = """

network={
    ssid="WIFI-SSID"
    scan_ssid=1
    key_mgmt=WPA-PSK
    psk="WIFI-PSK"
}
WIFI-COUNTRY"""

wifiSSID = sys.argv[1]
wifiPSK = sys.argv[2]
wifiType = sys.argv[3]
wifiCountry = ""
if len(sys.argv) > 3 and sys.argv[4] != "":
    if "-" in sys.argv[4] and sys.argv[4][0:sys.argv[4].find("-")] != "":
        wifiCountry = "country=" + sys.argv[4][0:sys.argv[4].find("-")]
    else:
        wifiCountry = ""

if wifiSSID != "" and wifiType != "":
	if wifiPSK == "" or wifiType == "Open (no password)":
		wifiText = openWifi.replace("WIFI-SSID", wifiSSID).replace("WIFI-COUNTRY", wifiCountry)
	elif wifiType == "WEP":
		wifiText = wepWifi.replace("WIFI-SSID", wifiSSID).replace("WIFI-PSK", wifiPSK).replace("WIFI-COUNTRY", wifiCountry)
	elif wifiType == "WPA/WPA2":
		wifiText = wpaWifi.replace("WIFI-SSID", wifiSSID).replace("WIFI-PSK", wifiPSK).replace("WIFI-COUNTRY", wifiCountry)

with open("/etc/wpa_supplicant/wpa_supplicant.conf", "a") as wifiFile:
	wifiFile.write(wifiText)

os.system("wpa_cli reconfigure")
time.sleep(5)

# It's likely that the block following this one will be one that uses the
# internet - such as a download file or apt-get block. It takes a few seconds
# for the WiFi to connect and obtain an IP address, run the waitForNetwork shell
# script, which will loop waiting for a network connection (timeout 150 seconds)
# and continue once there is one
os.system("chmod +x /boot/PiBakery/blocks/wifisetup/waitForNetwork.sh")
os.system("/boot/PiBakery/blocks/wifisetup/waitForNetwork.sh")
