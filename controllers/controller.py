#!/usr/bin/python
import sys
import os
model_lib_path = os.path.abspath('./models/')
sys.path.append(model_lib_path)

import model

class Controller():
    def __init__(self):
        self.InstructionSet = model.InstructionSet()
        self.in_quiz_mode = False
        

    def set_STDDiagramView(self, STDDiagramView):
        self.STDDV = STDDiagramView
 
    def set_DLXDataPathView(self, DLXDataPathView):
        self.DLXDPV = DLXDataPathView
        
    def micro_instruction_state_clicked(self, misv):
        if misv.selected:
            self.DLXDPV.set_control_signals(misv.control_signals)
        else:
            self.DLXDPV.set_control_signals({})

        for instr_state_view in self.STDDV.ISVs:
            if not instr_state_view.instr_state ==misv.instr_state:
                instr_state_view.set_selected(False)

    def instruction_selected(self, instr_name):
        print 'Loading instruction: '  + instr_name 
        #find model
        instr = self.InstructionSet.get_instruction(instr_name)

        #send model to STDDV
        self.STDDV.load_instruction(instr)

        #clear DLXDPV
        self.DLXDPV.clear()

    def get_i_instr(self):
        return self.InstructionSet.i_instrs

    def get_r_instr(self):
        return self.InstructionSet.r_instrs

    def get_j_instr(self):
        return self.InstructionSet.j_instrs
