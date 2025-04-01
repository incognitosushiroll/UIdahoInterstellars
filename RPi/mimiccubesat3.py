import serial
import stt_pb2
import time
import sliplib

'''
This program mimics the larger NASA Ames CubeSat. This CubeSat will write a command to call either "sample_rpi" or "direct_rpi" in the stt_test.py file, which runs the SOST software needed to determine satellite location. 
There are two commands this python file will send over the serial port depending on which stt_test.py function it wants to call (function descriptions in stt_test.py): 
To call "sample_rpi" to use an onboard photo: 
    - stt_type = "sample_rpi"
    - cat_division = 5, 10, or 15  
    - exp_time = 8 (for 8 ms, recommend don't change)
    - n_pic = 1 - 50 (indices of onboard photos to choose from)

To call "direct_rpi" to take a photo and use it to determine loc: 
    - stt_type = "direct_rpi" 
    - cat_division = 5, 10, or 15 
    - exp_time = 8 (for 8 ms, recommend don't change)

This script will send the command over the serial port and wait to receive the loc data back from stt_test.py. It will read the data in bytes, append the bytes to the buffer, 
check if the byte is the end byte (used to stop reading from the port), and then turn the loc into readable data for interpretation and use. 
'''

ser = serial.Serial("/dev/ttyUSB0", baudrate=9600)

cmd = stt_pb2.StarTrackerCommand()
cmd.stt_type = "sample_rpi"
cmd.cat_division = 5
cmd.exp_time = 8
cmd.n_pic = 8

# Wrap in SLIP before sending
serialized_str = cmd.SerializeToString() 
#serialized_str = serialized_str.replace(sliplib.ESC, sliplib.ESC + sliplib.ESC_ESC).replace(sliplib.END, sliplib.ESC + sliplib.ESC_END)
print(serialized_str)
encoded_cmd = sliplib.encode(serialized_str)
ser.write(encoded_cmd)
print(encoded_cmd)

#time.sleep(1)  # Allow time for processing

# Read byte-by-byte, looking for the SLIP end byte
buffer = bytearray()

while True:
    byte = ser.read(1)  # Read single byte at a time
    if byte:
        #print(byte[0])
        buffer.append(byte[0]) #create the buffer from the individual bytes
        print(buffer)
        try: 
            dec_buf = sliplib.decode(bytes(buffer))
            break 
        except: 
            continue
        '''
        if byte[0] == sliplib.END:  # Check if we reached the end
            print("end")
            break
'''

# while True:
#     while ser.in_waiting or not buffer:  # Keep reading until we have data
#         byte = ser.read(1)  # Read one byte
#         if byte:
#             buffer.append(byte[0])  # Append received byte to buffer
#             if byte[0] == sliplib.END:  # Stop reading when reaching SLIP END
#                 break

#### old loop, ignore #### 
# while True:
#     byte = ser.read(1)  # Read single byte at a time
#     if not byte:
#         break  # Exit if timeout occurs / no byte wrote
#     buffer.append(byte[0]) #create the buffer from the individual bytes
#     if byte[0] == sliplib.END:  # Check if we reached the end
#         break
##########################

# Decode SLIP-wrapped response
try:
    #decoded_data = sliplib.decode(buffer)
    out = stt_pb2.StarTrackerOutput()
    out.ParseFromString(dec_buf)
    print("Received decoded output:", out)
except sliplib.DecodeError:
    print("Error decoding SLIP data.")
except Exception as e:
    print("Error parsing protocol buffer:", e)

# Graceful closeout 
ser.close()