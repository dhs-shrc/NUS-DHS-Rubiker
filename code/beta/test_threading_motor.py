#rpi 1 master
import pigpio
from motor import Motor
from motor import RackMotor
import random
import threading
import time
#from cube_display import *

#def main(config, io):
def main(io):
    #GPIO 14,15,18,23; PIN  8,10,12,16
    #GPIO 24,25, 8, 7; PIN 18,22,24,26
    #GPIO 1 ,12,16,20; PIN 28,32,26,38
    #GPIO 6 ,13,19,26; PIN 31,33,35,37 (Left turn)
    #GPIO 10, 9,11, 5; PIN 19,21,23,29 (
    #GPIO 17,27, 3, 4; PIN 11,13,5 ,7
    #22 doesn't work
    # ani_main()
    
    #rpi 1
    p1 = RackMotor(17,27, 3, 4,io)
    m1 = Motor(24,21, 8,7,io)
    r1 = RackMotor(10, 9,11, 5,io)
    r2 = RackMotor(1 ,12,16,20,io)
    m2 = Motor(6 ,13,19,26,io)
    #m1.move_deg(0)
    #m2.move_deg(90)
    #r2.move_set_power(255)
    p1.move_set_power(255)

    """
    for i in range(len(config)):
        if config[i] == "L":
            move_motor(17,27,3,4,90,io)    
        #if config[i] == "R":
        elif config[i] == "F":
            move_motor(14,15,18,23,90,io)
    
    for i in range(len(config)):
        if config[i] == "L":
            move_motor(17,27,3,4,90,io)    
        #if config[i] == "R":
        if config[i] == "F":
            move_motor(14,15,18,23,90,io)
            
    
        if config[i] == "U":
        if config[i] == "B":
        if config[i] == "D":
        if config[i] == "L'":
        if config[i] == "R'":
        if config[i] == "F'":
        if config[i] == "U'":
        if config[i] == "B'":
        if config[i] == "D'":
    
    #t2 = threading.Thread(target = move_motor, args = ("Rack",14,15,18,23,io))
    #t1 = threading.Thread(target = move_motor, args = ("m2",17,27,3,4,io))
    """
    
def move_motor(y,b,w,bl,degree,io):
    mot = Motor(y,b,w,bl,io)
    #moves = [random.randint(-180, 180) for i in range(10)]
    moves = [degree]
    for move in moves:
            mot.move_deg(move)
            print(moves)
    
def panic_button(y,b,w,bl,io):
    m1 = Motor(y,b,w,bl,io)
    moves = [0,0,0,0]
    for move in moves:
        m1.move_deg(move)
    
    

if __name__ == "__main__":
    io = pigpio.pi()
    #move_motor(17,27,3,4,0,io)
    
    try:
        #main(["L","R","L"],io)
        main(io)
    except KeyboardInterrupt:
        print("Program stopped")
        panic_button(17,27,3,4,io)
        panic_button(14,15,18,23,io)
        panic_button(6,13,19,26,io)
        panic_button(10,9,11,5,io)

