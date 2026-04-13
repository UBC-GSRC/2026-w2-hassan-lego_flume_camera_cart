# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:14:12 2024

@author: Katrin Tanner
"""

from Network import Axis
from Network import Controller
from BinaryCommunication import BinaryCommunication
import time

cartController = Controller('192.168.100.21')
cartAxle = Axis('192.168.100.21', 0, "cart") 
com = BinaryCommunication()

com.connect(cartController)
com.enableDrive(cartAxle)

#------------------------------------------------------------------------------------------------------#
#------------------------------------------- Example Code ---------------------------------------------#
#------------------------------------------------------------------------------------------------------#


#------------------------------------------ Move Cart Home --------------------------------------------#
com.setBit(cartAxle, 796)                                   # jog positive
Home = 0
while Home == 0:
    Home = com.requestBit(cartAxle, 4600, 3)                  # read out home position
    time.sleep(0.01)
com.setBit(cartAxle,795)                                    # stop jog

#--------------------------------------- Set position to zero -----------------------------------------#
com.setParameter(cartAxle, 12288, 0, 'long')                # current position = 0
com.setParameter(cartAxle, 12290, 0, 'long')                # actual position = 0

#------------------------------------------- Do bed scann ---------------------------------------------#
flumelen = 240
pictureDistance = 10
for i in range(0, flumelen, pictureDistance):
    com.move(cartAxle,-20)
    inMotion = 1
    flag = 1
    while inMotion == 1:                                        # wait till cart stops
        inMotion = com.requestBit(cartAxle, 4112, 5)            # read out if cart is moving position
        time.sleep(0.01)

    #Automatically trigger the camera
    com.setBit(cartAxle, 32)
    time.sleep(1)  # Allow time for the camera to be triggered
    com.clrBit(cartAxle, 32)
    print("Camera triggered automatically")

#------------------------------------------ Move Cart Home --------------------------------------------#
com.setBit(cartAxle, 796)                                   # jog positive
Home = 0
while Home == 0:
    Home = com.requestBit(cartAxle, 4600, 3)                # read out home position
    time.sleep(0.01)
com.setBit(cartAxle,795)                                    # stop jog

#------------------------------------------------------------------------------------------------------#
#------------------------------------------ Ende Example Code -----------------------------------------#
#------------------------------------------------------------------------------------------------------#

com.disableDrive(cartAxle)
com.disconnect(cartController)
    
