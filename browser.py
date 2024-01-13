import tkinter
from url_request import URL

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100

def lex(body):
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text+=c
    return text

def layout(text):
    display_text = []
    cursor_x,cursor_y = HSTEP,VSTEP
    for c in text:
        display_text.append((cursor_x,cursor_y,c))
        cursor_x+=HSTEP
        if cursor_x>= WIDTH-HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_text
        
    
class BrowserViewer():
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll = 0
        self.window.bind("<Down>",self.scroll_down)
    
    def scroll_down(self, e):
        self.scroll +=SCROLL_STEP
        self.draw()
        
    def load(self,url):
        # self.canvas.create_rectangle(10,20,400,300)
        # self.canvas.create_oval(100,100,150,150)
        # self.canvas.create_text(200,150, text="Hola")
        body = url.request()
        text = lex(body)
        self.display_list = layout(text)
        self.draw()
        
    def draw(self):
        self.canvas.delete("all")
        for x,y,t in self.display_list:
            if y>self.scroll + HEIGHT:continue
            if y + VSTEP < self.scroll:continue
            self.canvas.create_text(x,y-self.scroll,text=t)
        

if __name__=="__main__":
    import sys
    BrowserViewer().load(URL(sys.argv[1]))
    tkinter.mainloop()

