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
        # gui organization
        # section_frame contains everything related to the file sections
        # within that, primary interest is the children of sections are vertically aligned with each other
        # therefore, each top-level section will init its own horizontally-stretched frame, holding it and its children
        # textbox width will be hard-coded so that they appear to display in columns, one per "level"
        # the GUI will be able to handle more than 3 levels, but default display will expect only 3 levels
        
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
        self.current_data = FileFormat(text)
        if not self.current_data.is_valid():
            print("Error: File format is invalid") # TODO display the errors, and display error where user will notice it
        self.update_label_filename()
        self.update_section_frame()
        
    def update_section_frame(self):
        Window.remove_children(self.section_frame)
        tab_order = 0
        for file_section in self.current_data.file_root.children:
            frame = self.build_frame_for_file_section(self.section_frame, file_section, tab_order)
            tab_order = tab_order + 1
        self.focus_section_id = None # clear instruction

    # recursively builds nested frames for children sections  
    def build_frame_for_file_section(self, parent_widget, file_section, tab_order):
        frame  =  tkinter.Frame(parent_widget,  width=200,  height=400)
        frame.pack(side=tkinter.TOP,  fill=tkinter.X, expand=True,  padx=5)        
        textbox_width = self.get_textbox_width(file_section.level)
        textbox_height = self.get_textbox_height(file_section.level)
        textbox = tkinter.Text(frame, width=textbox_width, height=textbox_height) #measured in characters
        textbox.file_section_id = file_section.get_id()
        textbox.tab_order = tab_order
        textbox.insert(tkinter.END, file_section.get_full_text())
        textbox.pack(side=tkinter.LEFT, fill=tkinter.NONE, expand=False, anchor='n', padx=5)
        textbox.bind('<Alt-Return>', self.section_alt_plus_return)
        textbox.bind('<Alt-Down>', self.section_alt_plus_down)
        textbox.bind('<Alt-Up>', self.section_alt_plus_up)
        if hasattr(self, 'focus_section_id') and self.focus_section_id == file_section.get_id():
            textbox.focus_set()
        if len(file_section.children) > 0:
            children_frame  =  tkinter.Frame(frame,  width=200,  height=400)
            children_frame.pack(side=tkinter.LEFT,  fill=tkinter.BOTH, expand=True,  padx=5)        
            for child_section in file_section.children:
                frame = self.build_frame_for_file_section(children_frame, child_section, tab_order)

    # width is in characters, and is based on a 1500px wide window
    def get_textbox_width(self, level):
        if level == 1:
            return 30
        if level == 2:
            return 45
        return 70

    def get_textbox_height(self, level):
        if level == 1:
            return 3
        if level == 2:
            return 8
        return 16
        
    # recursive, returns True when the right textbox is located
    def focus_based_on_tab_order(self, tab_order, frame=None):
        if frame == None:
            return self.focus_based_on_tab_order(tab_order, self.section_frame)
        for widget in frame.winfo_children():
            if isinstance(widget, tkinter.Frame):
                # dig down for the textboxes within the nested frames
                success = self.focus_based_on_tab_order(tab_order, widget)
                if success:
                    return True
            elif hasattr(widget, 'tab_order') and widget.tab_order == tab_order:
                widget.focus_set()
                if isinstance(widget, tkinter.Text):
                    # put cursor at start of text
                    widget.mark_set("insert", "0.0")
                return True
        return False

    def section_alt_plus_return(self, event):
        # insert new section sibling after this one
        new_section_id = self.current_data.file_root.add_sibling_after(event.widget.file_section_id)
        # redraw all
        self.focus_section_id = new_section_id
        self.update_section_frame()
        return 'break'

    def section_alt_plus_down(self, event):
        # change focus to next section
        self.focus_based_on_tab_order(event.widget.tab_order + 1)
        return 'break'

    def section_alt_plus_up(self, event):
        # change focus to previous section
        self.focus_based_on_tab_order(event.widget.tab_order - 1)
        return 'break'

    @staticmethod
    def remove_children(element):
        for child in element.winfo_children():
            child.destroy()

		
if __name__ == "__main__":
    root = tkinter.Tk()
    root.geometry("1500x800") #size of window - width x height
    app = Window(root)
    root.mainloop()

