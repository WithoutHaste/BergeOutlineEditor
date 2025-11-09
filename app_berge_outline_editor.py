import tkinter
import re
import os
import subprocess
import uuid


class Window(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master # this was "root" in the outer code
        self.master.title("Berge Outline Editor") #title displayed on window
        self.pack(fill=tkinter.BOTH, expand=1) #layout of window
        self.init_layout()

    def init_layout(self):
        filename = "temp.md"
        
        label_filename = tkinter.Label(self, text="Filename: " + filename)
        label_filename.pack(side=tkinter.TOP, anchor='w', padx=10, pady=5)
        
        textbox = tkinter.Text(self, width=90, height=10) #measured in characters
        textbox.pack(side=tkinter.TOP, fill=tkinter.X, expand=True, anchor='w', padx=10)
        textbox.focus_set()
        self.textbox = textbox
        
        button_frame_bottom  =  tkinter.Frame(self,  width=200,  height=400)
        button_frame_bottom.pack(side=tkinter.TOP,  fill=tkinter.X, expand=True,  padx=0)
        
        quitButton = tkinter.Button(button_frame_bottom, text="Quit", command=self.client_quit)
        quitButton.pack(side=tkinter.RIGHT, padx=10)
            
    def client_quit(self):
        exit()
		
if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("800x800") #size of window - width x height
    app = Window(root)
    root.mainloop()

