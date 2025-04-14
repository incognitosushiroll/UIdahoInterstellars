# Navigate to project directory
cd UIdahoInterstellars/RPi || { echo "Directory UIdahoInterstellars/RPi not found."; exit 1; }

# Run installation scripts
echo "Running linux_installer.sh..."
sh linux_installer.sh

echo "Extracting catalog..."
sudo sh extract_cat.sh

# Install Python dependencies
echo "Installing Python packages: astropy and pillow..."
python3 -m pip install astropy pillow

echo "Installing system package: python3-numpy..."
sudo apt update
sudo apt install -y python3-numpy

echo "Setup complete!"
