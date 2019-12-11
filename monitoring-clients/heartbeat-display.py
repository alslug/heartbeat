#!/usr/bin/env python

import argparse

mote_phat       = 'mote-phat'
usb             = 'usb'
status_phat     = 'status_phat'
status_hat      = 'status-hat'
parser = argparse.ArgumentParser(description='Display status-lights on mote.',fromfile_prefix_chars='@')
mutually_exclusive = parser.add_mutually_exclusive_group(required=True)
parser.add_argument('url',                      help='URL of heartbeat display-object as json', type=str)
mutually_exclusive.add_argument('--mote-phat',  help='Show using mote-phat',    dest='output',   action='store_const', const=mote_phat  )
mutually_exclusive.add_argument('--usb',        help='Show using mote on usb',  dest='output',   action='store_const', const=usb        )
mutually_exclusive.add_argument('--status-phat',help='Show using status-phat',  dest='output',   action='store_const', const=status_phat)
mutually_exclusive.add_argument('--status-hat', help='Show using status-hat',   dest='output',   action='store_const', const=status_hat )
parser.add_argument('--loop',                   help='Keep looping, while refreshing status-bar',action='store_const', const=1, default=0)
args = parser.parse_args()      #'@/etc/heartbeat-display.conf')

print "============================="
print args

if args.output == mote_phat:
        import motephat
        mote=motephat
elif args.output == usb:
        from mote import Mote
        mote = Mote()
        mote.configure_channel(1, 16, False)
        mote.configure_channel(2, 16, False)
        mote.configure_channel(3, 16, False)
        mote.configure_channel(4, 16, False)
elif args.output == status_phat:
        print '--status_phat er ikke implementeret endnu'
        exit(1)
elif args.output == status_hat:
        print '--status_hat er ikke implementeret endnu'
        exit(1)

import json
import time
import requests

loop=True
while loop:
        mote.clear()
        print "============================="
        response = requests.get(args.url)
        beats = json.loads(response.text)
        for beat in beats:
                channel = beat["sorting"] / 16 + 1
                led     = beat["sorting"] % 16
                if channel <= 4:
                        mote.set_pixel( channel,        led,    beat["r"],      beat["g"],      beat["b"]       )
                print channel, led, beat["color"]

        mote.show()
        time.sleep(1)
        loop=args.loop
