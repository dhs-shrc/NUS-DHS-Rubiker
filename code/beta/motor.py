import time
    
class Motor:
    def __init__(self, yellow, blue, white, black, io):
        # colors are GPIO pin numbers
        self.yellow = yellow
        self.blue = blue
        self.white = white
        self.black = black
        self.io = io
        
        # io is the raspberry pi object from pigpio
        self.io.callback(self.yellow, 2, self.change_state)  # callback function
        self.io.callback(self.blue, 2, self.change_state)
        
        self.levels = [0 for i in range(4)]  # consecutive (chronological) states of PWM output pins (yellow and blue)
        
        # PID control variables
        self.curr_pos = 0
        self.set_pos = 0
        self.error = 0
        self.last_error = None
        self.integral = 0
        
        # Set pid  multiplier tuning for rack(r) / other motor(m)
        self.m_kp = 0.08
        self.m_ki = 0
        self.m_kd = 0.05
        
                
        
    def change_state(self, pin, level, tick):
    
        self.levels[0] = self.levels[2]  # move current state to previous slot
        self.levels[1] = self.levels[3]
        
        if pin == self.yellow: # update current state
            self.levels[2] = level
        elif pin == self.blue:
            self.levels[3] = level
        s = sum(self.levels)
        
        # determine direction of motor
        forward = False
        if s==1:
            if self.levels[0] or self.levels[3]:
                forward=True
        elif s==3:
            if self.levels[0]==0 or self.levels[3]==0:
                forward=True
        if forward:
            self.curr_pos += 1
        else:
            self.curr_pos -= 1
    
    def cut_power(self):
        self.io.set_PWM_dutycycle(self.white, 0)
        self.io.set_PWM_dutycycle(self.black, 0)
        return "stopped"
    
    #uses PID    
    def move_deg(self, deg):
        
        #set arbitrary position next
        self.set_pos+=deg*2
        
        #counter to stop if goes past a certain count
        sample_count = 0
        
        #track time taken
        t = time.time()
        while True:
            #regulate pid steps at intervals of 0.02s
            if time.time()>t+0.02:
                
                #calculate the current error
                self.error = self.set_pos - self.curr_pos
                
                if self.last_error == None:
                    self.last_error = self.error
                
                #add up accumulated error from past error
                self.integral += self.error
                
                #calculate error rate by 
                error_rate = self.error-self.last_error
                print("Error Rate",error_rate)
                
                '''Deduce the velocity setting required by PID formula'''
                #setting for claw with no cube
                v = self.error*self.m_kp + self.integral*self.m_ki+ error_rate*self.m_kd
                
                #setting for claw with cube
                #v = self.error*0.07 + self.integral*0.00005 + error_rate*0.18
                
                self.last_error = self.error
                v_mag = min(abs(v), 5)
                #print(v_mag)
                
                if v>=0:
                    self.io.set_PWM_dutycycle(self.white, 0)
                    self.io.set_PWM_dutycycle(self.black, v_mag*45)
                else:
                    self.io.set_PWM_dutycycle(self.white, v_mag*45)
                    self.io.set_PWM_dutycycle(self.black, 0)
                t += 0.02
                print("Current pos",self.curr_pos,"Set position",self.set_pos)
                print("sample_count",sample_count)
                #sample_count+=1
                #time.sleep(1)
                
                if self.set_pos-4 <= self.curr_pos <= self.set_pos+4:
                    sample_count+=1
                    
                else:
                    sample_count=0
                
                
            if sample_count>=10:
                print("done")
                self.io.set_PWM_dutycycle(self.white, 0)
                self.io.set_PWM_dutycycle(self.black, 0)
                self.curr_pos = 0
                self.set_pos = 0
                self.error = 0
                self.last_error = None
                self.integral = 0
                sample_count = 0
                break
                
    def release(self):
        self.io.set_PWM_dutycycle(self.white, 0)
        self.io.set_PWM_dutycycle(self.black, 0)
        
            
class RackMotor(Motor):
    #need not require yellow and blue
    def __init__(self, yellow, blue, white, black, io):
        super().__init__(yellow, blue, white, black, io)
        self.m_error = 0.05
        self.m_integral = 0.3
        self.m_error_rate = 0.2    
    
    def move_set_power(self,power):
        start = time.time()
        
        current = time.time() - start
        while True:
            if power > 0:
                self.io.set_PWM_dutycycle(self.white, abs(power))
                self.io.set_PWM_dutycycle(self.black, 0)
                print("going in forward")
            elif power < 0:
                self.io.set_PWM_dutycycle(self.white, 0)
                self.io.set_PWM_dutycycle(self.black, abs(power))
                print("going in reverse")
            else:
                self.io.set_PWM_dutycycle(self.white, 0)
                self.io.set_PWM_dutycycle(self.black,0)
        
            current = time.time() - start
            print(current)
            if current >= 0.4:
                self.io.set_PWM_dutycycle(self.white, 0)
                self.io.set_PWM_dutycycle(self.black,0)
                break
                
            
        
        
    def reset_turning(self,yellow,blue,white,black,io):
        #used to reset after a certain direction
        
        self.io.callback(self.yellow, 2, self.change_state)  # callback function
        self.io.callback(self.blue, 2, self.change_state)
        
        self.levels = [0 for i in range(4)]  # consecutive (chronological) states of PWM output pins (yellow and blue)
        
        # PID control variables
        self.curr_pos = 0
        self.set_pos = 0
        self.error = 0
        self.last_error = None
        self.integral = 0
        
        self.io.set_PWM_dutycycle(self.white, 0)
        self.io.set_PWM_dutycycle(self.black, 0)
        
        


    
