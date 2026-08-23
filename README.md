# Energy-Dashboard
   A display that shows your household’s energy data, the weather forecast and the temperature. The dynamic backlight (GREEN: electricity production by photovoltaic system > household's consumption | BLUE: consumption > production) allows you to adjust your energy consumption to save electricity. If you regularly struggle with battery failures caused by blown fuses (as I and my father do), the backlight (RED: battery fuse blown) allows you to react quickly. This module helps you manage your household more sustainably and, as a result, save on your electricity costs. 

## Displayed data 
  1. electricity production of the photovoltaic system 
  2. electricity consumption of the household
  3. current weather: icon (☀️ or ☁️) displays the current weather (determined via direct solar radiation in W/m² => threshold can be set in config.py)
  4. forecast change: predicted time until the weather changes (e.g "☀️ 3h" means: the direct solar radiation is under the threshold value in 3h). This helps you to estimate how long your PV system is producing electricity.
  5. battery level
  7. outdoor temperature
  8. indoor temperatur
  9. todays maximum outdoor temperature
  10. todays minimum outdoor temperature

Press the button to switch between the two pages. The photoresistor is used for dynamically adjusting the brightness of the backlight to the room brightness. 

## Underlying Technology  
The module is powered by an Raspberry Pi Pico 2W which executes a scheduler. The household's energy data is retrieved via Modbus TCP from the Sungrow communication module WiNet-S. Except the indoor temperature (detected with a Temperature Sensor) the weather related date is requested from the free Weather API [Open-Meteo](https://open-meteo.com/). 

## If you want one - build it
**Required Tools:**
  - soldering iron
  - 3D printer
  - motivation and a little bit of money :-)

**Required Products**  
  - 1x Raspberry Pi Pico 2W
  - 2x through-hole 01x20 female pin sockets
  - 1x Waveshare's LCD1602 RGB Module
  - 1x photoresistor
  - 1x DS18B20 temperature sensor
  - 4x M3 40mm screws + screw-nuts
  - 1x right angled tactile button
  - 1x PCB (I purchased it on JLCPCB) (gerber files coming soon)
  - 1x 3D printed case (get files [here](https://github.com/B-e-n-j-o-o/Energy-Dashboard/3d_files) or on [Onshape](https://cad.onshape.com/documents/fe910dcf5090e09b129dc4b0/w/445839dbb3f75b7a6e49436a/e/11c19a83d04b76eda0bfc8fb?renderMode=0&uiState=6a8b52e7040663373746c148))

The assembly will be self-explanatory from the pictures (coming soon)... Good luck :-) 

# Build Intentions
This display was build at my fathers request. He asked for a device that provides all essential information at a glance without the need to log into a mobile phone or an app. 
