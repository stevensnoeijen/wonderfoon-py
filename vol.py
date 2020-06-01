#!/usr/bin/python3.7

import subprocess
import sys

v = sys.argv[1]

subprocess.call(["amixer", "sset", "Speaker", v + "%"])