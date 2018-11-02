# SmartMirror
SmartMirror project written in Python

### Dependencies
- Software :
  - OpenCV 2.x
  - Python 3.x
  - [Requirements File](requirements.txt)
- Hardware :
  - [Two Way Mirror (18"x14")](https://www.twowaymirrors.com/smart-mirror/)
  - Raspberry Pi 3b+ (You can get away with an older model)
  - Camera (I'm using the PSEye Modified but any camera should do):
      -  I also haven't set up motion capabilites yet either
  - LED Monitor (Preferably that cover the whole surface of your two way mirror)
  
## Setup Hand Recognition and OpenCV
Use this guide: https://www.learnopencv.com/install-opencv-3-on-yosemite-osx-10-10-x/

Make sure you're working in your virtual environment!

Install openCV with 
```shell
brew install opencv
```
## Run!
Start the app
```shell
python3 Window.py
```
 
