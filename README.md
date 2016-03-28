1. Install Pygame
Before installing Pygame, the latest development libraries of SDL is installed at first. To install SDL:
sudo apt-get install build-essential xorg-dev libudev-dev libts-dev libgl1-mesa-dev libglu1-mesa-dev libasound2-dev libpulse-dev libopenal-dev libogg-dev libvorbis-dev libaudiofile-dev libpng12-dev libfreetype6-dev libusb-dev libdbus-1-dev zlib1g-dev libdirectfb-dev 
go to: http://www.libsdl.org/download-2.0.php download "SDL2-2.0.4.tar.gz" extract the archive (tar -xvzf SDL2-2.0.4.tar.gz) and run the follow commands:
./configure
make
sudo make install

sudo apt-get install libsdl1.2-dev
sudo apt-get install libsmpeg-dev
sudo apt-get install libv41
cd /usr/include/linux
sudo ln -s ../libv4l1-videodev.h videodev.h
sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev
sudo apt-get install python-pygame
