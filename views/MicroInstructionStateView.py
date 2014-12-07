import Tkinter as tk

class MicroInstructionStateView():
    CIRCLE_WIDTH  = 30
    CIRCLE_HEIGHT = 30
    ARROW_LENGTH = 80
    ARROW_HEAD_LENGTH = 8
    ARROW_HEAD_HEIGHT = 10
    MEM_WAIT_STRING = 'MW = 1/...'
    QUIZ_COORDS = [26,30, 144, 150]
    QUIZ_BOX_COLOR = '#DEAD01'
    ALT_BRANCH_TEXT = 'Branch not taken...'
    
    
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
                self.canvas.create_text(self.x + self.CIRCLE_WIDTH/2, self.y - self.CIRCLE_WIDTH/2, text=self.ALT_BRANCH_TEXT, anchor=tk.SW)

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
        if self.controller.in_quiz_mode:
            self.quiz_box_visible = not self.quiz_box_visible
            self.draw_quiz_box()
        else:
            self.canvas.itemconfig(self.quiz_box, fill='')            
        pass




