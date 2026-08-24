import network
import urequests
import sys
import socket
import ntptime
import time

from config import WLAN_SSID, WLAN_PASSWORD
from config import INVERTER_IP, MODBUS_PORT
from config import HOME_LATITUDE, HOME_LONGITUDE, MIN_DIRECT_RADIATION_SUN

max_tries_wlan = 5
# Function returns True if wlan is connected and False if WLAN not available.
def connectWLAN():		
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if wlan.isconnected():
        return True
            
    wlan.connect(WLAN_SSID, WLAN_PASSWORD)
    for _ in range(max_tries_wlan):			
        if wlan.status() >= 3: 	# if wlan is connected 
            return True
        time.sleep(1)
    
    print("WLAN CONNNTECTION FAILED")
    return False

max_tries_ntptime = 3
# Function syncs the microcontrollers time to the real time. True: successful; False: not successful.
def sync_clock():
    for _ in range(max_tries_ntptime):
        try:
            ntptime.settime()	# syncs time lib to real time
            return True
        except Exception as e:
            time.sleep(0.5)
    return False

# The following functions requests energy data from the WiNet-S communication module. It returns True if data request was successful and False if not. 
# 
# Documentation for data addresses of the communication module:
# https://forum.iobroker.net/assets/uploads/files/1739613340960-f2a8971f-a3b9-4dc1-8608-a7d3d3001a9e-communication.protocol.of.residential.hybrid.inverter_v1.1.2_en.pdf
#
# StateOfCharge:    86 Battery level    13023           U16         0.1%             13023 - 1 => hex: \x32\xde
# Consumption:      77 Load power       13008-13009     S32         1W               13008 - 1 => hex: \x32\xCF
# Production:       21 Total DC power   5017-5018       U32         W                5017  - 1 => hex: \x13\x98
# Battery Failue:   119 BMS fault 1     13074~13075     U32                                            \x33\x11
# 
# MODBUS TCP PACKET
#   Transaktionsnummer	    Protokollkennzeichen	Zahl der noch folgenden Bytes	Adresse	    Funktion(https://de.wikipedia.org/wiki/Modbus)	Daten
#   2 Byte	                2 Byte (immer 0x0000)	2 Byte (n + 2)	                1 Byte	    1 Byte	                                        n Byte
#   \x00\x01                \x00\x00                \x00\x06                        \x01        \x04                                            register address    count   
#                                                                                                                                               \x13\x87            \x00\x01
# the WiNet-S uses little-endian for double-word data. Big-endian for byte data;
# => 32bit data must be converted; therefore r[11:13]+r[9:11]

max_tries_modbus = 3
def request_inverter_via_modbus():

    data = {"consumption": None, "production": None, "stateOfCharge": None,"batteryFailure":None}

    for _ in range(max_tries_modbus):
        s = None
        try: 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.5)
            s.connect((INVERTER_IP, MODBUS_PORT))

            # Battery Level
            if data["stateOfCharge"] == None:
                s.sendall(b"\x00\x01\x00\x00\x00\x06\x01\x04\x32\xDE\x00\x01")
                r = s.recv(1024)
                data["stateOfCharge"] = int(int.from_bytes(r[9:11]) * 0.1)

            # Consumption
            if data["consumption"] == None:
                s.sendall(b"\x00\x01\x00\x00\x00\x06\x01\x04\x32\xCF\x00\x02")
                r = s.recv(1024)
                data["consumption"] = int.from_bytes(r[11:13]+r[9:11], True)

            # PV Production
            if data["production"] == None:
                s.sendall(b"\x00\x01\x00\x00\x00\x06\x01\x04\x13\x98\x00\x02")
                r = s.recv(1024)
                data["production"] = int.from_bytes(r[11:13]+r[9:11])

            # Battery Failure
            if data["batteryFailure"] == None:
                s.sendall(b"\x00\x01\x00\x00\x00\x06\x01\x04\x33\x11\x00\x02")
                r = s.recv(1024)
                if int.from_bytes(r[11:13]+r[9:11]) > 0: data["batteryFailure"] = True
                else: data["batteryFailure"] = False

            return data
        
        except Exception as e:
            pass
            
        finally:
            if s: s.close()
    return False

url = f"https://api.open-meteo.com/v1/forecast?latitude={HOME_LATITUDE}&longitude={HOME_LONGITUDE}&hourly=direct_radiation&minutely_15=temperature_2m&daily=temperature_2m_max,temperature_2m_min"

#WEATHER STATUS VARIABLES
SUN = 0
CLOUD = 1

def getWeather():  			# returns if weather is cloudy or  sunny + how long it will stay so 
    
    ### TIME
    currentTime = time.localtime()			# returns utc+0 
    currentHour = currentTime[3]
    currentMinute = currentTime[4]
    
    ### DATA
    try:
        response = urequests.get(url)
        
        if response.status_code != 200: 
            print(f"WEATHER - STATUS CODE: {response.status_code}")
            return False
        
        weatherData = response.json()
    
    except Exception as e:
        print(f"WEATHER: {e}")
        print(response.text)
        return False
    
    finally:
        if response:
            response.close()
    
    ### WEATHER STATUS
    hourlyRadiation = weatherData["hourly"]["direct_radiation"]
    
    currentRaditation = hourlyRadiation[currentHour+1] # +1 cause the values are calculated from the preceding hour
    
    if currentRaditation <= MIN_DIRECT_RADIATION_SUN: 
        weatherStatus = CLOUD
    else:
        weatherStatus = SUN
    
    ### FORECAST CHANGE
    nextRadiations = hourlyRadiation[currentHour+1:]

    forecastChange = 0

    if weatherStatus == SUN:
        for i, cloudCover in enumerate(nextRadiations):
            if cloudCover < MIN_DIRECT_RADIATION_SUN:
                forecastChange = i
                break

    if weatherStatus == CLOUD:
        for i, cloudCover in enumerate(nextRadiations):
            if cloudCover >= MIN_DIRECT_RADIATION_SUN:
                forecastChange = i
                break
    
    weatherDic = {"weatherStatus": weatherStatus,
                  "forecastChange_h": forecastChange,
                  "temp_outdoor": weatherData["minutely_15"]["temperature_2m"][currentHour*4+int(currentMinute/15)],
                  "temp_min": weatherData["daily"]["temperature_2m_min"][0],
                  "temp_max": weatherData["daily"]["temperature_2m_max"][0]}   
    
    return weatherDic
