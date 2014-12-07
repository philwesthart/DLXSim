#!/usr/bin/python

import sys
import os
sys.path.append(os.path.abspath('./models'))
sys.path.append(os.path.abspath('./views'))
sys.path.append(os.path.abspath('./controllers'))
import Tkinter as tk
import Image, ImageTk
from ttk import Frame
import tkFont
from controller import Controller

root = tk.Tk()

# Full screen app class
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

class MicroInstructionStateView():
    CIRCLE_WIDTH  = 30
    CIRCLE_HEIGHT = 30
    ARROW_LENGTH = 80
    ARROW_HEAD_LENGTH = 8
    ARROW_HEAD_HEIGHT = 10
    MEM_WAIT_STRING = 'MW = 1/...'
    QUIZ_COORDS = [26,30, 144, 150]
    QUIZ_BOX_COLOR = '#DEAD01'
    
    
    def __init__(self, parent_canvas, x, y, instr, is_last, is_branching, controller):
        self.canvas = parent_canvas
        self.x = x
        self.y = y
        self.instr = instr
        self.instr_state = instr.state_string
        self.fill="white"
        self.selected = False
        self.controller = controller
        self.control_signals = instr.control_signals
        self.has_mem_wait = instr.has_mem_wait
        self.is_last = is_last
        self.is_branching = is_branching

        self.first_draw = True
        self.draw()
        self.first_draw = False
        

    def set_selected(self, selected):
        self.selected = selected
        self.draw()

    def click_handler(self, event):

        self.selected = not self.selected

        self.draw()
        self.controller.micro_instruction_state_clicked(self)

    def draw(self):
        #delete redrawn objects
        if hasattr(self, 'circle'):
            self.canvas.delete(self.circle)
        if hasattr(self, 'circle_text'):
            self.canvas.delete(self.circle_text)

        #draw a circle for the state
        if not self.selected:
            self.fill = "white"
        else:
            self.fill = "lightgreen"
        self.circle = self.canvas.create_oval(self.x, self.y, self.x + self.CIRCLE_WIDTH, self.y + self.CIRCLE_HEIGHT, fill=self.fill)

        #add click handler for circle
        self.canvas.tag_bind(self.circle, "<Button-1>", self.click_handler)
        
        #draw circle state text
        self.circle_text = self.canvas.create_text(self.x + self.CIRCLE_WIDTH/2, self.y + self.CIRCLE_HEIGHT/2, text=self.instr_state)
        self.canvas.tag_bind(self.circle_text, "<Button-1>", self.click_handler)

        if self.first_draw:
            #draw next state arrow
            self.canvas.create_line(self.x + self.CIRCLE_WIDTH, self.y + self.CIRCLE_WIDTH/2, self.x + self.CIRCLE_WIDTH + self.ARROW_LENGTH, self.y+self.CIRCLE_WIDTH/2)
            self.canvas.create_polygon(self.x + self.CIRCLE_WIDTH + self.ARROW_LENGTH + self.ARROW_HEAD_LENGTH, self.y + self.CIRCLE_WIDTH/2, self.x  + self.CIRCLE_WIDTH + self.ARROW_LENGTH, self.y + self.CIRCLE_WIDTH/2 + self.ARROW_HEAD_HEIGHT/2, self.x + self.CIRCLE_WIDTH + self.ARROW_LENGTH, self.y + self.CIRCLE_WIDTH/2 - self.ARROW_HEAD_HEIGHT/2)

            #make input label

            #make control signals label
            con_sig = ''
            for key, val in self.control_signals.items():
                con_sig = con_sig + key + ' = ' + str(val) + '\n'
            self.canvas.create_text(self.x + self.CIRCLE_WIDTH, self.y + self.CIRCLE_WIDTH,text=con_sig, anchor=tk.NW)

            #add memwait loop if necessary
            if self.has_mem_wait:
                self.canvas.create_arc(self.x, self.y, self.x+self.CIRCLE_WIDTH, self.y - self.CIRCLE_WIDTH, start=-45, extent=270, style='arc')
                self.canvas.create_polygon(self.x, self.y, self.x+10, self.y-10, self.x + 10, self.y)
                self.canvas.create_text(self.x + self.CIRCLE_WIDTH/2, self.y - self.CIRCLE_WIDTH, anchor=tk.S, text=self.MEM_WAIT_STRING)

            #draw branch for branching instruction
            if self.is_branching:
                self.canvas.create_line(self.x + self.CIRCLE_WIDTH/2, self.y, 
                                           self.x + self.CIRCLE_WIDTH/2, self.y - self.CIRCLE_WIDTH/2,
                                           self.x + 3*self.CIRCLE_WIDTH/2 + self.ARROW_LENGTH + self.ARROW_HEAD_LENGTH, self.y - self.CIRCLE_WIDTH/2,
                                           self.x + 3*self.CIRCLE_WIDTH/2 + self.ARROW_LENGTH + self.ARROW_HEAD_LENGTH, self.y 
                                           )
                self.canvas.create_polygon(self.x + 3*self.CIRCLE_WIDTH/2 + self.ARROW_LENGTH + self.ARROW_HEAD_LENGTH, self.y ,
                                           self.x + 3*self.CIRCLE_WIDTH/2 + self.ARROW_LENGTH + self.ARROW_HEAD_LENGTH - self.ARROW_HEAD_HEIGHT/2, self.y - self.ARROW_HEAD_LENGTH,
                                           self.x + 3*self.CIRCLE_WIDTH/2 + self.ARROW_LENGTH + self.ARROW_HEAD_LENGTH + self.ARROW_HEAD_HEIGHT/2, self.y - self.ARROW_HEAD_LENGTH
                                           )

            #if last state, draw S0
            if self.is_last:
                self.canvas.create_oval(self.x + self.CIRCLE_WIDTH + self.ARROW_LENGTH + self.ARROW_HEAD_LENGTH, self.y, self.x + 2 * self.CIRCLE_WIDTH + self.ARROW_LENGTH + self.ARROW_HEAD_LENGTH, self.y + self.CIRCLE_WIDTH, fill="white" )
                self.canvas.create_text(self.x + 3* self.CIRCLE_WIDTH/2 + self.ARROW_LENGTH + self.ARROW_HEAD_LENGTH, self.y + self.CIRCLE_HEIGHT/2, text="S0")

            self.first_draw = False
        
                # If in quiz mode, draw blank-out box
            self.quiz_box = self.canvas.create_polygon(self.x + self.QUIZ_COORDS[0], self.y + self.QUIZ_COORDS[1],
                                self.x + self.QUIZ_COORDS[2], self.y + self.QUIZ_COORDS[1],
                                self.x + self.QUIZ_COORDS[2], self.y + self.QUIZ_COORDS[3],
                                self.x + self.QUIZ_COORDS[0], self.y + self.QUIZ_COORDS[3],
                                fill=self.QUIZ_BOX_COLOR, outline='black'
                                )
            self.canvas.tag_bind(self.quiz_box, '<Button-1>', self.quiz_box_clicked)
            self.quiz_box_visible = True
        self.draw_quiz_box()

    def draw_quiz_box(self):
        if self.controller.in_quiz_mode:
            if self.quiz_box_visible:
                self.canvas.itemconfig(self.quiz_box, fill=self.QUIZ_BOX_COLOR)
            else:
                self.canvas.itemconfig(self.quiz_box, fill='')
        else:
            self.canvas.itemconfig(self.quiz_box, fill='')  

    def quiz_box_clicked(self, event):
        print "Quiz box clicked!"
        if self.controller.in_quiz_mode:
            self.quiz_box_visible = not self.quiz_box_visible
            self.draw_quiz_box()
        else:
            self.canvas.itemconfig(self.quiz_box, fill='')            
        pass



