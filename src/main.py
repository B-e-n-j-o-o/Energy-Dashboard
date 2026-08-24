import time
import sys
import machine

from connection import *
from sensors import Sensors
from Display import DISPLAY
from Button import BUTTON

data =	{
            "consumption": 		0,
            "production": 		0,
            "stateOfCharge": 	0,
            "batteryFailure": 	False,
            "weatherStatus": 	SUN,
            "forecastChange_h": 0,
            "temp_outdoor": 	0,
            "temp_indoor":		0,
            "temp_min": 		0,
            "temp_max": 		4,
            "brightness":		0,
        }       

def errorHandler(errorMessage, exception = None):		# blocks until button press than reboot
    print(errorMessage)
    display.write_text(errorMessage, "PRESS BTN:REBOOT")
    
    with open("log.txt", "a") as file:
        file.write(f"==> {errorMessage}\n")
        
        if exception is not None:
            sys.print_exception(e, file)
            
        file.write("\n")
    
    while True:
        if btn.was_pressed():
            machine.reset()     # Reboot the Pico W
        time.sleep(1)
            
#=============== Network Tasks ===============#
def ensure_WLAN():				
    if not connectWLAN():
        errorHandler("ERR_WLAN_DOWN")
        
def task_inverter_modbus():			
    if not (liveData := request_inverter_via_modbus()): 
        errorHandler("ERR_MODBUS")
        
    data["consumption"] = liveData["consumption"]
    data["production"] = liveData["production"]
    data["stateOfCharge"] = liveData["stateOfCharge"]
    data["batteryFailure"] = liveData["batteryFailure"]
    #print(f"2. {liveData}")

def task_Weather():			
    if not (weather_dictionary := getWeather()): 
        errorHandler("ERR_WEATHER")
        
    #print(f"4. {weather_dictionary}")
    
    data["weatherStatus"] = weather_dictionary["weatherStatus"]
    data["forecastChange_h"] = weather_dictionary["forecastChange_h"]
    data["temp_outdoor"] = weather_dictionary["temp_outdoor"]
    data["temp_min"] = weather_dictionary["temp_min"]
    data["temp_max"] = weather_dictionary["temp_max"]
        
#=============== Sensor Tasks ===============#
s = Sensors()      
def task_read_ds18b20():
    temp_indoor = s.ds18b20()
    #print(f"Temperature: {temp_indoor}")
    data["temp_indoor"] = temp_indoor
    
def task_read_photoresitor():
    brightness = s.photoresitor()
    #print(f"Brightness: {brightness}")
    data["brightness"] = brightness
    
#=============== Display Tasks ===============#
def task_update_display():
    display.update(data)

#=============== Color Tasks ===============#
def task_update_display_color():
    display.update_color(data["production"], data["consumption"], data["batteryFailure"], data["brightness"])
    
#=============== Button Tasks ===============#
    
def task_check_button():
    if btn.was_pressed():
        display.toggle()

#=============== Scheduler ===============#
            
def run_task(task):
    if task.__name__ in ["task_LiveData_Modbus", "task_Weather"]:
        ensure_WLAN()
    task()

tasks = [
    {"function": task_inverter_modbus, 			"interval_s": 10 		, "last_run": 0},
    {"function": task_Weather, 					"interval_s": 120		, "last_run": 0},
    {"function": task_read_ds18b20, 			"interval_s": 10		, "last_run": 0},
    {"function": task_read_photoresitor, 		"interval_s": 2			, "last_run": 0},
    {"function": task_update_display_color,		"interval_s": 2			, "last_run": 0},
    {"function": task_update_display, 			"interval_s": 10		, "last_run": 0},
    {"function": task_check_button, 			"interval_s": 1			, "last_run": 0}
]

def scheduler():
    while True:
        now = time.time()
        for task in tasks:
            
            if now - task["last_run"] >= task["interval_s"]:
                
                run_task(task["function"])
                task["last_run"] = now
        time.sleep(1.0)
        
try:
    time.sleep(1)
    
    display = DISPLAY()
    btn = BUTTON()
    
    display.setRGB(0,100,0)
        
    display.write_text("Solar Dashboard", "build by Benjo")
    time.sleep(2)
    
    ensure_WLAN() 
    
    if not(sync_clock()):
        errorHandler("ERR_NTPTIME")
    
    display.clear()
    
    scheduler()
    
except Exception as e:
    errorHandler("ERR_UNKNOWN", e)
 
