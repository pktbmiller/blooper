# blooper (Spark , Katana)
[Demo video Spark GO](https://youtu.be/kttswfzxGsI)

[Demo video KATANA GO](https://youtu.be/Ww5pN00mOyM)

Looper for Positive Grid Spark amps using Raspberry Pi

Tested on Raspberry Pi Zero W and Pi Zero 2 W

Pi 3B has issues with USB audio cards and can run but with minor glitches in playback

Ingredients
  1 Pi Zero W or Pi Zero 2 W

  2 Install Raspberry Pi Lite (32 bit)
  
    Use the Raspberry Pi Image software from Pi website
    
    Configure wireless lan to enable remote login via ssh

  3 boot up and login via ssh

  4 Disable pi internal audio card

    edit /config.tx - comment out line for bcm chip
    dtparam=audio=on
    

  5 Install jack2 

    sudo apt-get install jackd

  6 Install sooperlooper
 
    sudo apt-get install sooperlooper
    
  7 Copy sl.sh and oscb1button.py to home/sll directory
  
  8 use OTG cable and USB-C cable to connect to Mini or Go
  
  9 Make sure spark is powered on
  
  10 cd sll directory
  
  11 run ./sl.sh for Spark (or kat.sh for Katana GO)
  
  TODO
  
  need to install python dependencies 
  
  sudo pip3 install pyhton-osc


  NOTE boot time is long Pi Zero 20-30 secs
  
  Pi 2 Zero <20 secs (networking is still enables to allow ssh)
  
  for me 20 secs is not a big deal for practice and totally portable 
  
