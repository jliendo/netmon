from time import sleep

import RPi.GPIO as GPIO


def on_off(times, delay):
    for i in range(times):
        GPIO.output(13, True)
        sleep(delay)
        GPIO.output(13, False)
        sleep(delay)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)

on_off(3, 0.5)
on_off(10, 0.1)
