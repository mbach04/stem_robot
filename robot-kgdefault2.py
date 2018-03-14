#!/usr/bin/env python

import Adafruit_PCA9685
import usb.core
import usb.util
import time
import os
import numpy as np


# ===========================================================================
#
# KINGS GRANT STEM ROBOT 5/31/16
# DEFAULT PROGRAMMING
# Added Green (Channel8) & Red (Channel9) LED function
# Added Servo 13 option for Tandem Arm use
# Added HP Wired Keyboard support
# Changed speed 0 from 338/378 to 158/558
# Added Insignia Keypad support
# Added speed red light and changed main loop function
# 4/25 Added iPazzPort Keyboard device
# ===========================================================================

# Initialise the PWM device using the default address
pwm = Adafruit_PCA9685.PCA9685()

# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)


servoMin = 107  # Was 158 Min pulse length out of 4096
servoStop = 307 # Was 358
servoMax = 507  # Was 558 Max pulse length out of 4096
speed = 10
count=0
i=60
pause=0
tack=0
jitter=0
BTN_J_ACTIVE=0
onesec=0
fivesec=0
fiveseccount=0
updown=1
speedcount=0

pwm.set_pwm_freq(50)                        # Set frequency to 50 Hz

USB_VENDOR  = 0x0c45 # Rii
USB_PRODUCT = 0x7000 # Mini Wireless Keyboard

USB_IF      = 0 # Interface
USB_TIMEOUT = 5 # Timeout in MS

BTN_W     = 26		#W
BTN_X     = 27		#X
BTN_A     = 4		#A
BTN_D     = 7		#D

BTN_Q     = 20		#Q
BTN_E     = 8		#E
BTN_Z     = 29		#Z
BTN_C     = 6		#C

BTN_U	  = 24		#U
BTN_J	  = 13		#J
BTN_O     = 18		#O
BTN_L     = 15		#L

BTN_LEFT  = 80		#<-
BTN_RIGHT = 79		#->

BTN_1	  = [30]	#1
BTN_2	  = [31]	#2
BTN_3	  = [32]	#3
BTN_4	  = [33]	#4
BTN_5	  = [34]	#5
BTN_6	  = [35]	#6
BTN_7	  = [36]	#7
BTN_8	  = [37]	#8
BTN_9	  = [38]	#9
BTN_0	  = [39]	#0


BTN_STOP  = 44 		# Space
BTN_EXIT  = 41 		# ESC


#Insignia 19 Key Keypad
if usb.core.find(idVendor=0x1a2c, idProduct=0x0e24) != None:
  dev = usb.core.find(idVendor=0x1a2c, idProduct=0x0e24)

  BTN_W 	= 96		#W
  BTN_X     	= 90		#X
  BTN_A     	= 92		#A
  BTN_D     	= 94		#D

  BTN_Q     	= 95		#Q
  BTN_E     	= 97		#E
  BTN_Z     	= 89		#Z
  BTN_C     	= 91		#C
  
  BTN_U		= 85		#U
  BTN_J		= 84		#J
  BTN_O   	= 87		#O
  BTN_L 	= 86		#L
  
  BTN_LEFT  	= 98		#<-
  BTN_RIGHT 	= 99		#->

  BTN_1	  	= [83,89]	#1
  BTN_2	  	= [83,90]	#2
  BTN_3	  	= [83,91]	#3
  BTN_4	  	= [83,92]	#4
  BTN_5	  	= [83,93]	#5
  BTN_6	  	= [83,94]	#6
  BTN_7	  	= [83,95]	#7
  BTN_8	  	= [83,96]	#8
  BTN_9	  	= [83,97]	#9
  BTN_0	  	= [83,98]	#0

  BTN_STOP  	= 93 		# Space
  BTN_EXIT  	= 41 		# ESC

