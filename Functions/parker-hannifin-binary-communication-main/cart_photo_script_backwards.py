from cart_control import Cart #imports Cart object from the "cart_control.py" file
from BinaryCommunication import Axis
import time                   #import time module to allow pauses between steps in for loop
import os
import wmi                    #checks to see if the cameras are connected to the computer or not, can be commented out if needed


pictures_path = r"E:\Hongsheng\65L\7.5-12h" #path to the folder where images should be saved

#TODO make sure the code can still connect to the cart in this way

cart = Cart('192.168.100.94', 5006) #sets the IP andy port needed to connect to the cart
cart.connect()                      #Connects to the cart allow commans to be sent through TCP server
axis = Axis(0)
cart.send_command(axis.enableDrive())
time.sleep(3)

distance_per_move = 125                              #distance to move between images in mm

number_of_moves = 37                               #number of moves needed throughout the experiment
total_distance = distance_per_move * number_of_moves  #125mm * 37 = 4600mm = 4.6 meteres moved
current_position = total_distance

count_down = number_of_moves-1  #creates the count variable
count_up = 1

correct_path = input("Did you update the path? (y/n)")

if correct_path == 'y':
    
    
    comp = wmi.WMI() #establishes connection with "Windows Management Instrumentation" 
    wql = "Select * From Win32_USBControllerDevice" #query to search for anything that is a USB device

    camera_count = 0 
    for item in comp.query(wql):
        if item.Dependent.Name == 'Canon EOS Rebel T6': #if device with correct camera name exists it updates the counter
            camera_count += 1

    if camera_count == 3: #checking that all 3 cameras are connected

        cart.send_command(axis.move(total_distance, 'a', 'IEEE32'))
        time.sleep(30)

        print("cameras are connected, now beginning photo sequence")
        #cart.send_command(f'X/{distance_per_move*number_of_moves}')
        #time.sleep(60)
    
        while current_position > 0:                        #builds while loop
            cart.take_digicam_photo(pictures_path) #takes image using digicam command and saves them to designated folder
            #time.sleep(1)                          #time waited after picture command is called to ensure the picture is taken and is not blurry
            print(f"{count_up} photo(s) taken, {count_down} left to take")  #informs user about progress
            count_up = count_up + 1                                         #updates the count variable. Could be done much better but is functional
            count_down = count_down -1
            cart.send_command(axis.move(current_position - distance_per_move, 'a', 'IEEE32'))
            #time.sleep(1.2)                          #time waited after sending move command, gives time for cart to move before images are taken
            
            current_position -= distance_per_move

        cart.take_digicam_photo(pictures_path) #takes image using digicam command and saves them to designated folder
        #time.sleep(1)                          #time waited after picture command is called to ensure the picture is taken and is not blurry

        cart.send_command(axis.move(2000, 'a', 'IEEE32'))  #sending cart 2m away from home so there is space to deal with lighttable
        time.sleep(10)

    else:
        print("Please reconnect the cameras")

else:
    print("Please update the path to save the pictures in the correct location")

cart.send_command(axis.disableDrive())
cart.disconnect()  #disconnects from the cart at the end

print("Complete!")  #Message prints to the terminal to inform user the process is complete
