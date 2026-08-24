from RGB1602 import RGB1602
from connection import SUN, CLOUD
import time

# ICON CONSTANTS LOCATIONS in CG RAM
# used on both pages
SUN_LEFT 		= 0
SUN_RIGHT 		= 1
HOME_LEFT 		= 2		
HOME_RIGHT 		= 3		

# Solar page
BATTERY 		= 4	
WEATHER_LEFT 	= 5
WEATHER_RIGHT 	= 6	

# Temperature page
ARROW_UP 		= 4
ARROW_DOWN 		= 5
DEGREE_CELSIUS	= 6

# PAGE DEFINITION
ENERGY = 0
TEMPERATURE = 1

class DISPLAY:
    #=============== INIT ===============#
    def __init__(self):
        
        self.rgb1602 = RGB1602(16,2)
     
        # ICONS displayed on both pages
        self.generateSunChars()
        self.generateHomeChars()
        
        self.currentPage = ENERGY
        
        # ENERGY PAGE SETUP
        self.energyData_last = [bytearray(b" "*16), bytearray(b" "*16)]
        
        self.batteryIcon_last = [0x0E,0x1B,0x11,0x11,0x11,0x11,0x11,0x1F]
        self.rgb1602.createChar(BATTERY, self.batteryIcon_last)
        self.stateOfCharge_last = 0
        
        self.weatherStatus_last = SUN
        self.generateWeatherChar_sunny()
        
        # TEMPERATURE PAGE SETUP
        self.tempData_last = [bytearray(b" "*16), bytearray(b" "*16)]
        
        # BRIGHTNESS
        self.pwm_signal_last = 0
        
    #=============== ICONS ===============#
    def generateBatteryChar(self, charge):
        batteryIcon = [0x0E,0x1B,0x11,0x11,0x11,0x11,0x11,0x1F]
        fullBars = int(charge / 18.75)
        for i in range(fullBars):
            batteryIcon[6-i] = 0x1F
        rest = (charge % 18.75)
        if (fullBars % 2) == 0:
            if rest >= 6.25:
                batteryIcon[6-fullBars] = 0x19
            if rest >= 12.5:
                batteryIcon[6-fullBars] = 0x1d
        else:
            if rest >= 6.25:
                batteryIcon[6-fullBars] = 0x13
            if rest >= 12.5:
                batteryIcon[6-fullBars] = 0x17 
        if charge == 100:
            batteryIcon[1] = 0x1f   
        return batteryIcon
        
    def generateWeatherChar_sunny(self):
        self.rgb1602.createChar(WEATHER_LEFT , [0x00, 0x04, 0x01, 0x03, 0x0B, 0x03, 0x01, 0x04])
        self.rgb1602.createChar(WEATHER_RIGHT, [0x10, 0x02, 0x18, 0x1C, 0x1D, 0x1C, 0x18, 0x02])
        
    def generateWeatherChar_cloudy(self):
        self.rgb1602.createChar(WEATHER_LEFT , [0x00, 0x01, 0x03, 0x0F, 0x1F, 0x1F, 0x0F, 0x00])
        self.rgb1602.createChar(WEATHER_RIGHT, [0x00, 0x18, 0x1C, 0x1E, 0x1E, 0x1E, 0x1C, 0x00])
        
    def generateSunChars(self):
        self.rgb1602.createChar(SUN_LEFT , [0x1F, 0x1F, 0x1E, 0x1E, 0x19, 0x04, 0x10, 0x12])
        self.rgb1602.createChar(SUN_RIGHT, [0x0C, 0x00, 0x10, 0x04, 0x00, 0x10, 0x08, 0x00])
        
    def generateHomeChars(self):
        self.rgb1602.createChar(HOME_LEFT , [0x00, 0x01, 0x03, 0x07, 0x0F, 0x07, 0x06, 0x06])
        self.rgb1602.createChar(HOME_RIGHT, [0x00, 0x00, 0x10, 0x18, 0x1C, 0x18, 0x18, 0x18])
    
    #=============== DATA UPDATE LOGIC ===============#
    def _byteArray_EnergyData(self, data):
        
        energyData_b = [bytearray(b"\x00\x01              "),
                        bytearray(b"\x02\x03           % \x04")]
        
        production = data["production"]
        forecastChange_h = data["forecastChange_h"]
        consumption = data["consumption"]
        stateOfCharge = data["stateOfCharge"]
        
        ### PRODUCTION
        if production >= 10000:
            p = str(round(production/1000, 1)) + "kW"
        elif production >= 1000:
            p = str(round(production/1000, 1)) + " kW"
        else:
            p = str(int(production)) + " W"
        
        ### FORECAST CHANGE
        if int(forecastChange_h/24) > 99:
            f = "99h"
        elif forecastChange_h >= 24:
            f = str(int(forecastChange_h/24)) + "d"
        else:   
            f = str(forecastChange_h) + "h"
        
        ### CONSUMPTION
        if consumption >= 10000:
            c = str(round(consumption/1000, 1)) + "kW"
        elif consumption >= 1000:
            c = str(round(consumption/1000, 1)) + " kW"
        else:
            c = str(int(consumption)) + " W"
        
        ### STATE OF CHARGE
        s = str(int(stateOfCharge))
        
        energyData_b[0][3:3+len(p)] 			= p.encode('utf-8')			# production
        energyData_b[0][13-len(f):15-len(f)] 	= bytearray(b"\x05\x06")	# weather icon
        energyData_b[0][16-len(f):] 			= f.encode('utf-8')			# forcast change

        energyData_b[1][3:3+len(c)] 			= c.encode('utf-8')			# consumption
        energyData_b[1][13-len(s):13] 			= s.encode('utf-8')			# state of charge
        
        return energyData_b
    
    def _update_EnergyIcons(self, data):
        # UPDATE BATTERY ICON (only if changed)
        if int(data["stateOfCharge"]) != int(self.stateOfCharge_last):
            batteryIcon_new = self.generateBatteryChar(data["stateOfCharge"])
            if batteryIcon_new != self.batteryIcon_last:
                self.rgb1602.createChar(BATTERY, batteryIcon_new)
                self.batteryIcon_last = batteryIcon_new
        
        # UPDATE WEATHER ICON (only if changed)
        if data["weatherStatus"] != self.weatherStatus_last:
            if data["weatherStatus"] == SUN:
                self.generateWeatherChar_sunny()
            else:
                self.generateWeatherChar_cloudy()
            self.weatherStatus_last = data["weatherStatus"]
        
    def _byteArray_TempData(self, data):
        
        tempData_b = [	bytearray(b"\x00\x01             \x04"),
                        bytearray(b"\x02\x03             \x05")]
        
        t_o 	= str(int(data["temp_outdoor"])) + "\x06C"
        t_i 	= str(int(data["temp_indoor"])) 	+ "\x06C"
        t_min 	= str(int(data["temp_min"])) 	+ "\x06C"
        t_max 	= str(int(data["temp_max"])) 	+ "\x06C"
        
        tempData_b[0][3:3+len(t_o)] = t_o.encode('utf-8')
        tempData_b[0][14-len(t_max):14] = t_max.encode('utf-8')
        tempData_b[1][3:3+len(t_i)] = t_i.encode('utf-8')
        tempData_b[1][14-len(t_min):14] = t_min.encode('utf-8')
        
        return tempData_b
    
    def _update_chars(self, new_data, last_data):
        for i in range(16):
            if new_data[0][i] != last_data[0][i]:
                self.rgb1602.setCursor(i,0)
                self.rgb1602.write(new_data[0][i])
            if new_data[1][i] != last_data[1][i]:
                self.rgb1602.setCursor(i,1)
                self.rgb1602.write(new_data[1][i])
    
    ##=============== MAIN FUNTIONALITY ===============#
    def update(self, data) :
        
        energyData_b 	= self._byteArray_EnergyData(data)
        tempData_b 		= self._byteArray_TempData(data)
                
        # UPDATE everything
        if self.currentPage == ENERGY:
            self._update_EnergyIcons(data)
            new_data = energyData_b
            last_data = self.energyData_last
        else:
            new_data = tempData_b
            last_data = self.tempData_last
        
        self._update_chars(new_data, last_data)
        
        self.energyData_last = energyData_b
        self.tempData_last = tempData_b
        
     
    def toggle(self):
        
        if self.currentPage == ENERGY:
            
            self.rgb1602.createChar(ARROW_UP, [0x00, 0x04, 0x0E, 0x15, 0x04, 0x04, 0x04, 0x00])
            self.rgb1602.createChar(ARROW_DOWN , [0x00, 0x04, 0x04, 0x04, 0x15, 0x0E, 0x04, 0x00])
            self.rgb1602.createChar(DEGREE_CELSIUS , [0x0E, 0x0A, 0x0E, 0x00, 0x00, 0x00, 0x00, 0x00])
        
            self._update_chars(self.tempData_last, self.energyData_last)
            
            self.currentPage = TEMPERATURE
            
        else:
            self.rgb1602.createChar(BATTERY, self.batteryIcon_last)
            
            if self.weatherStatus_last == SUN:
                self.generateWeatherChar_sunny()
            else:
                self.generateWeatherChar_cloudy()
            
            self._update_chars(self.energyData_last, self.tempData_last)
            
            self.currentPage = ENERGY
     
    def setRGB(self,r,g,b):
        self.rgb1602.setRGB(r,g,b)
            
    def clear(self):
        self.rgb1602.clear()
    
    def _set_brightness(self,brightness):
        max_pwm = 190
        min_pwn = 1
        
        # max_brigthness = 100, min_brightness = 0
        ### Raw map() = 
        # (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        #  x * (max_pwm - min_pwn) / 100 + min_pwn
        
        pwm_signal = brightness * (max_pwm - min_pwn) / 100 + min_pwn

        return int(pwm_signal)
    
   
    
    def _brightness_transition(self, r, g, b, pwm_signal): #r,g,b = 0 or 1 
        
        if pwm_signal == self.pwm_signal_last:
            return

        steps = 2
        if (pwm_signal - self.pwm_signal_last) < 0:
            steps = -steps
        
        for pwm in range(self.pwm_signal_last, pwm_signal, steps):
            self.rgb1602.setRGB(r * pwm ,g * pwm,b * pwm)
            time.sleep(0.05) 
        
        self.pwm_signal_last = pwm_signal
        
    def update_color(self, production, consumption, battery_failure, brightness):
        r, g, b = 0, 0, 0
        
        pwm_signal = self._set_brightness(brightness)
            
        ### RED
        if battery_failure:
            self.rgb1602.setRGB(self.pwm_signal_last,0,0)
            self._brightness_transition(1,0,0, pwm_signal)
            return
         
        ### GREEN
        if production > consumption:
            self.rgb1602.setRGB(0,self.pwm_signal_last,0)
            self._brightness_transition(0,1,0, pwm_signal)
            return
        
        ### BLUE
        self.rgb1602.setRGB(self.pwm_signal_last,self.pwm_signal_last,self.pwm_signal_last)
        self._brightness_transition(1,1,1, pwm_signal)
        
    
    def write_text(self, row1, row2=""):
        self.rgb1602.clear()
        
        self.rgb1602.setCursor(0,0)
        self.rgb1602.printout(row1)
        self.rgb1602.setCursor(0,1)
        self.rgb1602.printout(row2)