#iPazzPort Keyboard
elif usb.core.find(idVendor=0xc40, idProduct=0x8000):
  dev = usb.core.find(idVendor=0xc40, idProduct=0x8000)

  BTN_W	= 26	#W
  BTN_X	= 27	#X
  BTN_A	= 4		#A
  BTN_D	= 7		#D

  BTN_Q	= 20	#Q
  BTN_E	= 8		#E
  BTN_Z	= 29	#Z
  BTN_C	= 6		#C

  BTN_U = 24		#U
  BTN_J	= 13		#J
  BTN_O	= 18		#O
  BTN_L = 15		#L

  BTN_LEFT = 80		#<-
  BTN_RIGHT	= 79	#->

  BTN_1	= [30]	#1
  BTN_2	= [31]	#2
  BTN_3	= [32]	#3
  BTN_4	= [33]	#4
  BTN_5	= [34]	#5
  BTN_6	= [35]	#6
  BTN_7	= [36]	#7
  BTN_8	= [37]	#8
  BTN_9	= [38]	#9
  BTN_0	= [39]	#0

  BTN_STOP = 44 		# Space
  BTN_EXIT = 41 		# ESC

else:
  dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

print dev
print "\nKGROBOT 5/31/16 DEFAULT\n"

endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
  dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

control = [1]*7
while True:
    try:
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
#        if np.count_nonzero(control)==0:
#           BTN_J_ACTIVE=0

        pwm.set_pwm(0, 0, servoStop)
        pwm.set_pwm(1, 0, servoStop)
        pwm.set_pwm(2, 0, servoStop)
        pwm.set_pwm(3, 0, servoStop)
        pwm.set_pwm(13, 0, servoStop)
        pwm.set_pwm(14, 0, servoStop)
        pwm.set_pwm(15, 0, servoStop)

        print(control,BTN_J_ACTIVE,np.count_nonzero(control))
    except:
        pass


    if BTN_STOP in control:
      if BTN_D in control:
        pwm.set_pwm(1, 0, servoMax)
        pwm.set_pwm(3, 0, servoMin)
        if tack<10:              
          pwm.set_pwm(0, 0, servoMin)
          pwm.set_pwm(2, 0, servoMax)
        else:
          pwm.set_pwm(0, 0, servoMax)
          pwm.set_pwm(2, 0, servoMin)

      if BTN_A in control:
        pwm.set_pwm(1, 0, servoMin)
        pwm.set_pwm(3, 0, servoMax)
        if tack<10:              
          pwm.set_pwm(0, 0, servoMin)
          pwm.set_pwm(2, 0, servoMax)
        else:
          pwm.set_pwm(0, 0, servoMax)
          pwm.set_pwm(2, 0, servoMin)

      if BTN_W in control:
        pwm.set_pwm(0, 0, servoMin)
        pwm.set_pwm(2, 0, servoMax)
        if tack<10:              
          pwm.set_pwm(1, 0, servoMin)
          pwm.set_pwm(3, 0, servoMax)
        else:
          pwm.set_pwm(1, 0, servoMax)
          pwm.set_pwm(3, 0, servoMin)

      if BTN_X in control:
        pwm.set_pwm(0, 0, servoMax)
        pwm.set_pwm(2, 0, servoMin)
        if tack<10:              
          pwm.set_pwm(1, 0, servoMin)
          pwm.set_pwm(3, 0, servoMax)
        else:
          pwm.set_pwm(1, 0, servoMax)
          pwm.set_pwm(3, 0, servoMin)

    else:

      if BTN_D in control:
        pwm.set_pwm(1, 0, servoMax)
        pwm.set_pwm(3, 0, servoMin)

      if BTN_A in control:
        pwm.set_pwm(1, 0, servoMin)
        pwm.set_pwm(3, 0, servoMax)

      if BTN_W in control:
        pwm.set_pwm(0, 0, servoMin)
        pwm.set_pwm(2, 0, servoMax)

      if BTN_X in control:
        pwm.set_pwm(0, 0, servoMax)
        pwm.set_pwm(2, 0, servoMin)


    if BTN_C in control:
      pwm.set_pwm(0, 0, servoMax)
      pwm.set_pwm(2, 0, servoMin)
      pwm.set_pwm(1, 0, servoMax)
      pwm.set_pwm(3, 0, servoMin)

    if BTN_Q in control:
      pwm.set_pwm(0, 0, servoMin)
      pwm.set_pwm(2, 0, servoMax)
      pwm.set_pwm(1, 0, servoMin)
      pwm.set_pwm(3, 0, servoMax)

    if BTN_Z in control:
      pwm.set_pwm(0, 0, servoMax)
      pwm.set_pwm(2, 0, servoMin)
      pwm.set_pwm(1, 0, servoMin)
      pwm.set_pwm(3, 0, servoMax)

    if BTN_E in control:
      pwm.set_pwm(0, 0, servoMin)
      pwm.set_pwm(2, 0, servoMax)
      pwm.set_pwm(1, 0, servoMax)
      pwm.set_pwm(3, 0, servoMin)


