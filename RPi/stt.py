import argparse
import stt_selector as stt
import serial
import stt_pb2

parser = argparse.ArgumentParser(prog="STT", description="STT main script")
parser.add_argument("port", type=str, help="Serial Port for RPi")
parser.add_argument("-b", "--baudrate", type=int, help="Baud rate", default=9600)
args = parser.parse_args()

ser = serial.Serial(args.port, args.baudrate)

while True:
    buf = ser.read()
    buf += ser.read(ser.in_waiting)
    print(buf)

    cmd = stt_pb2.StarTrackerCommand()
    cmd.ParseFromString(buf)

    if cmd.cat_division not in (5, 10, 15):
        print("Please introduce a valid catalog division: 5/10/15")

    if cmd.stt_type == "direct_rpi":
        ra, dec, roll, match_std_x, match_std_y = stt.solve_lis_grab_img(cmd.cat_division, cmd.exp_time)
    elif cmd.stt_type == "sample_rpi":
        ra, dec, roll, match_std_x, match_std_y = stt.solve_lis_sample_rpi(cmd.cat_division, cmd.n_pic)
    elif cmd.stt_type == "sample_stereo":
        ra, dec, roll, match_std_x, match_std_y = stt.solve_lis_sample_stereo(cmd.cat_division, cmd.n_pic)
    else:
        print("---> ERROR: Please introduce a valid option to use this STT software (see the Documentation)!")
    
    out = stt_pb2.StarTrackerOutput()
    out.ra = float(ra)
    out.dec = float(dec)
    out.roll = float(roll)
    out.match_std_x = float(match_std_x)
    out.match_std_y = float(match_std_y)

    ser.write(out.SerializeToString())
