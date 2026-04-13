Summary of included files:
    There are two files you need to include in your code for it to work. Download these files and copy them to the same folder you have your own code
    safed to.: 
        BinaryCommunication.py -> This file includes the commands you need for the communication. 
        Network.py -> This file contains the structure of your network. Parker controllers are built to establish a large network with multiple controllers
        and axles. So far the code is only written for one actuator but it gives you the possibility for extension. 
    If you are just getting started with working with the binary host interface there are some files that might help you to understand how this works:
        Explanation for Users.txt -> Here you find some explanation if you just want to use the code and don't have in depth knolage about programming.
        It explains how you can stack the functions together and what parameters to hand them for the code to work.
        test_com.py -> You can download this code and start working with it. It has all the setup functions included and a small example to see if
        everything works as it should. You can replace the example functions later with your own code.

The communication uses the binary host interface. 
Port 5006.

Explanation to positions:
    There are several different positions, that seem the same at first glance but are not. The Actual Position (P12295 for Axis0) is the position of 
    the encoder. It changes every time the motor moves no matter how it is moved (jog, Mov, etc.). The current position (P12288 for Axis0) 
    is only influenced when using the MOV command in ACR view or when using the equivalent via the binary communication interface. when
    using the jog command it will stay the same and the controller will assign the "new" position the value of the "old" current position. 
    In consequence when using the mov command afterwards. Position 0 will have the offset that was created by the jog movement. 
    The target position (P12289 for Axis0) is in relation to the 0 position of the current position. It indicates the position you send the cart to via the mov command.
    The equivalent to the target position for the actual position is called commanded position (P12295 for Axis0). It is the same than the secondary setpoint. 

    You should be fine and not run into trouble if you stick to the following procedure:
    1. Start your program with setting the "jog home" bit. This will move the cart to its home position and set all relevant position parameters
       to zero. 
    4. don't use the jog command during your bedscann. If you have to you can just start with step 1 again. 

    For the feeder all of this isn't relevant

Comment about outputs:
    On this controller the output works like a switch controlled by the controller. To create a signal you have to add an external power supply or use the 5V
    of the controller. 

most important Parameters and Bits summary:

Current position Axis0				->	P12288          
Target position Axis0				->	P12289          
Actual position Axis0				->	P12290
Secondary Setpoint Axis0            ->  P12295          
Primary Setpoint Axis0              ->  P12294
Position Encoder0                   ->  P6144    
Jog offset                          ->  P11297       

Axis0 I/Os:
Analog Input 0					    ->	P35332
Analog Input 1					    ->	P35340
Input 0                             ->  Bit0        ||  P4096, Bit1
Input 1                             ->  Bit1        ||  P4096, Bit2
Input 2                             ->  Bit2        ||  P4096, Bit3
Input 3                             ->  Bit3        ||  P4096, Bit4
Input 4                             ->  Bit4        ||  P4096, Bit5
Input 5                             ->  Bit5        ||  P4096, Bit6
Input 6                             ->  Bit6        ||  P4096, Bit7
Output 32                           ->  Bit32       ||  P4097, Bit1
Output 33                           ->  Bit33       ||  P4097, Bit2
Output 34                           ->  Bit34       ||  P4097, Bit3
Output 35                           ->  Bit35       ||  P4097, Bit4

Jog parameter Axis0:
Jog forward                         ->  Bit796
Jog stopping                        ->  Bit795
Jog reverse                         ->  Bit797
Jog home                            ->  Bit17160

Actual Torque Axis0				    ->	P28740
Actual Velocity Axis0				->	P28741
User unit					        ->	P12375
Jog Acceleration Axis0				->	P12349
Jog Velocity Axis0				    ->	P12348
Jog Deceleration Axis0				->	P12350
Velocity Axis0					    ->	P12315
Acceleration Axis0				    ->	P12316
PPU						            ->	P12375

Enable Drive Axis0				    ->	Bit8465
Home Input Current state            ->  Bit16130    ||  P4600, Bit3
Homing Axis0 successful				->	Bit16134
Homing Axis0 unsuccessful			->	Bit16135
In motion                           ->  Bit516      ||  P4112, Bit5

For other Parameter and Bit settings reference the ACR Programmer's Guide and the ACR-View Software.
In the Bit Statos of the Status Panel in the ACR-Software you can also find which Parameter a Bit belongs to. (Top right corner.)