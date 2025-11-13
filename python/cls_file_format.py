import re

class FileFormat():
    MARKER_FINAL = "(final)"
    MARKER_DUPLICATE_SECTION = "# Duplicate: All Final Sections"
    
    # takes in the entire raw text of a file
    # will do its best to parse the file - will keep a list of errors
    def __init__(self, raw_text):
        self.parsing_errors = []
        self.file_root = FileRoot()
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
                if isinstance(current_file_section, FileRoot):
                    current_file_section = None
            if current_file_section == None:
                # new top-level section
                current_file_section = FileSection(self.file_root)
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
        
class FileRoot():
    ID_DELIMITER = "."
    ID_CHARACTERS = ['A','B','C','D','E','F','G','H','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] # skipping I (commonly looks like an L)
    
    def __init__(self):
        self.children = []
        self.level = 0
        
    def append_child(self, child):
        self.children.append(child)
        
    def get_child_id(self, child):
        ith = FileRoot.get_index_of_element(self.children, child)
        return FileRoot.convert_index_to_id(ith)
            
    @staticmethod
    def get_index_of_element(collection, element):
        index = 0
        for c in collection:
            if c == element:
                return index
            index = index + 1
                
    # convert integer to characters
    # A to Z, AA to AZ to ZZ, etc
    @staticmethod
    def convert_index_to_id(index):
        char_count = len(FileRoot.ID_CHARACTERS)
        result = ""
        if index == 0:
            return FileRoot.ID_CHARACTERS[index]
        while index > 0:
            remainder = int(index % char_count)
            result = FileRoot.ID_CHARACTERS[remainder] + result
            index = index - remainder
            index = index / char_count
        return result
        

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
        
    # id is only valid for the current file configuration
    # any adding/removing/reordering of sections can change all the ids
    def get_id(self):
        return self.parent.get_child_id(self)
        
    def get_child_id(self, child):
        prefix = self.get_id()
        ith = FileRoot.get_index_of_element(self.children, child)
        return prefix + FileRoot.ID_DELIMITER + FileRoot.convert_index_to_id(ith)
        
    @staticmethod
    def get_level(line):
        pattern = re.compile('#+', re.IGNORECASE )
        match = pattern.match(line)
        if match == None:
            return 0
        return len(match.group())