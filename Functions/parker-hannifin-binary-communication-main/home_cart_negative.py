
from Network import Axis
from Network import Controller
from BinaryCommunication import BinaryCommunication
import time
import CameraCart

cart = CameraCart.CameraCart()
cart.home()
print(f"Successfully homed: {cart.get_home_successful()}")