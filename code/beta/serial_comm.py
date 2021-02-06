import time
import serial

class serial_comm:
	def __init__(self):
		self.ser = serial.Serial(
			port='/dev/ttyS0',
			baudrate=9600, 
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=0.02
		)
	
	def wait_confirmation(self):
		#waiting confirmation
		#receive data from serial			
		try:
			rec_data = self.ser.readline().decode()
		except:
			return False
			
		
		#print("Waiting Confirmation: ", rec_data)
		
		#continue read from serial if no data
		if rec_data == "":
			return False
		else:
			return True
			
	
	def write_serial(self,to_send):
		counter = 0
		
		to_send = to_send.encode()
		confirmed = False
		
		#continue sending data if not received by other rpi
		while not confirmed:
			#print("Sending data: ",to_send)
			
			if self.ser.isOpen() == False:
				#ensures that the serial port is open
				self.ser.open()
				self.ser.flush()

			
			#write to serial port
			self.ser.write(to_send)
			self.ser.close()
			self.ser.open()
			
			#continue to read from serial
			if self.wait_confirmation() == True:
				#print("sent successfully")
				#clos serial
				self.ser.close()
				confirmed = True
				
			counter+=1
			
	def read_serial(self):
		counter = 0
		
		if self.ser.isOpen() == False:
			#ensures that the serial port is open
			self.ser.open()
				
		#receive data from serial
		rec_data = self.ser.readline().decode()
		
		#print(counter, "Other raspi says: ", rec_data)
		
		#continue read from serial if no data
		while rec_data == "":
			counter+=1
			rec_data = self.ser.readline().decode()
			#print(counter, "Other raspi says: ", rec_data)
		
		#print(rec_data)

		#Give confirmation to the other rpi
		#write to serial port
		
		msg = f"received {rec_data} success"
		self.ser.write(msg.encode())
		
		#close serial
		self.ser.close()
		
		return rec_data
			
