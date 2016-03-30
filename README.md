Solution of Rush hour

1. Initialize the squares and cars
  At first, 36 squares with index from 0 - 35 are initialized. The position of a square is determined as
  x = index % 6
  y = index / 6
  x is the row number of the square, and y is the column number of the square.
  A square object has properties of occupied and car. If there is a car on the square, square.occupied = True and square.car = car.name. Otherwise sqaure.occupied = False and square.car = None.
  The car objects A, B, C, E, F, G, H, I, J, R are intialized. A car object has two possible orientations, 'h' meaning horizontal and 'v'meaning vertical. A car can occupy 2 or 3 squares and only move in its orientation.
  A car object also has freedom properties, namely freedom_left, freedom_right, freedom_up and freedom_down. The freedom indicates the number of unoccupied squares before and after the car.  

2. Move the cars
  For each car, the range of possible squares to move to are searched by calling car.get_freedom().  Then a square is randomly selected from  the range. If the car could move to the square without overlapping with other cars or protruding the border of the board, the positions of the car is updated to the new position. If there are no unoccupied squares before or after the car, the position of the car remains the same.

3. Create the graph
  The problem is converted to a graph. All possible configurations of the cars are explored until a winning configuration is found where there are no other cars in the row of R. Each configuration is a vertex. The distance between every two vertices are calculated. A vertex is connected to its nearest neighbors. Breadth-first search is performed to find the shortest path from the initial configuration to the winning configuration. When the shortes path is found, all of the moves in the path are recorded.

4. Show the solution in animation
  The moves in the shortest path are shown in animation using pygame. 

Appendices:

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

In windows:
go to http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
pygame-1.9.2a0-cp27-none-win32.whl
pygame-1.9.2a0-cp27-none-win_amd64.whl
pygame-1.9.2a0-cp34-none-win32.whl
pygame-1.9.2a0-cp34-none-win_amd64.whl
pygame-1.9.2a0-cp35-none-win32.whl
pygame-1.9.2a0-cp35-none-win_amd64.whl
