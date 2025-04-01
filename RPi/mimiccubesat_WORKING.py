import serial
import stt_pb2
import time

'''This script acts as the Cube Sat, sending commands to the star tracker telling it to perform LIS and output the satellite's celestial coordinates using SOST calculations found in stt_functions.py.'''
'''To test this code, we ran this script on a windows 11 machine and ran the stt_test.py script on the rpi 5 with a microSD card running the SOST software from Github'''


ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout = 100) #dont need timeout if using sliplib
#May have to change the tty0 port to a COM port depending on what the device manager on the windows device says 

cmdtype = "sample_rpi"
catalog = 5
exptime = 8
n_pic = 9

#Send protocol buffer command as if CubeSat sent it
cmd = stt_pb2.StarTrackerCommand()
cmd.stt_type = cmdtype
cmd.cat_division = catalog
cmd.exp_time = exptime
cmd.n_pic = n_pic


#instead of this, wrap in sliplib and send 
ser.write(cmd.SerializeToString())
#print(cmd.SerializeToString())
print(cmd) 

#Allow time for processing 

#time.sleep(1) 

#Read protocol buffer location from star tracker
'''
buf = bytearray()

while True:
    byte = ser.read(1)
    if byte:
        #en_byte = byte.encode("utf-8")
        buf = buf.append(byte[0])
        print(byte)
        end_byte = "9"
        en_end = end_byte.encode("utf-8")
        if byte[0] == en_end: 
            break
        '''

#dec_buf = buf.decode("utf-8")

'''    byte = ser.read(1)  # Read single byte at a time
    if byte:
        #print(byte[0])
        buffer.append(byte[0]) #create the buffer from the individual bytes
        print(buffer)
        try: 
            dec_buf = .decode(bytes(buffer))
            break 
        except: 
            continue
'''
while ser.in_waiting == 0:
    time.sleep(0.2)
buf = ser.read()
# end = bytes(9) 
# print(buf)
# while end not in buf: 
#     buf += ser.read()
#     print(buf)
# print("end seen")
# buf = buf 
while ser.in_waiting:
    buf += ser.read(ser.in_waiting) 


#buf = ser.read() #read shoud be wrapped in a while loop and read byte at a time, checking for end code byte 
#read byte and store into byte buffer, pass into sliplib decode function, if function returns "none" then keep reading
'''
end = 1
while end not in buf:
    buf += ser.read()
'''

#print(buf)
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