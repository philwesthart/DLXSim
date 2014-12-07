#!/usr/bin/python
import sys
import os
sys.path.append(os.path.abspath('./models'))
sys.path.append(os.path.abspath('./views'))
sys.path.append(os.path.abspath('./controllers'))
import Tkinter as tk
from AppView import AppView

# Instantiate Tkinter root 
root = tk.Tk()
root.wm_title("DLX Datapath Learning Simulator")

# Create App View
view = AppView(root)

# Start main loop
root.mainloop()
