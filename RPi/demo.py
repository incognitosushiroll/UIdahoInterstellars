import argparse
import serial
import stt_pb2

parser = argparse.ArgumentParser()
parser.add_argument("port", type=str)
parser.add_argument("-b", "--baudrate", type=int, default=9600)
parser.add_argument(
    "type",
    type=str,
    help="The way of running the software: direct_rpi, sample_rpi, sample_stereo.",
)
parser.add_argument(
    "catalog",
    type=int,
    help="The degree of catalog separation in the algorithm: 5, 10, 15.",
)
parser.add_argument(
    "-exp",
    "--exptime",
    type=int,
    help="Exposure time (in ms) of the grabbed picture (in direct mode).",
    default=800,
)
parser.add_argument(
    "-n",
    "--npic",
    type=int,
    help="The number of the picture to analyze (in sample mode).",
    default=1,
)
args = parser.parse_args()

ser = serial.Serial(args.port, args.baudrate)

cmd = stt_pb2.StarTrackerCommand()
cmd.stt_type = args.type
cmd.cat_division = args.catalog
cmd.exp_time = args.exptime
cmd.n_pic = args.npic
print(cmd)
ser.write(cmd.SerializeToString())
print("---")
out = stt_pb2.StarTrackerOutput()
buf = ser.read()
buf += ser.read(ser.in_waiting)
out.ParseFromString(buf)
print(out)

ser.close()
