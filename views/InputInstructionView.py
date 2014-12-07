from ttk import Frame
import tkFont
import Tkinter as tk


class InputInstructionView(Frame):
    START_COL = 1
    START_ROW = 0
    COLS_PER_TYPE = 3
    INSTR_BUTTON_WIDTH = 2
    I_BG = "#00AAAA"
    R_BG = "#AA00AA"
    J_BG = "#AAAA00"

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent = parent
#        tk.Grid.__init__(self, parent)
        self.controller = controller
        i_instrs = controller.get_i_instr()
        r_instrs = controller.get_r_instr() 
        j_instrs = controller.get_j_instr() 

        #set title        
        label0=tk.Label(self, width=70, background="#AAAAAA", text="Select Instruction:", font=tkFont.Font(size=20))
        label0.grid(row=0, column=0, columnspan=3*self.COLS_PER_TYPE, sticky=tk.N+tk.E+tk.W)

        label1=tk.Label(self, background=self.I_BG, text="I-Type", font=tkFont.Font(size=15))
        label1.grid(row=1, column=0, columnspan=self.COLS_PER_TYPE, sticky=tk.N)
        label2=tk.Label(self, background=self.R_BG, text="R-Type", font=tkFont.Font(size=15))
        label2.grid(row=1, column= 1 * self.COLS_PER_TYPE, columnspan=self.COLS_PER_TYPE)
        label3=tk.Label(self, background=self.J_BG, text="J-Type", font=tkFont.Font(size=15))
        label3.grid(row=1, column= 2 * self.COLS_PER_TYPE, columnspan=self.COLS_PER_TYPE)

        i_buttons = []
        for index, instr in enumerate(i_instrs):
            i_buttons.append( tk.Button(self, text=instr, width=self.INSTR_BUTTON_WIDTH, background=self.I_BG))
            i_buttons[index].name = instr
            i_buttons[index].grid(row=2+index/self.COLS_PER_TYPE, column = index % self.COLS_PER_TYPE)
            i_buttons[index].bind("<Button-1>", self.instr_button_clicked)

        r_buttons = []
        for index, instr in enumerate(r_instrs):
            r_buttons.append( tk.Button(self, text=instr, width=self.INSTR_BUTTON_WIDTH, background=self.R_BG))
            r_buttons[index].name = instr
            r_buttons[index].grid(row=2+index/self.COLS_PER_TYPE, column = self.COLS_PER_TYPE + index % self.COLS_PER_TYPE)
            r_buttons[index].bind("<Button-1>", self.instr_button_clicked)

        j_buttons = []
        for index, instr in enumerate(j_instrs):
            j_buttons.append( tk.Button(self, text=instr, width=self.INSTR_BUTTON_WIDTH, background=self.J_BG))
            j_buttons[index].name = instr
            j_buttons[index].grid(row=2+index/self.COLS_PER_TYPE, column = 2*self.COLS_PER_TYPE + index % self.COLS_PER_TYPE)
            j_buttons[index].bind("<Button-1>", self.instr_button_clicked)
        
    def instr_button_clicked(self, event):
        print 'Instruction selected: ' + event.widget.name
        self.controller.instruction_selected(event.widget.name)
