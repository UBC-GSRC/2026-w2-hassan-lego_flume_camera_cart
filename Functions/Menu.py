# -*- coding: utf-8 -*-
"""
Created on 2024-11-15

@author: Devin Fennerty
"""

from Network import Axis
from Network import Controller
from BinaryCommunication import BinaryCommunication
import time

cartController = Controller('192.168.100.21')
cartAxle = Axis('192.168.100.21', 0, "cart") 
com = BinaryCommunication()

# Connect and enable the cart
com.connect(cartController)
com.enableDrive(cartAxle)

# Default configuration
flumelen = 13700
pictureDistance = 170
precise_start = 0 # location of increased overlap between photos for higher resolution
precise_end = 13600 # location where increase overlap ends
computer_position = -11000
axis_reverse = True
"Note distance is measured in mm entire flume is around 1500cm"

def cameraTrigger(pos=None):
    # Trigger Cameras
    time.sleep(0.1)
    com.setBit(cartAxle, 32)
    if pos == None:
        print(f"Camera triggered")
    else:7
    print(f"Camera triggered at position {pos}")
    time.sleep(0.1)
    com.clrBit(cartAxle, 32)

def moveToZero():
    com.move(cartAxle, 0, 'a')

def moveCartHome():
    """Move the cart to the home position."""
    # # assumes cart is downstream of home sensor!
    print("\n*******************************************************************************************************************\n")
    print("ERROR: Homing cannot be done from the lego flume camera cart computer. Talk to Adam to home the cart from his computer.")
    print("\n*******************************************************************************************************************")
    # com.setBit(cartAxle, 17160)
    # home = 0
    # while home == 0:
    #     home = com.requestBit(cartAxle, 4600, 3)
    #     time.sleep(0.5)

def performBedScan():
    """Perform a bed scan using the current flumelen and pictureDistance."""
    global flumelen, pictureDistance
    print(f"Starting bed scan with flumelen = {flumelen} and pictureDistance = {pictureDistance}.")
    

    for i in range(0, flumelen, pictureDistance): # ensure the final distance is included in the images
        com.move(cartAxle, -i, 'a')
        
        inMotion = 1
        while inMotion == 1:
            inMotion = com.requestBit(cartAxle, 4112, 5)  # Wait for the cart to stop
            time.sleep(0.5)

        # Trigger Cameras
        time.sleep(0.1)
        com.setBit(cartAxle, 32)
        print(f"Camera triggered at position {i}.")
        time.sleep(0.5)
        com.clrBit(cartAxle, 32)
        time.sleep(3)

    print("Bed scan completed.")
    time.sleep(3)
    image_transfer()

def smallBedScan():
    """Perform a bed scan using the""" 
    print(f"Starting bed scan with flumelen = 50 and pictureDistance = 10.")
    for i in range(0, 50, 10):
        com.move(cartAxle, -10)
        inMotion = 1
        while inMotion == 1:
            inMotion = com.requestBit(cartAxle, 4112, 5)  # Wait for the cart to stop
            time.sleep(0.5)

        # Trigger Cameras
        time.sleep(0.1)
        com.setBit(cartAxle, 32)
        time.sleep(0.1)
        print(f"Camera triggered at position {i}.")
        time.sleep(2)
        com.clrBit(cartAxle, 32)
    
    print("Bed scan completed.")

def manualMove():
    """Allow the user to manually move the cart."""
    try:

        if axis_reverse:
            distance = int(input("Enter distance to move (positive is downstream; integer only): ")) * -1
        else:
            distance = int(input("Enter distance to move (negative is downstream; integer only): "))

        com.move(cartAxle, distance)

        if axis_reverse:
            print(f"Moving cart by {distance * -1} mm.")
        else:
            print(f"Moving cart by {distance} mm.")
        inMotion = 1
        while inMotion == 1:
            inMotion = com.requestBit(cartAxle, 4112, 5)  # Wait for the cart to stop
            time.sleep(0.5)
        print("Movement complete.")
    except ValueError:
        print("Invalid input: Please enter an integer value for the distance.")
    

def manualTrigger():
    flag = 1

    while flag == 1:

        user_input = input("Type 'c' and hit enter to trigger the camera manually: ").strip().lower()
        if user_input == 'c':
            com.setBit(cartAxle, 32)
            # com.setBit2(cartAxle, 32)
            print("Manual trigger: Camera triggered")
            time.sleep(1)  # Short delay to allow camera to capture
            com.clrBit(cartAxle, 32)
            # com.clearBit(cartAxle, 32)
            flag = 0
        else:
            print("Error: Wrong key entered. Please type 'c' to trigger the camera.")
    

def updateBedScan():
    """Allow the user to update configuration settings."""
    global flumelen, pictureDistance
    try:
        flumelen = int(input(f"Enter new value for flumelen (current: {flumelen}): "))
        pictureDistance = int(input(f"Enter new value for pictureDistance (current: {pictureDistance}): "))
        print(f"Settings updated: flumelen={flumelen}, pictureDistance={pictureDistance}.")
    except ValueError:
        print("Invalid input: Please enter integer values.")

