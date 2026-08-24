# WLAN Variables
# Replace WLAN_SSID and WLAN_PASSWORD with the network parameters to which the WiNet-S communication module is connnected.
# Consider if you communication module is in the guest network. Than the paramters must belong to the same subnet. 
WLAN_SSID 		= "your_WLAN_name"
WLAN_PASSWORD 	= "your_WLAN_password"

# MODBUS Variables
INVERTER_IP = "192.168.179.1"  		# Your WiNet-S IP address
MODBUS_PORT = 502

# WEATHER Variables
HOME_LATITUDE 				= 52.52	# latitude of your solar system
HOME_LONGITUDE 				= 13.41 # longitude of your solar system

MIN_DIRECT_RADIATION_SUN 	= 5		# threshold value to which the weather is considered cloudy (measured in W/m^2)

# PINS: do not change if you use my PCB
BTN_PIN 	= 4
DS18B20_PIN = 10
PHOTO_PIN 	= 26
SCL_PIN 	= 17
SDA_PIN 	= 16
