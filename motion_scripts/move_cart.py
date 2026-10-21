
from parker_hannifin_binary_communication.BinaryCommunication import BinaryCommunication
from parker_hannifin_binary_communication.Network import Controller
from parker_hannifin_binary_communication.Network import Axis
import time

cartController = Controller('192.168.100.21')
cartAxle = Axis('192.168.100.21', 0, "cart") 
com = BinaryCommunication()

com.connect(cartController)
com.enableDrive(cartAxle)

distance_mm = 100 # 13600 is max distance. 
com.move(cartAxle,distance_mm, Movement='a') # change movement to 'r' to be relative jogs. 'a' is absolute movement and only should be used after homing