#    if BTN_1 in control:
    if set(BTN_1).issubset(set(control)):
      servoMin = 303  # Min pulse length out of 4096
      servoMax = 311  # Max pulse length out of 4096
      speed = 1

#    if BTN_2 in control:
    if set(BTN_2).issubset(set(control)):
      servoMin = 301  # Min pulse length out of 4096
      servoMax = 313  # Max pulse length out of 4096
      speed = 2

#    if BTN_3 in control:
    if set(BTN_3).issubset(set(control)):
      servoMin = 299  # Min pulse length out of 4096
      servoMax = 315  # Max pulse length out of 4096
      speed = 3

#    if BTN_4 in control:
    if set(BTN_4).issubset(set(control)):
      servoMin = 297  # Min pulse length out of 4096
      servoMax = 317  # Max pulse length out of 4096
      speed = 4

#    if BTN_5 in control:
    if set(BTN_5).issubset(set(control)):
      servoMin = 295  # Min pulse length out of 4096
      servoMax = 319  # Max pulse length out of 4096
      speed = 5

#    if BTN_6 in control:
    if set(BTN_6).issubset(set(control)):
      servoMin = 293  # Min pulse length out of 4096
      servoMax = 321  # Max pulse length out of 4096
      speed = 6

#    if BTN_7 in control:
    if set(BTN_7).issubset(set(control)):
      servoMin = 291  # Min pulse length out of 4096
      servoMax = 323  # Max pulse length out of 4096
      speed = 7

#    if BTN_8 in control:
    if set(BTN_8).issubset(set(control)):
      servoMin = 289  # Min pulse length out of 4096
      servoMax = 325  # Max pulse length out of 4096
      speed = 8

#    if BTN_9 in control:
    if set(BTN_9).issubset(set(control)):
      servoMin = 266  # Min pulse length out of 4096
      servoMax = 348  # Max pulse length out of 4096
      speed = 9

#    if BTN_0 in control:
    if set(BTN_0).issubset(set(control)):
      servoMin = 107  # Min pulse length out of 4096
      servoMax = 507  # Max pulse length out of 4096
      speed = 10

    if BTN_LEFT in control:
      pwm.set_pwm(0, 0, servoMin)
      pwm.set_pwm(1, 0, servoMin)
      pwm.set_pwm(2, 0, servoMin)
      pwm.set_pwm(3, 0, servoMin)

    if BTN_RIGHT in control:
      pwm.set_pwm(0, 0, servoMax)
      pwm.set_pwm(1, 0, servoMax)
      pwm.set_pwm(2, 0, servoMax)
      pwm.set_pwm(3, 0, servoMax)

#Servo 15 is the Arm
#Servo 13 is the second servo for Arm if installed
    if BTN_O in control:
      pwm.set_pwm(15, 0, servoMin)
      pwm.set_pwm(13, 0, servoMax)


    if BTN_L in control:
      pwm.set_pwm(15, 0, servoMax)
      pwm.set_pwm(13, 0, servoMin)


