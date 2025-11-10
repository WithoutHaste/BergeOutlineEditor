import re

class FileFormat():
    MARKER_FINAL = "(final)"
    MARKER_DUPLICATE_SECTION = "# Duplicate: All Final Sections"
    
    # takes in the entire raw text of a file
    # will do its best to parse the file - will keep a list of errors
    def __init__(self, raw_text):
        self.parsing_errors = []
        self.file_sections = []
        lines = raw_text.split('\n')
        for line in lines:
            if line.startswith(MARKER_DUPLICATE_SECTION):
                break # ignore entire duplicate section, nothing comes after this
            level = FIleSection.get_level(line)
            current_level = len(self.file_sections)
            if level == 0 and current_level == 0:
                continue # skip everything before Markdown headers start
            if level == 0:
                self.file_sections[-1].append(line) # normal line
                continue
            if level == current_level:
                # TODO - new section attached to parent
                continue
            if level > current_level:
                # TODO append new child section
                continue
            if level < current_level:
                # TODO pop up to correct parent level before adding new section
                continue
            self.parsing_errors.append("Should not reach this point - unknown section depth")
        
    def is_valid(self):
        return len(self.parsing_errors) == 0

class FileSection():
    def __init__(self, first_line):
        self.lines = []
        pass
        
    def append_line(self, line):
        self.lines.append(line)
        
    @staticmethod
    def get_level(line):
        pattern = re.compile('#+', re.IGNORECASE )
        match = pattern.match(line)
        if match == None:
            return 0
        return len(match.group())