# Energy-Dashboard
   A display that shows your household’s energy data, the weather forecast and the temperature. The dynamic backlight (GREEN: generation > consumption | BLUE: consumption > generation) allows you to adjust your energy consumption to save electricity. If you regularly struggle with battery failures caused by blown fuses (as I do), the backlight (RED: battery fuse blown) allows you to react quickly. This module helps you manage your household more sustainably and, as a result, save on your electricity costs. 

# Displayed data and other features
  1. production of the photovoltaic system in W
  2. consumption of the househould in W
  3. forcast change: the icon (sun/cloud) displays the current weather (determined via direct solar radiation in W/m^2 => threshold can be set in config.py)

# Underlying Technology  
The module is powered by an Raspberry Pi Pico 2W which executes a scheduler. The household's energy data is retrieved via Modbus TCP from the Sungrow communication module WiNet-S. Except the indoor temperature the weather related date is requested from the free Weather API ((Open-Meteo)[https://open-meteo.com/]). 


# If you want one - build it
## Required Tools 
  - soldering iron
  - 3D printer
  - motivation and a little bit of money :-)
## Required Products  
  - 1x Raspberry Pi Pico 2W
  - 2x through-hole 01x20 female pin sockets
  - 1x Waveshare's LCD1602 RGB Module
  - 1x Photoresitor
  - 1x DS18B20 temperature sensor
  - 4x M3 40mm srews + srew-nuts
  - 1x PCB (I purchased it on JLCPCB) (gerber files coming soon)
  - 1x 3D printed case (three parts)
The assembly will be self-explanatory from the pictures (coming soon)... Good luck :-) 