def click_handler(event):
    print "[" + str(event.x) + ', ' + str(event.y) + "],"

class DLXDataPathView(tk.Canvas):
    WIDTH=550
    HEIGHT=700
#####Control Signal Lines ####
    S2OP_LINE = [[97,31], [317,31], [317,49]]
    ZFLAG_LINE = [[91, 41],[130, 41],[130, 80],[356, 80],[356, 67],[339, 67]]
    ALUOP_LINE = [[94, 61],[115, 61],[115, 90],[333, 90],[333, 78]]
    CLOAD_LINE = [[94,77], [110, 77], [110, 96], [441,96], [441, 150]]
    REGLOAD_LINE = [[94, 91], [106,91],[106,101],[391, 101],[391, 140]]
    ALOAD_LINE = [[95, 106], [229, 106], [229, 124]]
    AOE_LINE = [[95, 119], [120, 119], [120, 110], [219, 110], [219, 125]]
    BLOAD_LINE = [[93,135],[122,136],[122,155],[229,155],[229,168]]
    BOE_LINE = [[95,152],[115,150],[115,159],[219,161],[219,169]]
    REGSELECT_LINE = [[95,204],[361,204],[361,214]]
    IRLOAD_LINE = [[96,254],[362,254],[362,262]]
    IROES1_LINE = [[94,269],[126,268],[126,288],[263,288],[263,282]]
    IROES2_LINE = [[94,285],[116,285],[116,293],[274,293],[274,281]]
    OPCODE_LINE = [[96,298],[283,299],[283,282]]
    OPCODEALU_LINE = [[96,314],[363,314],[363,281]]
    RESET_LINE = [[95,328],[314,328],[314,347]]
    PCLOAD_LINE = [[95,342],[126,342],[126,334],[363,334],[363,346]]
    PCOES1_LINE = [[93,357],[126,357],[126,372],[263,372],[263,364]]
    PCMARSELECT_LINE = [[95,432],[387,432],[387,392],[422,391],[422,417]]
    MARLOAD_LINE = [[94,447],[361,447],[361,455]]
    MEMREAD_LINE = [[96,476],[422,477],[421,499],[422,477],[130,477],[130,564],[363,565],[363,593]]
    MDRLOAD_LINE = [[95,490],[363,490],[363,510]]
    MDROES2_LINE = [[94,505],[116,505],[116,496],[264,497],[264, 509]]
    MEMWRITE_LINE = [[94, 520],[116, 520],[116,539],[362,539],[362,527],[362, 539], [116, 539],[116,569],[348,569],[348,593]]
    MEMOP_LINE = [[95, 575],[332,575],[332, 592]]
    MEMWAIT_LINE = [[96, 636],[253, 636]]