def manualBedScan():
    """Allow the user to manually trigger image capture in the bed scan."""
    global flumelen, pictureDistance, precise_start, precise_end
    choice = input("Is the cart at the home position (y/n)?").strip()
    if choice == "y":
        print(f"Starting bed scan with flumelen = {flumelen} and pictureDistance = {pictureDistance}.")
        print(f"User has 1 minute to go around the side of the flume and collect the manual trigger")
        time.sleep(45)
        for i in range(0, flumelen, pictureDistance):
            if i >= precise_start and i < precise_end: 
                com.move(cartAxle, -pictureDistance/2)
                inMotion = 1
                while inMotion == 1:
                    inMotion = com.requestBit(cartAxle, 4112, 5)  # Wait for the cart to stop
                time.sleep(0.5)

                # Allowing time for use to trigger cameras
                time.sleep(5)
                print(f"Camera triggered at {(i+(0.5*pictureDistance))} mm.")
                time.sleep(1)

                com.move(cartAxle, -pictureDistance/2)
                inMotion = 1
                while inMotion == 1:
                    inMotion = com.requestBit(cartAxle, 4112, 5)  # Wait for the cart to stop
                time.sleep(0.5)

                # Allowing time for use to trigger cameras
                time.sleep(5)
                print(f"Camera triggered at {(i+pictureDistance)} mm.")
                time.sleep(1)
            
            else:

                com.move(cartAxle, -pictureDistance)
                inMotion = 1
                while inMotion == 1:
                    inMotion = com.requestBit(cartAxle, 4112, 5)  # Wait for the cart to stop
                    time.sleep(0.5)

                # Allowing time for use to trigger cameras
                time.sleep(5)
                print(f"Camera triggered at {(i+pictureDistance)} mm.")
                time.sleep(1)
            
        print(f"Cart stopped {len(range(0, flumelen, pictureDistance))} times")
        print("Bed scan completed.")
        print("Moving back home.")
        com.move(cartAxle, flumelen)
        inMotion = 1
        while inMotion == 1:
            inMotion = com.requestBit(cartAxle, 4112, 5)  # Wait for the cart to stop
            time.sleep(0.5)
        print("Finished!")

    else: print("Move the cart to the home position using option 1")

def image_transfer():
    '''Allow the user to manually connect to the cameras for image transfer (move cart to above computer)'''
    global computer_position
    print(f"Moving cart to position above computer, {computer_position}.")
    com.move(cartAxle, computer_position, 'a')
    inMotion = 1
    while inMotion == 1:
        inMotion = com.requestBit(cartAxle, 4112, 5)  # Wait for the cart to stop
        time.sleep(0.5)

    print(f"1. Go around the flume and connect the USB extension cord and power cord to the USB camera hub.")
    print("2. Use the windows comptuer next to the camera cart computer to download the images.\n")
    choice_2 = input("Have you finished transferring the images to the computer (y/n)?")
    if choice_2 == "y":
        choice_3 = input("Have you disconnected the cable from the camera cart (y/n)?")
        if choice_3 == "y":
            print("Moving back home.")
            com.move(cartAxle, -10, 'a')
            inMotion = 1
            while inMotion == 1:
                inMotion = com.requestBit(cartAxle, 4112, 5)  # Wait for the cart to stop
                time.sleep(0.5)
            print("Finished!")

        else:
            print("Disconnect the cable from the camera cart. Use option 0 if you want to return the cart to home position.")

    else:
        print("Once finished transferring disconnect the cable and move the cart back to the home posiiton manually using option 0")


def get_position():
    encoder_scale_factor = 0.0034 / 7.2150
    index, value = com.requestParameter(cartAxle, 6144)

    if axis_reverse:
        print(f"Current position: {round(-1 * value * encoder_scale_factor, 2)} mm (positive is downstream)")
    else:
        print(f"Current position: {round(value * encoder_scale_factor, 2)} mm (negative is downstream)")


def menu():
    """Display the main menu."""
    while True:
        print("\n--- Cart Control Interface ---")
        print("0. Move cart to feeder")
        print("1. Perform bed scan")
        print("2. Manual move (relative)")
        print("3. Manual Capture")
        print("4. Update BedScan")
        print("5. Small Bed Scan")
        print("6. Manual Bed Scan")
        print("7. Image Transfer")
        print("8. Homing procedure (only when the cart has lost its true position)")
        print("9. Exit")
        get_position()
        choice = input("Select an option (1-9): ").strip()

        if choice == '0':
            moveToZero()
        elif choice == '1':
            performBedScan()
        elif choice == '2':
            manualMove()
        elif choice == '3':
            manualTrigger()
        elif choice == '4':
            updateBedScan()
        elif choice == '5':
            smallBedScan()
        elif choice == '6':
            manualBedScan()
        elif choice == '7':
            image_transfer()
        elif choice == '8':
            moveCartHome()
        elif choice == '9':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

# Run the interface
try:
    menu()
finally:
    com.disableDrive(cartAxle)
    com.disconnect(cartController)
    print("Cart drive disabled and controller disconnected.")
