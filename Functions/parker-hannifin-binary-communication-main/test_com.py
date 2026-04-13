# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:14:12 2024

@author: Katrin Tanner
"""

from Network import Axis
from Network import Controller
from BinaryCommunication import BinaryCommunication
import time

cartController = Controller('192.168.100.11')
cartAxle = Axis('192.168.100.11', 0, "cart") 
com = BinaryCommunication()

com.connect(cartController)
com.enableDrive(cartAxle)

#------------------------------------------------------------------------------------------------------#
#------------------------------------------- Example Code ---------------------------------------------#
#------------------------------------------------------------------------------------------------------#


#------------------------------------------ Move Cart Home --------------------------------------------#
com.setBit(cartAxle, 17160)                                   # jog home
Home = 0
while Home == 0:                                              # wait till card is in home position
    Home = com.requestBit(cartAxle, 4600, 3)                  # read out home position 
    time.sleep(1)

#------------------------------------------- Do bed scann ---------------------------------------------#
flumelen = 240
pictureDistance = 10
for i in range(0, flumelen, pictureDistance):
    com.move(cartAxle,-20)
    inMotion = 1
    while inMotion == 1:                                        # wait till cart stops
        inMotion = com.requestBit(cartAxle, 4112, 5)            # read out if cart is moving position
        time.sleep(0.01)

    #trigger Cameras
    com.setBit(cartAxle, 32)
    time.sleep(1)                                               # wait two second so cameras can be triggered           
    com.clrBit(cartAxle, 32)

#------------------------------------------ Move Cart Home --------------------------------------------#
com.setBit(cartAxle, 17160)                                   # jog home
Home = 0
while Home == 0:                                              # wait till card is in home position
    Home = com.requestBit(cartAxle, 4600, 3)                  # read out home position 
    time.sleep(1)

#------------------------------------------------------------------------------------------------------#
#------------------------------------------ Ende Example Code -----------------------------------------#
#------------------------------------------------------------------------------------------------------#

com.disableDrive(cartAxle)
com.disconnect(cartController)
    
