from machine import Pin
from config import BTN_PIN

class BUTTON:
    def __init__(self):
        self.pin = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)        
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self._irq_handler)
        self.btn_was_pressed = False

    def _irq_handler(self, pin):
        self.btn_was_pressed = True
    
    def was_pressed(self):
        if self.btn_was_pressed:
            self.btn_was_pressed = False
            return True
        return False
