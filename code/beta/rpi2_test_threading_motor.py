#rpi 2 slave
import pigpio
from motor import Motor
from motor import RackMotor
import random
import threading
import time
from serial_comm import serial_comm
#from cube_display import *

SRL_R_RACK_OUT = R2_OUT = 'a'
SRL_R_RACK_IN = R2_IN = 'b'
SRL_F_RACK_OUT = R1_OUT = 'c'
SRL_F_RACK_IN = R1_IN = 'd'
SRL_F_FWD = M1_FWD = 'e'
SRL_F_REV = M1_REV = 'f'
SRL_R_FWD = M2_FWD = 'g'
SRL_R_REV = M2_REV = 'h'
SRL_ACK = 'z'
SRL_STOP = 'y'
B_FWD = -90
B_REV = 90
B_RACK_IN = -255
B_RACK_OUT = 255
L_FWD = -90
L_REV = 90
L_RACK_IN = -255
L_RACK_OUT = 255


P1_TOP = 'i'
P1_MID = 'j'
P1_BOT = 'k'

is_f_upright = True
is_b_upright = True
is_l_upright = True
is_r_upright = True
is_f_rack_in = True
is_b_rack_in = True
is_l_rack_in = True
is_r_rack_in = True

#def main(config, io):
def main(io):
    #GPIO 14,15,18,23; PIN  8,10,12,16
    #GPIO 24,25, 8, 7; PIN 18,22,24,26
    #GPIO 1 ,12,16,20; PIN 28,32,26,38
    #GPIO 6 ,13,19,26; PIN 31,33,35,37 (Left turn)
    #GPIO 10, 9,11, 5; PIN 19,21,23,29 (
    #GPIO 17,27, 3, 4; PIN 11,13,5 ,7
    #22 doesn't work
    
    #rpi2
    
    global rack_l,motor_l,rack_b,motor_b
    global is_f_upright, is_b_upright, is_l_upright, is_r_upright
    rack_l = RackMotor("rl", 6,13,19, 26,io)
    motor_l = Motor("ml", 1 ,21,16,20,io)
    rack_b = RackMotor("rb", 10, 9,11, 5,io)
    motor_b = Motor("mb", 24,25, 8, 7,io)
    comms = serial_comm()
    
    '''
    rack_l.move_deg(L_RACK_OUT)
    motor_l.move_deg(L_FWD)
    motor_l.move_deg(L_FWD)
    motor_l.move_deg(L_REV)
    motor_l.move_deg(L_FWD)
    motor_l.move_deg(L_REV)
    motor_l.move_deg(L_REV)
    rack_l.move_deg(L_RACK_IN)
    
    return
    '''
    
    #solution = "L' F R F' B' F B".split(" ")
    #solution = "B R' R L B' F B".split(" ")
    #solution = "R' F' B R U' F' U' U' B' B' L D F U' U' F' F' D' D' F' L' L' F' F' B R' R' F".split()
    solution = "F' F' B U' F' L' D F' B B L B B D F F U' D D R R U U R R F F U' R R B'".split()
    solution = "F L B B L U B' D' L' B U' F F B B D R R D B B U' D D B B".split()
    #solution = "U U' D D' L L' R R' B B' F F'".split()
    for step in solution:
        print(step)
        if step == "L":
            if not is_f_upright:
                comms.write_serial(SRL_F_RACK_OUT)
                comms.read_serial()
                comms.write_serial(SRL_F_FWD)
                comms.read_serial()
                comms.write_serial(SRL_F_RACK_IN)
                comms.read_serial()
                is_f_upright = True
            if not is_b_upright:
                rack_b.move_set_power(B_RACK_OUT)
                motor_b.move_deg(B_FWD)
                rack_b.move_set_power(B_RACK_IN)
                is_b_upright = True
            motor_l.move_deg(L_FWD)
            is_l_upright = not is_l_upright
        elif step == "L'":
            if not is_f_upright:
                comms.write_serial(SRL_F_RACK_OUT)
                comms.read_serial()
                comms.write_serial(SRL_F_FWD)
                comms.read_serial()
                comms.write_serial(SRL_F_RACK_IN)
                comms.read_serial()
                is_f_upright = True
            if not is_b_upright:
                rack_b.move_set_power(B_RACK_OUT)
                motor_b.move_deg(B_FWD)
                rack_b.move_set_power(B_RACK_IN)
                is_b_upright = True
            motor_l.move_deg(L_REV)
            is_l_upright = not is_l_upright
        elif step == "R":
            if not is_f_upright:
                comms.write_serial(SRL_F_RACK_OUT)
                comms.read_serial()
                comms.write_serial(SRL_F_FWD)
                comms.read_serial()
                comms.write_serial(SRL_F_RACK_IN)
                comms.read_serial()
                is_f_upright = True
            if not is_b_upright:
                rack_b.move_set_power(B_RACK_OUT)
                motor_b.move_deg(B_FWD)
                rack_b.move_set_power(B_RACK_IN)
                is_b_upright = True
            comms.write_serial(SRL_R_FWD)
            comms.read_serial()
            is_r_upright = not is_r_upright
        elif step == "R'":
            if not is_f_upright:
                comms.write_serial(SRL_F_RACK_OUT)
                comms.read_serial()
                comms.write_serial(SRL_F_FWD)
                comms.read_serial()
                comms.write_serial(SRL_F_RACK_IN)
                comms.read_serial()
                is_f_upright = True
            if not is_b_upright:
                rack_b.move_set_power(B_RACK_OUT)
                motor_b.move_deg(B_FWD)
                rack_b.move_set_power(B_RACK_IN)
                is_b_upright = True
            comms.write_serial(SRL_R_REV)
            comms.read_serial()
            is_r_upright = not is_r_upright
        elif step == "F":
            if not is_l_upright:
                rack_l.move_set_power(L_RACK_OUT)
                motor_l.move_deg(L_FWD)
                rack_l.move_set_power(L_RACK_IN)
                is_l_upright = True
            if not is_r_upright:
                comms.write_serial(SRL_R_RACK_OUT)
                comms.read_serial()
                comms.write_serial(SRL_R_FWD)
                comms.read_serial()
                comms.write_serial(SRL_R_RACK_IN)
                comms.read_serial()
                is_r_upright = True
            comms.write_serial(SRL_F_FWD)
            comms.read_serial()
            is_f_upright = not is_f_upright
        elif step == "F'":
            if not is_l_upright:
                rack_l.move_set_power(L_RACK_OUT)
                motor_l.move_deg(L_FWD)
                rack_l.move_set_power(L_RACK_IN)
                is_l_upright = True
            if not is_r_upright:
                comms.write_serial(SRL_R_RACK_OUT)
                comms.read_serial()
                comms.write_serial(SRL_R_FWD)
                comms.read_serial()
                comms.write_serial(SRL_R_RACK_IN)
                comms.read_serial()
                is_r_upright = True
            comms.write_serial(SRL_F_REV)
            comms.read_serial()
            is_f_upright = not is_f_upright
        elif step == "B":
            if not is_l_upright:
                rack_l.move_set_power(L_RACK_OUT)
                motor_l.move_deg(L_FWD)
                rack_l.move_set_power(L_RACK_IN)
                is_l_upright = True
            if not is_r_upright:
                comms.write_serial(SRL_R_RACK_OUT)
                comms.read_serial()
                comms.write_serial(SRL_R_FWD)
                comms.read_serial()
                comms.write_serial(SRL_R_RACK_IN)
                comms.read_serial()
                is_r_upright = True
            motor_b.move_deg(B_FWD)
            is_b_upright = not is_b_upright
        elif step == "B'":
            if not is_l_upright:
                rack_l.move_set_power(L_RACK_OUT)
                motor_l.move_deg(L_FWD)
                rack_l.move_set_power(L_RACK_IN)
                is_l_upright = True
            if not is_r_upright:
                comms.write_serial(SRL_R_RACK_OUT)
                comms.read_serial()
                comms.write_serial(SRL_R_FWD)
                comms.read_serial()
                comms.write_serial(SRL_R_RACK_IN)
                comms.read_serial()
                is_r_upright = True
            motor_b.move_deg(B_REV)
            is_b_upright = not is_b_upright
        else: #U, U', D, D'
            if (step == 'U' or step == "U'"):
                is_up = True
            elif (step == 'D' or step == "D'"):
                is_up = False
            else:
                print('Flying kite')
                raise Exception('flying kite')
            
                
            if is_l_upright:
                if not is_f_upright:
                    comms.write_serial(SRL_F_RACK_OUT)
                    comms.read_serial()
                    comms.write_serial(SRL_F_FWD)
                    comms.read_serial()
                    comms.write_serial(SRL_F_RACK_IN)
                    comms.read_serial()
                    is_f_upright = True
                if not is_b_upright:
                    rack_b.move_set_power(B_RACK_OUT)
                    motor_b.move_deg(B_FWD)
                    rack_b.move_set_power(B_RACK_IN)
                    is_b_upright = True
                rack_l.move_set_power(L_RACK_OUT)
                motor_l.move_deg(L_FWD)
                is_l_upright = False
                rack_l.move_set_power(L_RACK_IN)
            if is_r_upright:
                if not is_f_upright:
                    comms.write_serial(SRL_F_RACK_OUT)
                    comms.read_serial()
                    comms.write_serial(SRL_F_FWD)
                    comms.read_serial()
                    comms.write_serial(SRL_F_RACK_IN)
                    comms.read_serial()
                    is_f_upright = True
                if not is_b_upright:
                    rack_b.move_set_power(B_RACK_OUT)
                    motor_b.move_deg(B_FWD)
                    rack_b.move_set_power(B_RACK_IN)
                    is_b_upright = True
                comms.write_serial(SRL_R_RACK_OUT)
                comms.read_serial()
                comms.write_serial(SRL_R_FWD)
                comms.read_serial()
                is_r_upright = False
                comms.write_serial(SRL_R_RACK_IN)
                comms.read_serial()
             
            # retract front and back
            comms.write_serial(SRL_F_RACK_OUT)
            rack_b.move_set_power(B_RACK_OUT)
            comms.read_serial()
            
            # rotate cube's U to F claw
            if is_up:
                comms.write_serial(SRL_R_REV)
                motor_l.move_deg(L_FWD)
                comms.read_serial()
            else:
                comms.write_serial(SRL_R_FWD)
                motor_l.move_deg(L_REV)
                comms.read_serial()
                
            
            # rotate using F claw
            comms.write_serial(SRL_F_RACK_IN)
            rack_b.move_set_power(B_RACK_IN)
            comms.read_serial()
            if step == "U" or step == "D":
                comms.write_serial(SRL_F_FWD)
                comms.read_serial()
            elif step == "U'" or step == "D'":
                comms.write_serial(SRL_F_REV)
                comms.read_serial()
            is_f_upright = not is_f_upright
                
            comms.write_serial(SRL_F_RACK_OUT)
            rack_b.move_set_power(B_RACK_OUT)
            comms.read_serial()
            if not is_f_upright: # make it upright to prevent collision when rotating back
                comms.write_serial(SRL_F_FWD)
                comms.read_serial()
                is_f_upright = True
                
            if not is_b_upright: # make it upright to prevent collision when rotating back
                motor_b.move_deg(B_FWD)
                is_b_upright = True
            
            # rotate back
            if is_up:
                comms.write_serial(SRL_R_FWD)
                motor_l.move_deg(L_REV)
                comms.read_serial()
            else:
                comms.write_serial(SRL_R_REV)
                motor_l.move_deg(L_FWD)
                comms.read_serial()
            
            # reengage motors
            comms.write_serial(SRL_F_RACK_IN)
            rack_b.move_set_power(B_RACK_IN)
            comms.read_serial()
            
            is_l_upright = False
            is_r_upright = False
    comms.write_serial(SRL_STOP)
    return 
    
    
    '''
    if result != "":
        to_send = f"messaged about {result} received"
        comms.write_serial(to_send)
        print("sending confirmation")
    '''
        
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
        print("Program interrupted")
        rack_l.cut_power()
        motor_l.cut_power()
        rack_b.cut_power()
        motor_b.cut_power()
        
        
