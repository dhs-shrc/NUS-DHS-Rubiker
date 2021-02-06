
import pigpio
from motor import Motor
from motor import RackMotor
io = pigpio.pi()
r4 = Motor("r4", 6,13,19, 26,io)
m4 = Motor("m4", 1 ,21,16,20,io)
r3 = Motor("r3", 10, 9,11, 5,io)
m3 = Motor("m3", 24,25, 8, 7,io)
    
r4.cut_power()
m4.cut_power()
r3.cut_power()
m3.cut_power()
