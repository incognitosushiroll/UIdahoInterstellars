# ⭐ Star Tracker Linux Setup

This guide will walk you through setting up the Star Tracker project on a Linux system using socat for virtualization of ports and a single device, as well as using Google Protocol Buffers.

---


## Star Tracker Serial Communication Demo:
Do this once you have cloned the project.

1. Create a fake serial "cable":
```bash
socat -d2 pty,raw,echo=0 pty,raw,echo=0
```

Note the two paths that socat prints: /dev/pts/x and /dev/pts/y.

2. Start stt.py:
```bash
cd ~/UIdahoInterstellars/SOCAT
source .venv/bin/activate
python stt.py /dev/pts/x # replace x with what socat returned
```

3. Use demo.py:
```bash
cd ~/UIdahoInterstellars/SOCAT
source .venv/bin/activate
python demo.py /dev/pts/y sample_rpi 5 -n 22 # replace y with what socat returned
```

Try different values for -n (chooses a sample image from Star_Tracker/RPi/Sample_images/RPi). See python demo.py -h for more options.

## Next, if you'd like to use the Google Protocol Buffer: 
📦 1. Ready the Project Files

After cloning the repo.

```bash
cd SOCAT
```

🔧 2. Install System Dependencies

Ensure the required packages are installed:
```bash
sudo apt install build-essential protobuf-compiler python3-venv socat
```
🚀 3. Set Up the Project Environment

Navigate to the project directory and complete the setup:
```bash
cd UIdahoInterstellars/SOCAT
./linux_installer.sh
./extract_cat.sh
```
Create and activate a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install Python dependencies:
```bash
pip install -r requirements.txt
```
Generate Python code from the Protocol Buffers file:
```bash
protoc --python_out=. stt.proto
```
You are now ready to use the Star Tracker tools! 🛰️
