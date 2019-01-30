# -*- coding: utf-8 -*-

import RPi.GPIO


class GPIO:
    def __init__(self, pin):
        self.pin = pin
        self.mode = RPi.GPIO.IN
        RPi.GPIO.setwarnings(False)
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(pin, self.mode)

    # ハイにします、とは、
    def ハイにします(self):
        if self.mode == RPi.GPIO.IN:
            self.mode = RPi.GPIO.OUT
            RPi.GPIO.setup(self.pin, self.mode)
        RPi.GPIO.output(self.pin, RPi.GPIO.HIGH)

    # ローにします、とは、
    def ローにします(self):
        if self.mode == RPi.GPIO.IN:
            self.mode = RPi.GPIO.OUT
            RPi.GPIO.setup(self.pin, self.mode)
        RPi.GPIO.output(self.pin, RPi.GPIO.LOW)

    # ハイです、とは、
    def ハイです(self):
        if self.mode == RPi.GPIO.OUT:
            self.mode = RPi.GPIO.IN
            RPi.GPIO.setup(self.pin, self.mode)
        return RPi.GPIO.input(self.pin) == RPi.GPIO.HIGH


GPIO1 = GPIO(34)
GPIO2 = GPIO(35)
GPIO3 = GPIO(36)
