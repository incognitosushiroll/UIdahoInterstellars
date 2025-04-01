import serial
import stt_selector as stt
import stt_pb2
import serial 
import time 

'''This script runs the sample_rpi or direct_rpi functions that calls the stt_functions.py code, which does the calculations to perform LIS. This script will output the LIS coordinates when it receives the direct_rpi commmand from the Cube Sat.'''

# Set up UART on Raspberry Pi (listens for Windows or STM32 messages)
ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=5)

while True:
    buf = ser.read(50)  # Read available data
    # while ser.in_waiting: 
    #     buf += ser.read(ser.in_waiting)

    print("Received raw data:", buf)

    # Parse received protocol buffer
    cmd = stt_pb2.StarTrackerCommand()
    cmd.ParseFromString(buf) 
    # try:
    #     cmd.ParseFromString(buf)
    # except Exception as e:
    #     print("Error parsing protocol buffer:", e)
    #     continue

    # Validate input
    # if cmd.cat_division not in (5, 10, 15):
    #     print("Invalid catalog division. Expected: 5, 10, or 15.")
    #     continue

    print(f"Processing command: Type={cmd.stt_type}, Catalog={cmd.cat_division}")

    # Execute the appropriate function
    if cmd.stt_type == "direct_rpi":
        ra, dec, roll, match_std_x, match_std_y = stt.solve_lis_grab_img(cmd.cat_division, cmd.exp_time)
    if cmd.stt_type == "sample_rpi":
        ra, dec, roll, match_std_x, match_std_y = stt.solve_lis_sample_rpi(cmd.cat_division, cmd.n_pic)
    # else:
    #     print("ERROR: Invalid STT mode received.")
    #     continue

    # Create and send response
    out = stt_pb2.StarTrackerOutput()
    out.ra = float(ra)
    out.dec = float(dec)
    out.roll = float(roll)
    out.match_std_x = float(match_std_x)
    out.match_std_y = float(match_std_y)

    ser.write(out.SerializeToString())
    #time.sleep(5) #Allow time for all data to be sent over 
ser.close() 
