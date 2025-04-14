# ⭐ Star Tracker Linux Setup

This guide will walk you through setting up the Star Tracker project on a Linux system using socat for virtualization of ports and a single device.

---

## 📦 1. Extract the Project Files

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
cd uidaho-stt/RPi
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
