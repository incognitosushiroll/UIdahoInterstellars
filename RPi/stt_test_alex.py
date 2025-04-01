import serial
import stt_selector as stt
import stt_pb2
import sliplib
import time

'''This code will be run on the Rpi 5 / compute module and receive commands from the CubeSat in order to run the SOST software, which will output RA, DEC, and ROll. 
This program takes a command from the CubeSat in the form of protocol buffer. We wrap the proto buf using slip lip to tac on an end-byte. 
The end-byte will be used to determine if the full command has been sent across the wire. 
Using the command received, the if statements below will determine which SOST function will be used to determine loc of the CubeSat. 
    - "direct_rpi": Will take a photo using the integrated camera and use that to determine loc 
         *****Note that we will need to change the stt_functions.py and stt_selector.py file depending on what camera we choose!!!****** 
    - "sample_rpi": Will use onboard photo to determine loc, this will be used for testing purposes
Once the location has been determined using these functions, the RA/DEC/ROLL will be formatted into a proto buf and wrapped using slip lib to be sent back over the serial port to the CubeSat (aka: mimiccubesat.py)  
'''

ser = serial.Serial("/dev/ttyAMA0", baudrate=9600) # Removed timeout

while True:
    buffer = bytearray() # Must be byte array to have sliplib encode/decode 

    # While loop to continuously read the bytes sent across the wire 
    while True:
        byte = ser.read(1)  # Read single byte
        if byte:
            buffer.append(byte[0]) #create the buffer from the individual bytes
            try: 
                dec_buf = sliplib.decode(bytes(buffer))
                break 
            except: 
                continue
            #if byte[0] == sliplib.END:  # Check if we reached the end
            #    break

    # Decode the SLIP-wrapped command
    # Ask Alex: do we want a try statement? If the command fails and thus the program fails, will they want an error msg in the form of a proto buf sent back, or do they want it to listen to the port again? 
    # Basically, how do they want us to error handle in space? 
    try:
        #decoded_cmd = sliplib.decode(buffer)
        cmd = stt_pb2.StarTrackerCommand()
        cmd.ParseFromString(dec_buf)

        print(f"Processing command: Type={cmd.stt_type}, Catalog={cmd.cat_division}") # For debugging 

        # Execute command logic
        if cmd.stt_type == "direct_rpi": # Direct_rpi will take a photo and resolve loc
            ra, dec, roll, match_std_x, match_std_y = stt.solve_lis_grab_img(cmd.cat_division, cmd.exp_time)
        if cmd.stt_type == "sample_rpi": # Sample_rpi will use onboard photos to resolve loc
            ra, dec, roll, match_std_x, match_std_y = stt.solve_lis_sample_rpi(cmd.cat_division, cmd.n_pic)

        # Create and send response using proto buf
        out = stt_pb2.StarTrackerOutput()
        out.ra = float(ra)
        out.dec = float(dec)
        out.roll = float(roll)
        out.match_std_x = float(match_std_x) # May not be needed for final loc 
        out.match_std_y = float(match_std_y) # May not be needed for final loc 

        # Wrap response in SLIP and send
        encoded_out = sliplib.encode(out.SerializeToString())
        ser.write(encoded_out)
        print("Sent SLIP-encoded response.")

        time.sleep(5)  # Allow for transmission, see if we can delete this 

    except sliplib.DecodeError:
        print("SLIP decoding error.")
        break 
    except Exception as e:
        print("Error processing command:", e)
        break 

ser.close()