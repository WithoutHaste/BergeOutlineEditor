import tkinter
import tkinter.filedialog
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
        self.current_filename = None
        self.init_layout()

    def init_layout(self):
        
        button_frame_top  =  tkinter.Frame(self,  width=200,  height=400)
        button_frame_top.pack(side=tkinter.TOP,  fill=tkinter.X, expand=True,  padx=10)        
        
        label_filename = tkinter.Label(button_frame_top, text="Filename: none")
        label_filename.pack(side=tkinter.TOP, anchor='w', padx=10, pady=5)
        self.label_filename = label_filename
        
        open_button = tkinter.Button(button_frame_top, text="Open File", command=self.client_open_file)
        open_button.pack(side=tkinter.RIGHT, padx=10)

        textbox = tkinter.Text(self, width=90, height=10) #measured in characters
        textbox.pack(side=tkinter.TOP, fill=tkinter.X, expand=True, anchor='w', padx=10)
        textbox.focus_set()
        self.textbox = textbox
        
        button_frame_bottom  =  tkinter.Frame(self,  width=200,  height=400)
        button_frame_bottom.pack(side=tkinter.TOP,  fill=tkinter.X, expand=True,  padx=0)
        
        quitButton = tkinter.Button(button_frame_bottom, text="Quit", command=self.client_quit)
        quitButton.pack(side=tkinter.RIGHT, padx=10)
        
    def update_label_filename(self):
        if self.current_filename == None:
            self.label_filename['text'] = "Filename: None"
        else:
            self.label_filename['text'] = "Filename: " + os.path.basename(self.current_filename)
            
    def client_quit(self):
        exit()
        
    def client_open_file(self):
        filename = tkinter.filedialog.askopenfilename(filetypes=[('Markdown', '*.md')])
        if filename == (): #empty tuple
            filename = None
        self.current_filename = filename
        self.update_label_filename()

		
if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("800x800") #size of window - width x height
    app = Window(root)
    root.mainloop()

