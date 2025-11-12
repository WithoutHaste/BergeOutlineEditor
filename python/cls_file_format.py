import re

class FileFormat():
    MARKER_FINAL = "(final)"
    MARKER_DUPLICATE_SECTION = "# Duplicate: All Final Sections"
    
    # takes in the entire raw text of a file
    # will do its best to parse the file - will keep a list of errors
    def __init__(self, raw_text):
        self.parsing_errors = []
        self.file_sections = [] # just the top-level sections
        current_file_section = None
        lines = raw_text.split('\n')
        for line in lines:
            if line.startswith(FileFormat.MARKER_DUPLICATE_SECTION):
                break # ignore entire duplicate section, nothing comes after this
            level = FileSection.get_level(line)
            if level == 0:
                if current_file_section == None:
                     # skip everything before Markdown headers start
                    continue
                # normal line
                current_file_section.append_line(line)
                continue
            while current_file_section != None and level <= current_file_section.level:
                current_file_section = current_file_section.parent
            if current_file_section == None:
                # new top-level section
                current_file_section = FileSection(None)
                self.file_sections.append(current_file_section)
                continue
            if level > current_file_section.level:
                if level > current_file_section.level + 1:
                    self.parsing_errors.append("Header levels skipped a step - this may not be a Berge-formatted file")
                # add new child to parent
                current_file_section = FileSection(current_file_section)
                continue
            self.parsing_errors.append("Should not reach this point - unknown section depth")
        
    def is_valid(self):
        return len(self.parsing_errors) == 0

class FileSection():
    def __init__(self, parent_section):
        self.children = []
        self.lines = []
        self.level = 1
        if parent_section != None:
            self.level = parent_section.level + 1
            parent_section.append_child(self)
        self.parent = parent_section
        pass
        
    def append_line(self, line):
        self.lines.append(line)
        
    def append_child(self, child):
        self.children.append(child)
        
    def get_full_text(self):
        return "\n".join(self.lines).strip()
        
    @staticmethod
    def get_level(line):
        pattern = re.compile('#+', re.IGNORECASE )
        match = pattern.match(line)
        if match == None:
            return 0
        return len(match.group())