#####Data Lines ####
    DATA_COLOR = "blue"
    IR_TO_S1_LINE = [[253,270], [145,269],[145,73],[312,73]]
    IR_TO_S2_LINE = [[254, 274], [175, 274],[175, 53],[312, 53]]
    B_TO_S2_LINE = [[214, 180],[175, 180],[175, 53],[312, 53]]
    A_TO_S1_LINE = [[215, 136],[145, 136],[145, 71],[312, 71]]
    PC_TO_S1_LINE = [[253, 353],[146, 353],[146, 71],[312, 71]]
    MDR_TO_S2_LINE = [[253, 515],[175, 515],[175, 53],[312, 53]]
    ALU_TO_C_LINE = [[338, 63],[486, 63],[486, 161],[457, 161]]
    ALU_TO_PC_LINE = [[338, 62],[487, 62],[487, 353],[373, 353]]
    ALU_TO_MAR_LINE = [[338, 61],[486, 61],[486, 466],[373, 466]]
    PC_TO_MUX_LINE = [[373, 358],[392, 358],[392, 428],[410, 428]]
    MAR_TO_MUX_LINE = [[373, 461],[391, 461],[391, 443],[410, 443]]
    ADDR_TO_MEM_LINE = [[433, 432],[511, 432],[511, 653],[373, 653]]
    MDR_TO_MEM_LINE = [[373, 521],[392, 521],[392, 546],[535, 546],[535, 614],[373, 614]]
    MEM_TO_PC_LINE = [[373, 615],[535, 615],[535, 269],[373, 267]]
    MEM_TO_IR_LINE = [[373, 615],[534, 615],[534, 269],[373, 269]]
    REG_TO_A_LINE = [[294, 137],[234, 137]]
    REG_TO_B_LINE = [[294, 182],[234, 182]]
    C_TO_REG_LINE = [[435, 161],[372, 161]]
    MUX_TO_MDR_LINE = [[411, 516],[373, 516]]
    ALU_TO_MDR_MUX_LINE = [[338, 62],[485, 62],[485, 526],[433, 526]]
    MEM_TO_MDR_MUX_LINE = [[373, 614],[534, 614],[534, 510],[433, 510]]

    def __init__(self, parent, controller):
        self.parent = parent
        tk.Canvas.__init__(self, parent, width=self.WIDTH, height=self.HEIGHT)
        self.controller = controller
        self.controller.set_DLXDataPathView(self)

        self.photo = tk.PhotoImage(file="/home/pwest/Code/DLXSim/images/DLXCPU.gif")

        self.bind("<Button-1>", click_handler)
        
        #self.control_signals = {'S2OP':1, 'ALUOP':2, 'ZFLAG':1, 'CLOAD':1, 'REGLOAD':1, 'ALOAD':1, 'AOE': 1, 'BLOAD':1, 'BOE':1, 'REGSELECT':1, 'IRLOAD':1, 'IROES1':1, 'IROES2':1, 'OPCODE':1, 'OPCODEALU':1, 'RESET':1,'PCLOAD':1, 'PCOES1':1, 'PCMARSELECT':1,'MARLOAD':1,'MEMREAD':1,'MDRLOAD':1,'MDROES2':1,'MEMWRITE':1,'MEMOP':1, 'MEMWAIT':1}
        self.control_signals = {}

        self.draw()

    def set_control_signals(self, signals):
        self.control_signals = signals
        self.draw()

    def draw(self):
        self.delete(tk.ALL)

        self.image = self.create_image(0,0,image=self.photo, anchor=tk.NW)
        if 'S2OP' in self.control_signals:
            self.draw_poly_line(self.S2OP_LINE)
        if 'ZFLAG' in self.control_signals:
            self.draw_poly_line(self.ZFLAG_LINE)
        if 'ALUOP' in self.control_signals:
            self.draw_poly_line(self.ALUOP_LINE)
        if 'CLOAD' in self.control_signals:
            self.draw_poly_line(self.CLOAD_LINE)
            self.draw_poly_line(self.ALU_TO_C_LINE, self.DATA_COLOR, True)
        if 'REGLOAD' in self.control_signals:
            self.draw_poly_line(self.REGLOAD_LINE)
            self.draw_poly_line(self.C_TO_REG_LINE, self.DATA_COLOR, True)
        if 'ALOAD' in self.control_signals:
            self.draw_poly_line(self.ALOAD_LINE)
            self.draw_poly_line(self.REG_TO_A_LINE, self.DATA_COLOR, True)
        if 'AOE' in self.control_signals:
            self.draw_poly_line(self.AOE_LINE)
            self.draw_poly_line(self.A_TO_S1_LINE, self.DATA_COLOR, True)
        if 'BLOAD' in self.control_signals:
            self.draw_poly_line(self.BLOAD_LINE)
            self.draw_poly_line(self.REG_TO_B_LINE, self.DATA_COLOR, True)
        if 'BOE' in self.control_signals:
            self.draw_poly_line(self.BOE_LINE)
            self.draw_poly_line(self.B_TO_S2_LINE, self.DATA_COLOR, True)
        if 'REGSELECT' in self.control_signals:
            self.draw_poly_line(self.REGSELECT_LINE)
        if 'IRLOAD' in self.control_signals:
            self.draw_poly_line(self.IRLOAD_LINE)
            self.draw_poly_line(self.MEM_TO_IR_LINE, self.DATA_COLOR, True)
        if 'IROES1' in self.control_signals:
            self.draw_poly_line(self.IROES1_LINE)
            self.draw_poly_line(self.IR_TO_S1_LINE, self.DATA_COLOR, True)
        if 'IROES2' in self.control_signals:
            self.draw_poly_line(self.IROES2_LINE)
            self.draw_poly_line(self.IR_TO_S2_LINE, self.DATA_COLOR, True)
        if 'OPCODE' in self.control_signals:
            self.draw_poly_line(self.OPCODE_LINE)
        if 'OPCODEALU' in self.control_signals:
            self.draw_poly_line(self.OPCODEALU_LINE)
        if 'RESET' in self.control_signals:
            self.draw_poly_line(self.RESET_LINE)
        if 'PCLOAD' in self.control_signals:
            self.draw_poly_line(self.PCLOAD_LINE)
            self.draw_poly_line(self.ALU_TO_PC_LINE, self.DATA_COLOR, True)
        if 'PCOES1' in self.control_signals:
            self.draw_poly_line(self.PCOES1_LINE)
            self.draw_poly_line(self.PC_TO_S1_LINE, self.DATA_COLOR, True)
        if 'PCMARSELECT' in self.control_signals:
            self.draw_poly_line(self.PCMARSELECT_LINE)
            self.draw_poly_line(self.ADDR_TO_MEM_LINE, self.DATA_COLOR, True)
            if self.control_signals['PCMARSELECT'] == 0:
                self.draw_poly_line(self.PC_TO_MUX_LINE, self.DATA_COLOR, True)
            else:
                self.draw_poly_line(self.MAR_TO_MUX_LINE, self.DATA_COLOR, True)
        if 'MARLOAD' in self.control_signals:
            self.draw_poly_line(self.MARLOAD_LINE)
            self.draw_poly_line(self.ALU_TO_MAR_LINE, self.DATA_COLOR, True)
        if 'MEMREAD' in self.control_signals:
            self.draw_poly_line(self.MEMREAD_LINE)
            if self.control_signals['MEMREAD'] == 0:    
                self.draw_poly_line(self.ALU_TO_MDR_MUX_LINE, self.DATA_COLOR, True)
            else:                
                self.draw_poly_line(self.MEM_TO_MDR_MUX_LINE, self.DATA_COLOR, True)
                
        if 'MDRLOAD' in self.control_signals:
            self.draw_poly_line(self.MDRLOAD_LINE)
            self.draw_poly_line(self.MUX_TO_MDR_LINE, self.DATA_COLOR, True)

        if 'MDROES2' in self.control_signals:
            self.draw_poly_line(self.MDROES2_LINE)
            self.draw_poly_line(self.MDR_TO_S2_LINE, self.DATA_COLOR, True)
        if 'MEMWRITE' in self.control_signals:
            self.draw_poly_line(self.MEMWRITE_LINE)
            self.draw_poly_line(self.MDR_TO_MEM_LINE, self.DATA_COLOR, True)
        if 'MEMOP' in self.control_signals:
            self.draw_poly_line(self.MEMOP_LINE)
        if 'MEMWAIT' in self.control_signals:
            self.draw_poly_line(self.MEMWAIT_LINE)
        



    def draw_poly_line(self, coords, color='lightgreen',is_data=False):
        prev_coords = None
        for pair in coords:
            if prev_coords == None:
                prev_coords = pair
            else:
                if is_data:                    
                    self.create_line(prev_coords, pair, fill=color, width=3)
                else:
                    self.create_line(prev_coords, pair, fill=color, dash=(10, 10), width=3)
                prev_coords = pair
        pass
        
        

