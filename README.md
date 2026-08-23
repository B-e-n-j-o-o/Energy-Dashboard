# Energy-Dashboard
   A display that visualizes your household’s and photovoltaic's energy data, weather forecast and temperature. The dynamic backlight...
   ```
   GREEN 🟢: PV Production > household's consumption 
   BLUE  🔵: PV Production < household's consumption 
   RED   🔴: battery fuse blown
   ```
   ...allows you to adjust your energy consumption in real time (cooking, do the laundry). This module helps you manage your household more sustainably and, as a result, save on your electricity costs. Additionally, if you regularly struggle with battery failures caused by blown fuses of the battery system (as I and my father do), the backlight allows you to react quickly. 
   
# Displayed data 
  1. electricity produced by the photovoltaic system 
  2. electricity consumed by the household
  3. current weather
   ```
   SUN   ☀️: direct solar radiation > threshold (preset: 5 W/m² => threshold can be set in config.py)
   CLOUD ☁️: direct solar radiation <= threshold 
   ```  
  5. forecast change: predicted time until the weather changes (e.g "☀️ 3h" means: the direct solar radiation is under the threshold value in 3h). This helps you to estimate how long your PV system is producing electricity.
  6. battery level 🔋
  7. outdoor temperature
  8. indoor temperatur
  9. todays maximum outdoor temperature
  10. todays minimum outdoor temperature

Press the button to switch between the two pages. The photoresistor is used for dynamically adjusting the brightness of the backlight to the room brightness. 

# Underlying Technology  
The module is powered by an Raspberry Pi Pico 2W which executes a task scheduler. The household's energy data is retrieved via Modbus TCP from the Sungrow communication module WiNet-S. Except the indoor temperature (detected with a Temperature Sensor) the weather related date is requested from the free Weather API [Open-Meteo](https://open-meteo.com/). 

# If you want one - build it
**Required Tools:**
  - soldering iron
  - 3D printer
  - motivation and a little bit of money :-)

**Required Products**  
  - 1x Raspberry Pi Pico 2W
  - 2x through-hole 01x20 female pin sockets
  - 1x Waveshare's LCD1602 RGB Module
  - 1x 01x04 2.54mm screw terminal
  - 1x photoresistor
  - 1x DS18B20 temperature sensor
  - 4x M3 40mm screws + screw-nuts
  - 1x right angled tactile switch
  - 1x custom PCB (I purchased it on JLCPCB) (gerber files coming soon)
  - 1x custom 3D printed case (get files [here](https://github.com/B-e-n-j-o-o/Energy-Dashboard/3d_files) or on [Onshape](https://cad.onshape.com/documents/fe910dcf5090e09b129dc4b0/w/445839dbb3f75b7a6e49436a/e/11c19a83d04b76eda0bfc8fb?renderMode=0&uiState=6a8b52e7040663373746c148))

The physical assembly will be self-explanatory from the pictures (coming soon)... Good luck :-) 

**Software:**Download the micropython files from the src folder (coming soon) and upload them to the Pi Pico using the Thonny IDE (click [here](https://www.instructables.com/Uploading-Code-With-Thonny/) for a tutorial). 

# Build Intentions
This display was build at my fathers request. He asked for a device that provides all essential information at a glance, without having to log in to a cell phone or an app.

For this project, I exclusively used AI as a programming tutor and for web search. I assume it's crucial to understand underlying concepts before you can become a better (vibe-)programmer that can use AI on a larger scale responsibly. 

Since I'm not near a professional software developer don't use this code unless you have checked it yourself. 
