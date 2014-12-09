import Tkinter as tk
import os

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
        
        self.photo = tk.PhotoImage(file=os.path.abspath("./images/DLXCPU.gif"))

        self.control_signals = {}

        self.draw()

    def set_control_signals(self, signals):
        self.control_signals = signals
        self.draw()

    def clear(self):
        self.control_signals = {}
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
        
        
