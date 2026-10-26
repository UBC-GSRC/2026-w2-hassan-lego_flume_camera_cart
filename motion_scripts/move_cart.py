
from parker_hannifin_binary_communication.BinaryCommunication import BinaryCommunication
from parker_hannifin_binary_communication.Network import Controller
from parker_hannifin_binary_communication.Network import Axis
import time


def main():

    cartController = Controller('192.168.100.21')
    cartAxle = Axis('192.168.100.21', 0, "cart") 
    com = BinaryCommunication()

    com.connect(cartController)
    com.enableDrive(cartAxle)

    # NOTE: A negative relative movement moves the Lego flume cart towards the outlet. 

    # -13600 is the downstream boundary
    # -11000 for transferring images off of the cameras
    # 0 is the feeder boundary

    distance_mm = 0
    try:
        com.move(cartAxle,distance_mm, Movement='a') # change movement to 'r' to be relative jogs. 'a' is absolute movement and only should be used after homing
    except KeyboardInterrupt:
        com.setBit(cartAxle, 522)

    inMotion = 1
    while inMotion:
        inMotion = com.requestBit(cartAxle, 4112, 5)
        print("Moving")
        time.sleep(2)

    print("Complete")
if __name__ == "__main__":    
    main()