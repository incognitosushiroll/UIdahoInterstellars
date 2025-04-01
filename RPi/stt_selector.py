import os
import subprocess as sp
import stt_functions as stt

file_dir = os.path.abspath(os.path.dirname(__file__))
stt_dir = "{}/stt_data".format(file_dir)

def get_photo_index():
    existing_files = [f for f in os.listdir(stt_dir) if f.startswith("stt_img") and f.endswith(".jpg")] 
    indices = [int(f.split("_")[-1].split(".")[0]) for f in existing_files if f.split("_")[-1].split(".")[0].isdigit()] 
    return max(indices, default=0) + 1


def solve_lis_grab_img(cat_division, exposure_time_ms):
    exptime_micros = 1000 * exposure_time_ms
    photo_index = get_photo_index()
    image_dir = os.path.join(stt_dir, f"stt_img{photo_index}.jpg")
    #image_dir = "{}/stt_img.jpg".format(stt_dir) 
    print("\n---> STT: Taking picture with {} ms of exposure time.\n".format(exposure_time_ms))
    task = "libcamera-still -o {} -t 1 --width 1024 --height 1024 --shutter {}".format(image_dir, exptime_micros)
    process = sp.Popen(task, shell=True, stdout=sp.PIPE)
    process.wait()
    return_code = process.returncode
    #inc_photo += inc_photo 
    if return_code != 0:
        raise OSError("---> ERROR: The script in the shell was not correctly executed!")
    return stt.solve_lis(image_dir, cat_division, stt_dir)


def solve_lis_sample_rpi(cat_division, n_pic):
    if n_pic < 1 or n_pic > 50:
        raise ValueError("---> ERROR: --npic must be between 1 and 50")
    print("\n---> STT: Analyzing picture from Sample_images/RPi/img_{}.jpg "
          "using a catalog division of {}.\n".format(n_pic, cat_division))
    image_dir = "{}/Sample_images/RPi/img_{}.jpg".format(file_dir, n_pic)
    return stt.solve_lis(image_dir, cat_division, stt_dir)