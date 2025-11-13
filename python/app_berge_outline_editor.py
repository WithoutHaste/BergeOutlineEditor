import tkinter
import tkinter.filedialog
import re
import os
import subprocess
import uuid
from cls_file_format import FileFormat


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
        
        open_button = tkinter.Button(button_frame_top, text="Open File", command=self.client_select_file)
        open_button.pack(side=tkinter.RIGHT, padx=10)

        section_frame  =  tkinter.Frame(self,  width=200,  height=400)
        section_frame.pack(side=tkinter.TOP,  fill=tkinter.BOTH, expand=True,  padx=10)        
        self.section_frame = section_frame
        
        button_frame_bottom  =  tkinter.Frame(self,  width=200,  height=400)
        button_frame_bottom.pack(side=tkinter.TOP,  fill=tkinter.X, expand=True,  padx=0)
        
        quitButton = tkinter.Button(button_frame_bottom, text="Quit", command=self.client_quit)
        quitButton.pack(side=tkinter.RIGHT, padx=10)
            
    def client_quit(self):
        exit()
        
    def client_select_file(self):
        filename = tkinter.filedialog.askopenfilename(filetypes=[('Markdown', '*.md')])
        if filename == (): #empty tuple
            filename = None
        if filename == None:
            return
        self.current_filename = filename
        self.load_file()
        
    def update_label_filename(self):
        if self.current_filename == None:
            self.label_filename['text'] = "Filename: None"
        else:
            self.label_filename['text'] = "Filename: " + os.path.basename(self.current_filename)

    def load_file(self):
        if self.current_filename == None:
            print("Error: No file selected")
            return
        f = open(self.current_filename, "r")
        text = f.read()
        f.close()
        self.file_format = FileFormat(text)
        if not self.file_format.is_valid():
            print("Error: File format is invalid") # TODO display the errors, and display error where user will notice it
        self.update_label_filename()
        self.update_section_frame()
        
    def update_section_frame(self):
        Window.remove_children(self.section_frame)
        for file_section in self.file_format.file_sections:
            textbox = tkinter.Text(self.section_frame, width=90, height=4) #measured in characters
            textbox.insert(tkinter.END, file_section.get_full_text())
            textbox.pack(side=tkinter.TOP, fill=tkinter.X, expand=True, anchor='w', padx=10)
            textbox.bind('<Shift-Return>', self.section_shift_plus_return)
            textbox.bind('<Shift-Down>', self.section_shift_plus_down)
        # MAYBE NEED the short answer is this: when you destroy all the children widgets, pack no longer thinks it "owns" the window since there are no children to manage. Because of that, it doesn't try to resize the window. A simple work-around is to pack a tiny 1x1 frame in the window temporarily, to cause pack to resize the containing frame.

    def section_shift_plus_return(self, event):
        print("shift-enter")
        print(event.widget.get("1.0", "end"))
        # TODO insert new section below here
        # figure out which file_section this widget corresponds to
        # update self.file_format (which needs a new name) - tell it to insert a new file_section at the right point
        # then redo the whole display of the file
        # return focus to the correct widget - the newly added one

    def section_shift_plus_down(self, event):
        print("shift-down")
        # TODO change focus to section below here

    @staticmethod
    def remove_children(element):
        for child in element.winfo_children():
            child.destroy()

		
if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("800x800") #size of window - width x height
    app = Window(root)
    root.mainloop()

