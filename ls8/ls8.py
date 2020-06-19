# !/usr / bin / env python3
from cpu import *
import sys

"""Main."""


cpu = CPU()

cpu.load(sys.argv[1])
# cpu.load('examples/call.ls8')


cpu.run()