#Servo 14 is the Release
    if BTN_U in control:
      pwm.set_pwm(14, 0, servoMin)
      if jitter>4:
        pwm.set_pwm(15, 0, 303)
      else:
        pwm.set_pwm(15, 0, 311)
  
    if BTN_J in control:
      pwm.set_pwm(14, 0, servoMax)
      if jitter>4:
        pwm.set_pwm(15, 0, 301)
      else:
        pwm.set_pwm(15, 0, 313)

        
     
#SHIFT, SHIFT, ESC, DEL
#Does not work for HP Keyboard
    if 34 in control and 229 in control and 66 in control and 42 in control and 225 in control and 41 in control:
      pwm.set_pwm(0, 0, servoStop)
      pwm.set_pwm(1, 0, servoStop)
      pwm.set_pwm(2, 0, servoStop)
      pwm.set_pwm(3, 0, servoStop)
      pwm.set_pwm(13, 0, servoStop)
      pwm.set_pwm(14, 0, servoStop)
      pwm.set_pwm(15, 0, servoStop)
      pwm.set_pwm(8, 0, 0)
      pwm.set_pwm(9, 0, 4000)
      os.system('shutdown now -h')

    if 83 in control and 86 in control and 98 in control and 88 in control:
      pwm.set_pwm(0, 0, servoStop)
      pwm.set_pwm(1, 0, servoStop)
      pwm.set_pwm(2, 0, servoStop)
      pwm.set_pwm(3, 0, servoStop)
      pwm.set_pwm(13, 0, servoStop)
      pwm.set_pwm(14, 0, servoStop)
      pwm.set_pwm(15, 0, servoStop)
      pwm.set_pwm(8, 0, 0)
      pwm.set_pwm(9, 0, 4000)
      os.system('shutdown now -h')

    if BTN_EXIT in control and BTN_STOP in control:
      pwm.set_pwm(0, 0, servoStop)
      pwm.set_pwm(1, 0, servoStop)
      pwm.set_pwm(2, 0, servoStop)
      pwm.set_pwm(3, 0, servoStop)
      pwm.set_pwm(13, 0, servoStop)
      pwm.set_pwm(14, 0, servoStop)
      pwm.set_pwm(15, 0, servoStop)
      pwm.set_pwm(8, 0, 0)
      pwm.set_pwm(9, 0, 0)
      usb.util.release_interface(dev,USB_IF)
      dev.attach_kernel_driver(USB_IF)
      exit()

    if 86 in control and 87 in control and 88 in control:
      pwm.set_pwm(0, 0, servoStop)
      pwm.set_pwm(1, 0, servoStop)
      pwm.set_pwm(2, 0, servoStop)
      pwm.set_pwm(3, 0, servoStop)
      pwm.set_pwm(13, 0, servoStop)
      pwm.set_pwm(14, 0, servoStop)
      pwm.set_pwm(15, 0, servoStop)
      pwm.set_pwm(8, 0, 0)
      pwm.set_pwm(9, 0, 0)
      usb.util.release_interface(dev,USB_IF)
      dev.attach_kernel_driver(USB_IF)
      exit()

            
    
    pwm.set_pwm(8, 0, count)
    count=count+i
    if count>4000:
      i=-60
    if count<60:
      if pause<25:
        pause=pause+1
        i=0
      else:
        i=60
        pause=0
    

    onesec=onesec+updown  #When @ 50 = 1 second
    fivesec=fivesec+fiveseccount
    if onesec>=10:
      pwm.set_pwm(9,0,4000)
      updown=-1
    if onesec<=0:
      pwm.set_pwm(9,0,0)
      updown=1
      speedcount=speedcount+1
    if speedcount>=speed:
      onesec=1
      updown=0
      fivesec=0
      fiveseccount=1
      speedcount=0
    if fivesec>=50:
      updown=1
      fivesec=0
      fiveseccount=0




    tack=tack+1
    if tack>20:
      tack=0

    if jitter<9:
      jitter=jitter+1
    else:
      jitter=0



    time.sleep(0.02)






