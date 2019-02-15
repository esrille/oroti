#!/usr/bin/python3
# -*- coding: utf-8 -*-

真 = True
偽 = False

import RPi.GPIO


# 主体: GPIO
class GPIO:
    def __init__(self, pin):
        self.pin = pin
        self.mode = RPi.GPIO.IN
        RPi.GPIO.setwarnings(False)
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(pin, self.mode)

    # GPIOを　ハイにします、とは。
    def ハイにします(self):
        if self.mode == RPi.GPIO.IN:
            self.mode = RPi.GPIO.OUT
            RPi.GPIO.setup(self.pin, self.mode)
        RPi.GPIO.output(self.pin, RPi.GPIO.HIGH)

    # GPIOを　ローにします、とは。
    def ローにします(self):
        if self.mode == RPi.GPIO.IN:
            self.mode = RPi.GPIO.OUT
            RPi.GPIO.setup(self.pin, self.mode)
        RPi.GPIO.output(self.pin, RPi.GPIO.LOW)

    # GPIOが　ハイです、とは。
    def ハイです(self):
        if self.mode == RPi.GPIO.OUT:
            self.mode = RPi.GPIO.IN
            RPi.GPIO.setup(self.pin, self.mode)
        return RPi.GPIO.input(self.pin) == RPi.GPIO.HIGH


GPIO1 = GPIO(34)
GPIO2 = GPIO(35)
GPIO3 = GPIO(36)


class ライト:

    def default(self):
        if ひと.います():
            self.スイッチ.いれます()
        else:
            self.スイッチ.きります()


class スイッチ:

    def いれます(self):
        self.GPIO.ハイにします()

    def きります(self):
        self.GPIO.ローにします()


class ひと:

    def います(self):
        return GPIO3.ハイです()

ライト1 = ライト()
ライト2 = ライト()
スイッチ1 = スイッチ()
スイッチ2 = スイッチ()
ひと = ひと()
スイッチ1.GPIO = GPIO1
スイッチ2.GPIO = GPIO2
ライト1.スイッチ = スイッチ1
ライト2.スイッチ = スイッチ2

while True:
    ライト1.default()
    ライト2.default()
