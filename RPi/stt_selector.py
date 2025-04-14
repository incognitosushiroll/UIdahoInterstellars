import os
import subprocess as sp

def get_photo_index():
    existing_files = [f for f in os.listdir(stt_dir) if f.startswith("stt_img") and f.endswith(".jpg")]
    indices = []

    for f in existing_files:
        try:
            idx = int(f.split("_")[-1].split(".")[0])
            indices.append(idx)
        except ValueError:
            continue

    return max(indices) + 1 if indices else 0

def solve_lis_grab_img(cat_division, exposure_time_ms):
    exptime_micros = 1000 * exposure_time_ms
    photo_index = get_photo_index()
    image_path = os.path.join(stt_dir, f"stt_img{photo_index}.jpg")

    print(f"\n---> STT: Taking picture with {exposure_time_ms} ms of exposure time.\n")

    task = f"libcamera-still -o {image_path} -t 1 --width 1024 --height 1024 --shutter {exptime_micros}"
    process = sp.Popen(task, shell=True, stdout=sp.PIPE)
    process.wait()

    if process.returncode != 0:
        raise OSError("---> ERROR: The script in the shell was not correctly executed!")

    return stt.solve_lis(image_path, cat_division, stt_dir)



def solve_lis_sample_rpi(cat_division, n_pic):
    if n_pic < 1 or n_pic > 50:
        raise ValueError("---> ERROR: --npic must be between 1 and 50")
    print("\n---> STT: Analyzing picture from Sample_images/RPi/img_{}.jpg "
          "using a catalog division of {}.\n".format(n_pic, cat_division))
    image_dir = "{}/Sample_images/RPi/img_{}.jpg".format(file_dir, n_pic)
    return stt.solve_lis(image_dir, cat_division, stt_dir)
