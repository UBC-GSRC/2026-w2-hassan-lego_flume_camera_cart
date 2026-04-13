# -*- coding: utf-8 -*-
"""
Created on 2024-11-14

@author: Devin Fennerty
"""
import time
import array
flumelen = 40
pictureDistance = 10
arr1 = array.array('i',[1,2,3])

def plusArray(set, arr1):
    arr1.append(set)


for i in range(0, flumelen, pictureDistance):
    inMotion = 1
    flag = 1
    while inMotion == 1: #checks for cart to be stopped                  
        inMotion = 0 # wait till cart stops in actual code
        time.sleep(0.01)
        
    while flag == 1:

        user_input = input("Type 'c' and hit enter to trigger the camera manually: ").strip().lower()
        if user_input == 'c':
            set = 1
            plusArray(set,arr1)
            print("Manual trigger: Camera triggered")
            time.sleep(1)  # Short delay to allow camera to capture
            set = -5
            plusArray(set,arr1)
            flag = 0
        else:
            print("Error: Wrong key entered. Please type 'c' to trigger the camera.")
            flag = 1

    
print("Done Code")
print(arr1)