#!/usr/bin/env bash

echo "This will now install Quick Q on your Raspberry Pi!"
cd ~
git clone https://github.com/Fasermaler/Quick-Q
echo "Clone successful!"
echo "Installing Kivy"
sudo pip3 install Kivy
echo "Kivy Installed!"

echo "Installing firebase-admin"
sudo pip3 install firebase-admin
echo "firebase-admin installed!"

echo "This will now attempt to build openCV"

read -r -p "Are you sure? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])+$ ]]
then
    "Okay! This will take a while!"

    sudo apt-get update && sudo apt-get upgrade
    sudo apt-get install build-essential cmake pkg-config
    sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
    sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
    sudo apt-get install libxvidcore-dev libx264-dev
    sudo apt-get install libgtk2.0-dev libgtk-3-dev
    sudo apt-get install libatlas-base-dev gfortran
    sudo apt-get install python2.7-dev python3-dev

    echo "Phew! That installs the dependencies, now let's get on to the REAL stuff :D"

    cd ~
	wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.0.zip
	unzip opencv.zip

	echo "Let's grab the contrib packages too!"
	
	wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.3.0.zip
	unzip opencv_contrib.zip

	wget https://bootstrap.pypa.io/get-pip.py
	sudo python get-pip.py
	sudo python3 get-pip.py

	pip install numpy

	echo "No turning back now! Let's GO!"

	cd ~/opencv-3.3.0/
	mkdir build
	cd build
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
    	-D CMAKE_INSTALL_PREFIX=/usr/local \
    	-D INSTALL_PYTHON_EXAMPLES=ON \
    	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    	-D BUILD_EXAMPLES=ON ..


    echo "That wasn't even the real wait! Now is the real wait!"

    make

    echo "Now we just have to install!"
	
	sudo make install
	sudo ldconfig
else

    "Okay, exiting..."
fi

echo "We are done!"

cd ~/Quick-Q

python3 main.py

