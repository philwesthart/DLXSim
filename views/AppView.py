import Tkinter as tk
from ttk import Frame
from controller import Controller
from DLXDataPathView import DLXDataPathView
from InputInstructionView import InputInstructionView
from StateTransitionDiagramView import StateTransitionDiagramView
from MicroInstructionStateView import MicroInstructionStateView

class AppView(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = Controller()
        
        self.current_instruction = 1
            
        #load DLX image
        self.DLXDPV = DLXDataPathView(self.parent, self.controller)
        self.DLXDPV.grid(row=0, column=0, rowspan=2)

        #load inputs
        self.InputInstructionView = InputInstructionView(self.parent, self.controller)
        self.InputInstructionView.grid(row=0, column=1, sticky=tk.N)

        #load STD View
        self.STD_canvas = StateTransitionDiagramView(self.parent, self.controller)
        self.STD_canvas.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W, columnspan=3)

