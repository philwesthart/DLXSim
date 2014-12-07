import Tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width=400,  height=400, 
                                background="bisque")
        self.canvas.pack(fill="both", expand=True)

        graphic1 = GraphicObject(10,10,100,100, name="graphic1")
        graphic2 = GraphicObject(110,110,200,200, name="graphic2")

        graphic1.draw(self.canvas)
        graphic2.draw(self.canvas)

class GraphicObject(object):
    def __init__(self, x0,y0,x1,y1, name=None):
        self.coords = (x0,y0,x1,y1)
        self.name = name
	self.color = "white"

    def draw(self, canvas, outline="black", fill="white"):
    	self.canvas = canvas
        item = self.canvas.create_oval(self.coords, outline=outline, fill=self.color)
        self.canvas.tag_bind(item, "<1>", self.mouse_click)

    def mouse_click(self, event):
        print "I got a mouse click (%s)" % self.name
	if self.color == "white":
	   self.color = "red"
	   print "toggle"
	else:
		self.color="white"
	   	print "toggled"
	self.draw(self.canvas)

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()