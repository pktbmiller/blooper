import argparse
import random
import time
from typing import List, Any

from pythonosc import udp_client

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.osc_server import AsyncIOOSCUDPServer

from gpiozero import Button, LED
import asyncio


blue = LED(25)
red = LED(23)

newstate = 0

def state_handler(address, *args):
     global newstate 
     newstate = args[2]
     if newstate == 0 or newstate == 20:
       blue.off()
       red.off()
       buttons[0]["cmd"] = "record"
       buttons[0]["longcmd"] = None
     elif newstate == 2:
       red.on()
       blue.off()
       buttons[0]["cmd"] = "record"
     elif newstate == 4:
       blue.on()
       red.off()
       buttons[0]["cmd"] = "overdub"
     elif newstate == 5:
       red.on()
       blue.off()
       buttons[0]["cmd"] = "overdub"
       buttons[0]["longcmd"] = "undo"
     elif newstate == 10:
       red.off()
       blue.blink(0.25,0.25)
       buttons[0]["cmd"] = "trigger"


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

dispatcher = Dispatcher()
dispatcher.map("/state", state_handler)
dispatcher.set_default_handler(default_handler)

ip = "0.0.0.0"
port = 9959
buttons = [{"but":Button(5),  "state": False, "up":0, "down":0, "count":0, "cmd":"record", "longcmd":None}]

async def loop():
  global newstate
  # get then intial state of button so that we can use no or nc switch
  bstart = buttons[0]["but"].is_pressed
  client = udp_client.SimpleUDPClient("127.0.0.1", 9951)
  client.send_message("/sl/-1/register_auto_update", ["state", 10, "osc.udp://127.0.0.1:9959/", "/state"])
  while True:
    for button in buttons:
      # handle debounce
      if button["count"] > 0:
        button["count"] -= 1
      else:
        b = button["but"].is_pressed != bstart
        if b != button["state"]:
          if b:
            if button["up"] < 40:
              client.send_message("/sl/0/hit", "mute")
            else:
              client.send_message("/sl/0/hit", button["cmd"])
            button["state"] = True
            button["count"] = 10
            button["down"] = 0
          else:
            #client.send_message("/sl/0/up", button["cmd"])
            button["state"] = False
            button["count"] = 10
            button["up"] = 0
        else:
          if b:
            button["down"] += 1
            if button["down"] > 100:
               button["down"] = 0
               if newstate == 10:
                 client.send_message("/sl/0/hit", "undo_all")
               elif newstate == 5:
                 client.send_message("/sl/0/hit", "overdub")
                 client.send_message("/sl/0/hit", "undo")
                 client.send_message("/sl/0/hit", "undo")
               else:                 
                 client.send_message("/sl/0/hit", "undo")
          else:
            button["up"] += 1

    time.sleep(0.01)
    await asyncio.sleep(0)



async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())
