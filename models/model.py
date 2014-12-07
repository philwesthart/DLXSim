#!/usr/bin/python
import json
import sys
import os
sys.path.append(os.path.abspath('.'))
print os.path.abspath('.')
class InstructionSet():
    DATA_FILE = os.path.abspath('./models/json_data.json')
    def __init__(self):
        self.i_instrs = []
        self.j_instrs = []
        self.r_instrs = []
        
        self.instr_set_json = json.loads(open(self.DATA_FILE).read())
        self.instructions = {}
        for instr in self.instr_set_json:
            self.add_instruction(self.instr_set_json[instr])
        
        self.i_instrs = sorted(self.i_instrs)
        self.r_instrs = sorted(self.r_instrs)
        self.j_instrs = sorted(self.j_instrs)
    
    def add_instruction(self, instr):
        name = instr['name']
        print "Adding instruction: " + name
        self.instructions[name] = Instruction(instr)

        if  self.instructions[name].instruction_type == 'I':
            self.i_instrs.append(name)

        if  self.instructions[name].instruction_type == 'R':
            self.r_instrs.append(name)

        if  self.instructions[name].instruction_type == 'J':
            self.j_instrs.append(name)
        

    def get_instruction(self, name):
        return self.instructions[name]

    def to_JSON(self):
        pass


class Instruction():
    def __init__(self, json_instr):
        self.name = json_instr['name']
        self.num_micro_instructions = json_instr['num_micro_instructions']
        self.instruction_type = json_instr['instruction_type']
        self.is_branching = json_instr['is_branching']
        self.micro_instrs = []
        micro_instrs_json = json_instr['MicroInstructionStates']
        for micro_instr in micro_instrs_json :
            self.micro_instrs.append(MicroInstructionState(micro_instrs_json[micro_instr]))

        self.micro_instrs = sorted(self.micro_instrs, key=lambda MicroInstructionState: MicroInstructionState.state_number)
        
    def to_JSON(self):
        pass



class MicroInstructionState():
    def __init__(self, json_micro_instr):
        self.state_string = json_micro_instr['state_string']
        self.state_number = json_micro_instr['state_number']
        self.control_signals = json_micro_instr['control_signals']
        self.has_mem_wait = json_micro_instr['has_mem_wait']
        self.secondary_input = ''
        self.secondary_control_signals = ''

    def to_JSON(self):
        pass

   

if __name__ == '__main__':
    print 'Testing models instruction set'
    IS = InstructionSet()


