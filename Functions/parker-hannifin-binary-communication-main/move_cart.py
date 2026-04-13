
from Network import Axis
from Network import Controller
from BinaryCommunication import BinaryCommunication
import time

cartController = Controller('192.168.100.21')
cartAxle = Axis('192.168.100.21', 0, "cart") 
com = BinaryCommunication()

com.connect(cartController)
com.enableDrive(cartAxle)

distance_mm = -10

com.move(cartAxle,distance_mm, Movement='r') # change movement to 'r' to be relative jogs. 'a' is absolute movement and only should be used after homing