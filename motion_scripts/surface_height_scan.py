"""
Author: Adam Fong
Date: 2026-04-14
Description: This script is meant to provide a safe way to perform a surface height scan with the camera cart.
"""

import CameraCart
import URM14
import time     
from pathlib import Path
import sys
import csv
import matplotlib.pyplot as plt
import threading
import pandas as pd
from URM14 import URM14

DIRECTION_MODIFIER = -1 # Downstream is a negative value, this variable is for clarity

# Option 1: Recording distance while moving. 
BEDSCAN_DISTANCE_MM = 13500 # Scanning range from the current location, going downstream

# Option 2: Discrete steps, slower but goes to exact locations
BEDSCAN_STEP_SIZE_MM = 150

FLUME_LEN = 15290 # Length of the measuring tape adhered to the flume walls 

def time_elapsed(func):
    """
    Decorator to time the execution of a function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        return result
    return wrapper

class SurfaceHeightScanner:
    def __init__ (self, cart_ip='192.168.100.21', esp32_port = "COM7", flume_length = FLUME_LEN):
        self.bedscan_distance = BEDSCAN_DISTANCE_MM * DIRECTION_MODIFIER
        self.bedscan_step_size = BEDSCAN_STEP_SIZE_MM
        self.cart = CameraCart.CameraCartLego(cart_ip, esp32_port)
        self.heights = []
        self.sensor_ids = []
        self.upstream_positions = []
        self.cross_stream_positions = []
        self.error_counter = 0
        self.stop_thread = threading.Event()
        self.error_distance = threading.Event()
        self.error_timeout = threading.Event()
        self.flume_length = flume_length
        self.counter = 0

    def surface_height_procedure_steps(self):
        """
        Perform a surface height scan by moving the cart and measuring surface height at each step.
        """
        if self.cart.get_home_status() == False:
            raise Exception("Camera cart has not been homed. Please home the cart before starting the surface height scan.")
        
        locations = list(range(0, self.bedscan_distance, self.bedscan_step_size))
        locations.append(self.bedscan_distance) # Ensure the final position is included
        heights = []
        positions = []
        for location in locations:
            print(f"Moving to {location} mm\n")
            self.cart.jog_absolute(location, blocking=True)
            print(f"Measuring surface height at {location} mm\n")
            surface_height = self.cart.get_water_level()
            print(f"Surface height at {location} mm: {surface_height} mm\n")
            self.heights.append(surface_height)
            self.upstream_positions.append(self.cart.get_position()[1])

        print("Surface height scan complete. Returning to home position.")
        self.cart.jog_absolute(0, blocking=False) # return near home

        return self.heights, self.upstream_positions

    def surface_height_procedure_rapid(self):
        # Start a thread to record the distance and height data 
        record_thread = threading.Thread(target=self.record_data_constant, args=(self.stop_thread,self.error_distance, self.error_timeout))
        record_thread.start()
        self.cart.jog_absolute(self.bedscan_distance, blocking=True)
        self.stop_thread.set() # signal the recording thread to stop after movement is complete
        record_thread.join()

        # Go back home after scan

        if self.error_distance.is_set() == False and self.error_timeout.is_set() == False:
            print("Surface height scan complete.")
            time.sleep(1)
            print("Returning to home position.")
            self.cart.jog_absolute(0, blocking=False)
        else:
            print("Error! Read the terminal to see how to respond. Rerun the script. If the next scan is successful, combine the two files together to get a complete scan.")

    def record_data_constant(self, stop_event, error_distance, error_timeout):
        false_position_count = 0
        false_position = False
        start_pos = self.cart.get_position()[1]
        while stop_event.is_set() == False:

            # Check if it's taking forever to get the distance reading
            for urm14 in self.cart.distance_sensors:
                pos = self.cart.get_position()[1]

                print("Get surface height")
                height = self.cart.get_water_level(urm14.sensor_id, urm14.offset_z_mm)
                print("Surface height received ")
                if height == -1:
                    print("ESP32 Timeout Error: Stopping cart. Restart the distance sensor power switch and rerun.")
                    self.error_counter += 1

                    if self.error_counter > 10:
                        print("Too many erroneous distance measurements. Restart the power bar for the distance sensor.")
                        self.cart.kill_all_motions()
                        stop_event.set()
                        error_timeout.set()

                if abs(pos) > abs(start_pos + self.bedscan_distance - 500): # The wrong encoder position can sometimes be read which causes poor data. Skip these.
                    false_position_count += 1
                    false_position = True
                    if false_position_count >= 10:
                        print("Too many false positions detected. Exiting. Please try again.")
                        self.cart.kill_all_motions()
                        stop_event.set()
                        error_distance.set()
                    print("\nCart has seen an error which says it's past the maximum distance limit. Skipping reading.")
                    print("False Position: {:.2f} mm\n".format(pos))

                    if len(self.cart.distance_sensors) > 1:
                        continue
                
                if not false_position:
                    print("Position: {:.2f} mm, Surface Height: {:.2f} mm, Sensor ID: {}".format(pos, height, urm14.sensor_id))
                    self.upstream_positions.append(pos)
                    self.heights.append(height)
                    self.sensor_ids.append(urm14.sensor_id)
                    self.cross_stream_positions.append(urm14.offset_y_mm)
                    self.counter += 1
                    print(f"Counter: {self.counter}")
                    time.sleep(0.1)

                false_position = False
                
        self.convert_x_datum_to_flume_datum()

    def convert_x_datum_to_flume_datum(self):
        """The cart's X origin is at the inlet of the flume, while the origin of the flume is at the outlet. This converts the data to the Flume's origin."""
        
        # Arbitrarily take the first x offset as they have never been installed to have unique x offsets for each sensor
        self.flume_positions = list(self.flume_length - self.cart.distance_sensors[0].offset_x_mm - abs(pd.Series(self.upstream_positions))) 
        

    def write_csv(self):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        with open('surface_height_scan_' + timestamp + '.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['sensor_id', 'upstream_x_mm', 'y_mm', 'surface_height_mm'])
            for height, pos, sensor_id, cross_stream_pos in zip(self.heights, self.flume_positions, self.sensor_ids, self.cross_stream_positions):
                writer.writerow([sensor_id, pos, cross_stream_pos, height])

        print("Wrote data to surface_height_scan_" + timestamp + ".csv")

    def graph_heights(self):
        df = pd.DataFrame({"sensor_id": self.sensor_ids, "position_mm": self.flume_positions, "surface_height_mm": self.heights, "cross_stream_position_mm": self.cross_stream_positions})
        plt.figure(figsize=(10, 5))
        plt.ylim((-10, max((max(self.heights) + 10, 500))))
        for cross_stream_position, group in df.groupby("cross_stream_position_mm"):
            plt.plot(group["position_mm"], group["surface_height_mm"], marker='o', label = cross_stream_position)
        plt.title('Surface Height Scan')
        plt.xlabel('Upstream Cart Position (mm)')
        plt.ylabel('Surface Height (mm)')
        plt.legend(title="Cross Stream Position (mm)")
        plt.grid()
        plt.show()

@time_elapsed
def main():
    # X = Upstream distance
    # Y = Crossstream distance
    # Z = Vertical distance from flume bed
    urm14_1 = URM14(offset_x_mm = 250.0, offset_y_mm = 300, offset_z_mm = 962, sensor_id = 1)
    
    surface_scanner = SurfaceHeightScanner(cart_ip='192.168.100.21',esp32_port="/dev/ttyACM0", flume_length=FLUME_LEN)

    surface_scanner.cart.add_urm14(urm14_1)

    # Option 1: Scanning without stopping 
    # Ensure starting at home position
    surface_scanner.cart.jog_absolute(0)
    surface_scanner.surface_height_procedure_rapid()

    # Option 2: Scanning with stopping at each step defined in the top of the file
    # heights, positions = water_scanner.surface_height_procedure_steps()

    surface_scanner.write_csv()
    surface_scanner.graph_heights()

if __name__ == "__main__":
    main()
