""" fauxmo_minimal.py - Fabricate.IO

    This is a demo python file showing what can be done with the debounce_handler.
    The handler prints True when you say "Alexa, device on" and False when you say
    "Alexa, device off".

    If you have two or more Echos, it only handles the one that hears you more clearly.
    You can have an Echo per room and not worry about your handlers triggering for
    those other rooms.

    The IP of the triggering Echo is also passed into the act() function, so you can
    do different things based on which Echo triggered the handler.
"""

import fauxmo
import logging
import time
import pyamp
import pytv

def call_tv(state):
   print("Call TV tv to ", state)
   command = "ON"
   if state == False : 
      command = "OFF"
   tv.handleCommand(command)
   return True

def call_amp_mute(state):
   print("Call amp tv to ", state)
   command = "ON"
   if state == False : 
      command = "OFF"
   amp.set_mute(command)
   return True

def call_amp_power(state):
   print("Call amp tv to ", state)
   command = "ON"
   if state == False : 
      command = "STANDBY"
   amp.set_power(command)
   return True

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the device name being triggered
    """
    TRIGGERS = {"lounge tv": 52000, "stereo": 52001, "lounge mute": 52002}
    HANDLERS = {"lounge tv": call_tv, "stereo": call_amp_power, "lounge mute": call_amp_mute}

    def act(self, device_name, state):
        print("State", state, "for device ", device_name)
        return self.HANDLERS[device_name](state)

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    amp = pyamp.ampControl("192.168.1.56",23)

    tv  = pytv.tvControl("192.168.1.55",8080,"676905") 

    result = tv.connect()
    if result != "OK" :
       print("FAILED to connect to TV:",result)  

    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: " + str(e))
            break