class StateTransitionDiagramView(tk.Canvas):
    INSTR_TITLE_COORDS = [300, 0]
    STATE_STRING = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5']
    STATE_SPACING = 120
    STATE_ZERO_COORDS  = [50, 100]
    STATE_ONE_COORDS   = [STATE_SPACING * 1 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_TWO_COORDS   = [STATE_SPACING * 2 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_THREE_COORDS = [STATE_SPACING * 3 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_FOUR_COORDS  = [STATE_SPACING * 4 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_FIVE_COORDS  = [STATE_SPACING * 5 + STATE_ZERO_COORDS[0], STATE_ZERO_COORDS[1]]
    STATE_COORDS = [STATE_ZERO_COORDS,STATE_ONE_COORDS,STATE_TWO_COORDS,STATE_THREE_COORDS,STATE_FOUR_COORDS,STATE_FIVE_COORDS]

    def __init__(self, parent, controller):
        self.parent = parent
        tk.Canvas.__init__(self, parent, background='#888888')
        self.controller = controller
        self.controller.set_STDDiagramView(self)
        self.bind("<Button-1>", click_handler)
        
        self.ISVs = []
        self.in_quiz_mode = tk.BooleanVar()
        self.draw()

    def load_instruction(self, instr):
        self.ISVs = []
        self.delete(tk.ALL)

        self.create_text(self.INSTR_TITLE_COORDS[0],self.INSTR_TITLE_COORDS[1],text=instr.name, font=tkFont.Font(size=30), anchor=tk.N)
        
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
        
        self.quiz_cb_window = self.create_window(20,20, anchor=tk.SW, window=self.quiz_mode_cb)
        
        for ISV in self.ISVs:
            ISV.draw()

class InputInstructionView(Frame):
    START_COL = 1
    START_ROW = 0
    COLS_PER_TYPE = 4
    INSTR_BUTTON_WIDTH = 1
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
        label0=tk.Label(self, width=100, background="#AAAAAA", text="Select Instruction:")
        label0.grid(row=0, column=0, columnspan=3*self.COLS_PER_TYPE, sticky=tk.N)

        label1=tk.Label(self, background=self.I_BG, text="I-Type")
        label1.grid(row=1, column=0, columnspan=self.COLS_PER_TYPE, sticky=tk.N)
        label2=tk.Label(self, background=self.R_BG, text="R-Type")
        label2.grid(row=1, column= 1 * self.COLS_PER_TYPE, columnspan=self.COLS_PER_TYPE)
        label3=tk.Label(self, background=self.J_BG, text="J-Type")
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

class AppView(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller = Controller()
        
        self.current_instruction = 1
            
        #load DLX image
        self.DLXDPV = DLXDataPathView(self.parent, self.controller)
        self.DLXDPV.grid(row=0, column=0, rowspan=2)

        #Set up inputs
        self.InputInstructionView = InputInstructionView(self.parent, self.controller)
        self.InputInstructionView.grid(row=0, column=1, sticky=tk.N)

        #load STD View
        self.STD_canvas = StateTransitionDiagramView(self.parent, self.controller)
        self.STD_canvas.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W, columnspan=3)

    def draw_handler(self):
        self.STD_canvas.delete(tk.ALL)
        if self.current_instruction is not None:
#            self.STD_canvas.draw_circle()
            
            pass





# make it cover the entire screen
#w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#root.overrideredirect(1)
#root.geometry("%dx%d+0+0" % (w, h))


#root.focus_set() # <-- move focus to this widget
#root.bind("<Escape>", lambda e: e.widget.quit())

root.wm_title("DLX Datapath Learning Simulator")
view = AppView(root)
#app=FullScreenApp(root)
view.parent.configure(background='gray')
root.mainloop()
