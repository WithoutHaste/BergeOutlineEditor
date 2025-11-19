import tkinter
import tkinter.filedialog
import re
import os
import subprocess
import uuid
from cls_file_format import FileFormat, FileRoot


class ScrollCanvas():
    # initializes a vertical-scrolling canvas
    # add widgets to the canvas to include them in the scrollable space
    def __init__(self, parent_widget):
        frame  =  tkinter.Frame(parent_widget,  width=1500,  height=600)
        frame.pack(side=tkinter.TOP,  fill=tkinter.BOTH, expand=True)

        canvas = tkinter.Canvas(frame,  width=1480,  height=600)
        canvas.pack(side=tkinter.LEFT)
        scrollbar = tkinter.Scrollbar(frame, command=canvas.yview)
        scrollbar.pack(side=tkinter.LEFT, fill=tkinter.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', self.on_configure)
        #canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        canvas.bind_all("<Button-4>", self.on_mousewheel_down)
        canvas.bind_all("<Button-5>", self.on_mousewheel_up)
        self.canvas = canvas
        
    def on_configure(self, event):
        # update scrollregion after starting 'mainloop', when all widgets are in canvas
        # you want the scrollregion to exactly match the total size of what is inside the frame
        event.widget.configure(scrollregion=event.widget.bbox('all'))

    def update_scrollregion(self, height):
        bbox = (0, 0, 1480, height)
        self.scrolling_height = height
        self.canvas.configure(scrollregion=bbox)

    """        
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        # divide-by-120 is needed on Windows, it is not needed on Mac
    """
        
    def on_mousewheel_up(self, event):
        self.canvas.yview_scroll(int(1), "units")
        
    def on_mousewheel_down(self, event):
        self.canvas.yview_scroll(int(-1), "units")
        
    # You may need to call .update() on your tkinter instance before calling the jump function, otherwise the winfo values may be incorrect.
    def scroll_to_y(self, y):
        y = y - 125 # messy - taking out top of window
        print(y)
        self.canvas.yview_moveto(y / self.scrolling_height) # value 0 to 1


class TabOrder():
    # tab_order is used to control up/down movement
    # tab_order is breath-first, while display order is depth-first
    # this class keeps track of what the current tab_order for each column(level) is
    def __init__(self):
        # index = level
        # levels start at 1, so initializing with a dummy value at 0
        self.tab_order_per_level = [0]
        
    def get_tab_order(self, level):
        while len(self.tab_order_per_level) <= level:
            self.tab_order_per_level.append(0)
        self.tab_order_per_level[level] = self.tab_order_per_level[level] + 1
        return self.tab_order_per_level[level]


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

        new_button = tkinter.Button(button_frame_top, text="New File", command=self.client_new_file)
        new_button.pack(side=tkinter.RIGHT, padx=40)

        scroll_canvas = ScrollCanvas(self)
        self.scroll_canvas = scroll_canvas

        section_frame  =  tkinter.Frame(scroll_canvas.canvas,  width=200,  height=400)
        ###section_frame.pack(side=tkinter.TOP,  fill=tkinter.BOTH, expand=True,  padx=10)        
        scroll_canvas.canvas.create_window((0,0), window=section_frame, anchor='nw')
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
        
    def client_new_file(self):
        self.current_filename = None
        self.current_data = FileFormat("# A\n")
        self.focus_section_id = "A"
        self.update_label_filename()
        self.update_section_frame()
        
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
        tab_order_control = TabOrder()
        max_height = 0
        for file_section in self.current_data.file_root.children:
            sub_height = self.build_frame_for_file_section(self.section_frame, file_section, tab_order_control)
            max_height = sub_height + max_height
        self.scroll_canvas.update_scrollregion(max_height)
        self.focus_section_id = None # clear instruction

    # recursively builds nested frames for children sections  
    # initializes focus on currently selected section
    # returns max-height of this subtree of textboxes
    def build_frame_for_file_section(self, parent_widget, file_section, tab_order_control):
        max_height = 0
        frame  =  tkinter.Frame(parent_widget,  width=200,  height=400)
        frame.pack(side=tkinter.TOP,  fill=tkinter.X, expand=True,  padx=2) 
        textbox_width = self.get_textbox_width(file_section.level)
        textbox_height = self.get_textbox_height(file_section.level)
        max_height = textbox_height * 22 # converting char height to px height, roughly
        textbox = tkinter.Text(frame, width=textbox_width, height=textbox_height) #measured in characters
        textbox.file_section_id = file_section.get_id()
        textbox.tab_order = tab_order_control.get_tab_order(file_section.level)
        textbox.column = file_section.level
        textbox.insert(tkinter.END, file_section.get_full_text())
        textbox.pack(side=tkinter.LEFT, fill=tkinter.NONE, expand=False, anchor='n', padx=2)
        textbox.bind('<Alt-Return>', self.section_alt_plus_return)
        textbox.bind('<Alt-m>', self.section_alt_plus_m)
        textbox.bind('<Alt-Down>', self.section_alt_plus_down)
        textbox.bind('<Alt-Up>', self.section_alt_plus_up)
        textbox.bind('<Alt-Left>', self.section_alt_plus_left)
        textbox.bind('<Alt-Right>', self.section_alt_plus_right)
        if hasattr(self, 'focus_section_id') and self.focus_section_id == file_section.get_id():
            textbox.focus_set()
        children_height = 0
        if len(file_section.children) > 0:
            children_frame  =  tkinter.Frame(frame,  width=200,  height=400)
            children_frame.pack(side=tkinter.LEFT,  fill=tkinter.BOTH, expand=True,  padx=2)
            for child_section in file_section.children:
                child_height = self.build_frame_for_file_section(children_frame, child_section, tab_order_control)
                children_height = children_height + child_height
        if children_height > max_height:
            max_height = children_height
        return max_height

    # width is in characters, and is based on a 1500px wide window
    def get_textbox_width(self, level):
        if level == 1:
            return 30
        if level == 2:
            return 45
        return 68

    def get_textbox_height(self, level):
        if level == 1:
            return 3
        if level == 2:
            return 8
        return 16
        
    # recursive, returns True when the right textbox is located
    def focus_based_on_tab_order(self, tab_order, column, frame=None):
        if frame == None:
            return self.focus_based_on_tab_order(tab_order, column, self.section_frame)
        for widget in frame.winfo_children():
            if isinstance(widget, tkinter.Frame):
                # dig down for the textboxes within the nested frames
                success = self.focus_based_on_tab_order(tab_order, column, widget)
                if success:
                    return True
            elif hasattr(widget, 'tab_order') and widget.tab_order == tab_order and widget.column == column:
                widget.focus_set()
                if isinstance(widget, tkinter.Text):
                    # put cursor at start of text
                    widget.mark_set("insert", "0.0")
                self.scroll_canvas.scroll_to_y(widget.winfo_rooty())
                return True
        return False
        
    # recursive, returns True when the right textbox is located
    def focus_based_on_id(self, section_id, frame=None):
        if frame == None:
            return self.focus_based_on_id(section_id, self.section_frame)
        for widget in frame.winfo_children():
            if isinstance(widget, tkinter.Frame):
                # dig down for the textboxes within the nested frames
                success = self.focus_based_on_id(section_id, widget)
                if success:
                    return True
            elif hasattr(widget, 'file_section_id') and widget.file_section_id == section_id:
                widget.focus_set()
                if isinstance(widget, tkinter.Text):
                    # put cursor at start of text
                    widget.mark_set("insert", "0.0")
                self.scroll_canvas.scroll_to_y(widget.winfo_rooty())
                return True
        return False

    def section_alt_plus_return(self, event):
        # insert new section sibling after this one
        new_section_id = self.current_data.file_root.add_sibling_after(event.widget.file_section_id)
        # redraw all
        self.focus_section_id = new_section_id
        self.update_section_frame()
        return 'break'

    def section_alt_plus_m(self, event):
        # insert first child of current section, if there are none
        new_section_id = self.current_data.file_root.add_first_child(event.widget.file_section_id)
        if new_section_id == None:
            return
        # redraw all
        self.focus_section_id = new_section_id
        self.update_section_frame()
        return 'break'

    def section_alt_plus_down(self, event):
        # change focus to next section
        self.focus_based_on_tab_order(event.widget.tab_order + 1, event.widget.column)
        return 'break'

    def section_alt_plus_up(self, event):
        # change focus to previous section
        self.focus_based_on_tab_order(event.widget.tab_order - 1, event.widget.column)
        return 'break'

    def section_alt_plus_left(self, event):
        # change focus to parent section
        id_segments = event.widget.file_section_id.split(FileRoot.ID_DELIMITER)
        id_segments.pop()
        parent_id = FileRoot.ID_DELIMITER.join(id_segments)
        self.focus_based_on_id(parent_id)
        return 'break'

    def section_alt_plus_right(self, event):
        # change focus to first child section
        first_child_id = event.widget.file_section_id + FileRoot.ID_DELIMITER + FileRoot.ID_CHARACTERS[0]
        self.focus_based_on_id(first_child_id)
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

