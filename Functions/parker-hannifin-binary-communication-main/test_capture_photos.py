from cart_control import Cart #imports Cart object from the "cart_control.py" file
from BinaryCommunication import Axis
import time                   #import time module to allow pauses between steps in for loop
import wmi                    # type: ignore #checks to see if the cameras are connected to the computer or not, can be commented out if needed

pictures_path = r"E:\\Erin F\\BedScans\\bedscantest" #path to the folder where images should be saved

#TODO make sure the code can still connect to the cart in this way

cart = Cart('192.168.100.94', 5006) #sets the IP andy port needed to connect to the cart
cart.connect()                      #Connects to the cart allow commans to be sent through TCP server
axis = Axis('192.168.100.11', 0, "cart") 
time.sleep(3)

comp = wmi.WMI() #establishes connection with "Windows Management Instrumentation" 
wql = "Select * From Win32_USBControllerDevice" #query to search for anything that is a USB device

camera_count = 0 
for item in comp.query(wql):
    if item.Dependent.Name == 'Canon EOS Rebel T6': #if device with correct camera name exists it updates the counter
        camera_count += 1

print("{} Cameras Found".format(camera_count))

cart.take_digicam_photo(pictures_path) #takes image using digicam command and saves them to designated folder
