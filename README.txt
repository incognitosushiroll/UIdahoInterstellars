After cloning from the repo, follow these steps: 

cd UIdahoInterstellars/RPi
sh linux_installer.sh
sudo sh extract_cat.sh

To ensure astropy and numpy are installed, run:
python3 -m pip install astropy pillow
sudo apt install python3-numpy

Test the set-up process w/ SPEL SOST "stt.py" by running:
python3 stt.py sample_rpi 5 --npic 2


Note, that if you get an error while trying to install astropy, it may be an issue with the environment being externally managed. To fix:

cd ~
sudo rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED
cd ~/UIdahoInterstellars/RPi
sudo apt-get install libjpeg-dev zlib1g-dev
python3 -m pip install astropy pillow

*this may take a second to download

For full instructions from SPEL SOST source code, visit:
https://github.com/spel-uchile/Star_Tracker/tree/master
