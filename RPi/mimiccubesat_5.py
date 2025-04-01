import serial
import stt_pb2
import time

'''This script acts as the Cube Sat, sending commands to the star tracker telling it to perform LIS and output the satellite's celestial coordinates using SOST calculations found in stt_functions.py.'''
'''To test this code, we ran this script on a windows 11 machine and ran the stt_test.py script on the rpi 5 with a microSD card running the SOST software from Github'''


ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)
#May have to change the tty0 port to a COM port depending on what the device manager on the windows device says 

cmdtype = "sample_rpi"
catalog = 5
exptime = 8
n_pic = 8

#Send protocol buffer command as if CubeSat sent it
cmd = stt_pb2.StarTrackerCommand()
cmd.stt_type = cmdtype
cmd.cat_division = catalog
cmd.exp_time = exptime
cmd.n_pic = n_pic
ser.write(cmd.SerializeToString())
#print(cmd.SerializeToString())
print(cmd) 

#Allow time for processing 

time.sleep(1) 

#Read protocol buffer location from star tracker



buf = ser.read()
buf += ser.read(ser.in_waiting) 
time.sleep(1) 

#buf = ser.read(ser.in_waiting or 1) #Read available data in buffer 
#while ser.in_waiting: #Continue to read data in buffer until all data has been received 
#    buf += ser.read(ser.in_waiting)

print(buf)
out = stt_pb2.StarTrackerOutput()
out.ParseFromString(buf) 
print(out)

'''
try: 
    out = buf.ParseFromString()
    print(out)
except Exception as e: 
    print("error parsing startrackeroutput:", e)
'''
#Graceful closeout 
ser.close()