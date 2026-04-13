# -*- coding: utf-8 -*-
"""
Created on 2024-11-14

@author: Devin Fennerty
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


def manualMove():
    flag = 1
    while flag == 1:
        move_input = input("Type 'm' to move the cart manually: ").strip().lower()
        if move_input == 'm':
            try:
                distance = int(input("Enter distance to move (positive or negative integer): "))
                com.move(cartAxle, distance)
                print(f"Moving cart by {distance} units.")
                inMotion = 1
                while inMotion == 1:  # Wait until the cart stops
                    inMotion = com.requestBit(cartAxle, 4112, 5)
                    time.sleep(0.01)
                print("Movement complete.")
                flag = 0
            except ValueError:
                print("Invalid input: Please enter an integer value for the distance.")
        else:
            print("Error: Wrong key entered. Please type 'm' to move the cart.")
            flag = 1

manualMove()
"""
#------------------------------------------ Move Cart Home --------------------------------------------#
com.setBit(cartAxle, 796)                                   # jog positive
Home = 0
while Home == 0:
    Home = com.requestBit(cartAxle, 4600, 3)                # read out home position
    time.sleep(0.01)
com.setBit(cartAxle,795)                                    # stop jog

#--------------------------------------- Set position to zero -----------------------------------------#
com.setParameter(cartAxle, 12288, 0, 'long')                # current position = 0
com.setParameter(cartAxle, 12290, 0, 'long')                # actual position = 0

#------------------------------------------- Do bed scann ---------------------------------------------#

    
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
    
"""
