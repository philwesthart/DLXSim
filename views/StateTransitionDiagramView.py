import Tkinter as tk
import tkFont
from MicroInstructionStateView import MicroInstructionStateView

class StateTransitionDiagramView(tk.Canvas):
    INSTR_TITLE_COORDS = [425, 60]
    STATE_STRING = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5']
    STATE_SPACING = 120
    STATE_ZERO_COORDS  = [50, 145]
    STATE_ONE_COORDS   = [STATE_SPACING * 1 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_TWO_COORDS   = [STATE_SPACING * 2 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_THREE_COORDS = [STATE_SPACING * 3 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_FOUR_COORDS  = [STATE_SPACING * 4 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_FIVE_COORDS  = [STATE_SPACING * 5 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_COORDS = [STATE_ZERO_COORDS,STATE_ONE_COORDS,STATE_TWO_COORDS,STATE_THREE_COORDS,STATE_FOUR_COORDS,STATE_FIVE_COORDS]
    SUBTITLE_STRING = "Select a microinstruction state to view control signals and data flow on the image to the left"

    def __init__(self, parent, controller):
        self.parent = parent
        tk.Canvas.__init__(self, parent, background='#888888')
        self.controller = controller
        self.controller.set_STDDiagramView(self)
        
        self.ISVs = []
        self.in_quiz_mode = tk.BooleanVar()
        self.draw()

    def load_instruction(self, instr):
        self.ISVs = []
        self.delete(tk.ALL)

        self.create_text(self.INSTR_TITLE_COORDS[0],self.INSTR_TITLE_COORDS[1],text=instr.name, font=tkFont.Font(size=30), anchor=tk.S)
        self.create_text(self.INSTR_TITLE_COORDS[0], self.INSTR_TITLE_COORDS[1], text=self.SUBTITLE_STRING, anchor=tk.N)

        is_last = False
        is_branching = False
        for index, micro_instr in enumerate(instr.micro_instrs):            
            if (index + 1) == instr.num_micro_instructions:
                is_last=True
            if instr.is_branching and index == 3:
                is_branching = True
            else: 
                is_branching = False
            
                            
            self.ISVs.append(MicroInstructionStateView(self, self.STATE_COORDS[index][0], self.STATE_COORDS[index][1], micro_instr, is_last, is_branching, self.controller))
        self.current_instr = instr

        self.draw()

    def quiz_mode_check(self):
        self.controller.in_quiz_mode =  self.in_quiz_mode.get()
        self.draw()
        
        
    def draw(self):
        
        self.quiz_mode_cb = tk.Checkbutton(self, text="Quiz Mode", variable=self.in_quiz_mode, command=self.quiz_mode_check)
        
        self.quiz_cb_window = self.create_window(0,0, anchor=tk.NW, window=self.quiz_mode_cb)
        
        for ISV in self.ISVs:
            ISV.draw()
