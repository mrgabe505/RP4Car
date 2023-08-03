'''
code pulled from following links
https://www.digikey.com/en/maker/blogs/2021/how-to-control-servo-motors-with-a-raspberry-pi
https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/
https://www.winkleink.com/2013/04/raspberry-pi-unipolar-stepper-motors.html
'''

import RPi.GPIO as GPIO
from time import sleep
import os, sys, pygame
from pygame import locals
from gpiozero import Servo

servo = Servo(8)  #gpio pin 8 controls the servo motor
val = 0  #val is a varible that controls the turning servo, range is -1 to 1, corosponding to left and right

in1 = 4
in2 = 17  #gpio pins connected to each gpio pin
en = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)
p.start(25)

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

pygame.joystick.init()  # main joystick device system

deadZone = 0.1

try:
  j = pygame.joystick.Joystick(0)  # create a joystick instance
  j.init()  # init instance
  print('Enabled joystick: ' + j.get_name())
except pygame.error:
  print('no joystick found.')

while True:
  for e in pygame.event.get():  # iterate over event stack
    if e.type == pygame.locals.JOYAXISMOTION:  # Read Analog Joystick Axis
      turn = j.get_axis(0)  # left thumbstick, will affect turning
      y2, x2 = j.get_axis(5), j.get_axis(4)  #for switch controller fake, left trigger is 2, right trigger is 5. output value is -1 > 1, starts at 0 but defaults to -1
      # for white xbox controller, left trigger is 4, right is 5?
      servo.value = val
      throt = abs(((x2 + 1) * 50)-(y2 + 1) * 50)  #adds 1 to right trigger value, range becomes 0 to 2. Multiplied by 50 to get a range from 0 > 100 for pwm cycle

      if turn < -1 * deadZone:  #turning
        print(turn)
        val = (turn)

      if turn < deadZone and turn > deadZone * -1:  #code for when you need to drive foward
        print(turn)
        val = (turn)

      if turn > deadZone:  #turning
        print(turn)
        val = (turn)

      if x2 < deadZone:
        p.ChangeDutyCycle(0)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.  LOW)
        print('should not be moving')

      if throt > deadZone:
        print(throt)
        p.ChangeDutyCycle(throt)
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)  #this works
