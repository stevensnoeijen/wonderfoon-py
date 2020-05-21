#!/usr/bin/python

import alsaaudio
import sys

v = int(sys.argv[1])

m = alsaaudio.Mixer("PCM")
current_volume = m.getvolume() # Get the current Volume
m.setvolume(v) # Set the volume to %.
