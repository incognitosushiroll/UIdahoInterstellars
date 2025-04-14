# UIdaho Interstellars - RPi Star Tracker Setup

This guide provides the steps to set up the UI Interstellar Capstone Team Star Tracker system on a Raspberry Pi using the original SPEL SOST source code. 

NOTE: This setup is used for those wanting a two-device system, with one device running the mimic_cubesat code and the other running the stt_test code to mimic the star tracker. These two devices are meant to be set-up using UART and serial ports. If you don't wish to use this additional hardware, follow the instructions inside the SOCAT folder for a virtual port implementation. 

## 📦 Repository Setup

After cloning the repository, navigate to the correct directory and run the setup scripts:

```bash
cd UIdahoInterstellars/RPi
sh linux_installer.sh
sudo sh extract_cat.sh
```

🔧 Dependencies

Ensure the following Python packages are installed:
```bash
python3 -m pip install astropy pillow
sudo apt install python3-numpy
```
    Note: If you encounter an error while installing astropy, it may be due to the environment being externally managed. See the fix below.

🛠️ Fix for EXTERNALLY-MANAGED Environment Error

If you receive an error related to a managed environment while installing astropy, you can resolve it by:

```bash
cd ~
sudo rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED
cd ~/UIdahoInterstellars/RPi
sudo apt-get install libjpeg-dev zlib1g-dev
python3 -m pip install astropy pillow
```
    ⚠️ This step may take some time depending on your internet connection and system resources.

🚀 Test the Setup

Run the stt.py script with a sample dataset to verify your setup:

```bash
python3 stt.py sample_rpi 5 --npic 2
```
📚 Full Documentation

For the full instructions and original source code, visit the SPEL SOST GitHub repository:
👉 https://github.com/spel-uchile/Star_Tracker/tree/master
