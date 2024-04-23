#!/bin/bash

# wait for booting to complete
# make the pi zero green led off
sudo sh -c "echo none > /sys/class/leds/ACT/trigger"

sleep 1

# necessary to start jack
export DISPLAY=:0

# end previous processes
killall -9 jackd || echo "jackd was not running."
killall -9 sooperlooper || echo "sooperlooper was not running."
sudo killall -9 python || echo "python was not running."
sudo killall -9 python3 || echo "python was not running."
# start jack server

# this line should also be in ~/.jackdrc, because if the below line fails, sooperlooper will start its own jackd using the config in ~/.jac
# for pi zero use -p512
# for pi zero 2 use -p256 (for spark go, -p128 seemed to work but saw xruns on Spark Mini)(KatanaGo -p128 works very well) 
/usr/bin/jackd --realtime -P95 -t2000 -dalsa -r48000 -p128 -n3 -dhw:KATANAGO &
sudo sh -c "echo timer > /sys/class/leds/ACT/trigger"
sleep 3

# start sooperlooper
#/usr/bin/sooperlooper -L sess.slsess -p 9951 -l 1 -c 1 -t 120 &
# for Katana GO we can use stereo
/usr/bin/sooperlooper -p 9951 -l 1 -c 2 -t 120 &

# wait for sooperlooper to start
sleep 1

# list port names
jack_lsp -c
# make the connections from audio card to looper
jack_connect system:capture_1 sooperlooper:common_in_1 || (echo "error connecting audio (1)"; echo "sleep 5"; sleep 5 ; jack_connect system:capture_1 sooperlooper:common_in_1)
jack_connect system:capture_2 sooperlooper:common_in_2 || (echo "error connecting audio (1)"; echo "sleep 5"; sleep 5 ; jack_connect system:capture_1 sooperlooper:common_in_2)

jack_connect sooperlooper:common_out_1 system:playback_1 || echo "error connecting audio (2)"
jack_connect sooperlooper:common_out_2 system:playback_2 || echo "error connecting audio (2)"

sudo sh -c "echo heartbeat  > /sys/class/leds/ACT/trigger"
sudo python3 /home/pm04/sll/oscb1button.py &
sudo sh -c "echo none > /sys/class/leds/ACT/trigger"

