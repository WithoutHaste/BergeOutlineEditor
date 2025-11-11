import unittest
from cls_file_format import *

class Test_FileFormat(unittest.TestCase):
    def test_init(self):
        # no headers
        result = FileFormat("abc\ndef")
        self.assertEqual(len(result.file_sections), 0)
        self.assertEqual(len(result.parsing_errors), 0)
        # one header
        result = FileFormat("abc\ndef\n# A\nghi")
        self.assertEqual(len(result.file_sections), 1)
        self.assertEqual(result.file_sections[0].lines, ['ghi'])
        self.assertEqual(len(result.parsing_errors), 0)
        # one set of nested headers
        result = FileFormat("# A\nabc\n## A.A\ndef\n### A.A.A\nghi")
        self.assertEqual(len(result.file_sections), 1)
        self.assertEqual(result.file_sections[0].lines, ['abc'])
        self.assertEqual(len(result.file_sections[0].children), 1)
        self.assertEqual(result.file_sections[0].children[0].lines, ['def'])
        self.assertEqual(len(result.file_sections[0].children[0].children), 1)
        self.assertEqual(result.file_sections[0].children[0].children[0].lines, ['ghi'])
        self.assertEqual(len(result.file_sections[0].children[0].children[0].children), 0)
        self.assertEqual(len(result.parsing_errors), 0)
        # multiple sets of nested headers
        result = FileFormat("# A\nabc\n## A.A\ndef\n# B\nghi\n## B.A\njkl")
        self.assertEqual(len(result.file_sections), 2)
        self.assertEqual(result.file_sections[0].lines, ['abc'])
        self.assertEqual(len(result.file_sections[0].children), 1)
        self.assertEqual(result.file_sections[0].children[0].lines, ['def'])
        self.assertEqual(len(result.file_sections[0].children[0].children), 0)
        self.assertEqual(result.file_sections[1].lines, ['ghi'])
        self.assertEqual(len(result.file_sections[1].children), 1)
        self.assertEqual(result.file_sections[1].children[0].lines, ['jkl'])
        self.assertEqual(len(result.file_sections[1].children[0].children), 0)
        self.assertEqual(len(result.parsing_errors), 0)
        # jump back multiple levels AND add multiple children
        result = FileFormat("# A\nabc\n## A.A\ndef\n### A.A.A\nghi\n#### A.A.A.A\njkl\n## A.B\nmno")
        self.assertEqual(len(result.file_sections), 1)
        self.assertEqual(result.file_sections[0].lines, ['abc'])
        self.assertEqual(len(result.file_sections[0].children), 2)
        self.assertEqual(result.file_sections[0].children[0].lines, ['def'])
        self.assertEqual(len(result.file_sections[0].children[0].children), 1)
        self.assertEqual(result.file_sections[0].children[0].children[0].lines, ['ghi'])
        self.assertEqual(len(result.file_sections[0].children[0].children), 1)
        self.assertEqual(result.file_sections[0].children[0].children[0].children[0].lines, ['jkl'])
        self.assertEqual(len(result.file_sections[0].children[0].children[0].children[0].children), 0)
        self.assertEqual(result.file_sections[0].children[1].lines, ['mno'])
        self.assertEqual(len(result.file_sections[0].children[1].children), 0)
        self.assertEqual(len(result.parsing_errors), 0)
        # warns about skipped levels
        result = FileFormat("# A\nabc\n### A.A.A\ndef")
        self.assertEqual(len(result.file_sections), 1)
        self.assertEqual(result.file_sections[0].lines, ['abc'])
        self.assertEqual(len(result.file_sections[0].children), 1)
        self.assertEqual(result.file_sections[0].children[0].lines, ['def'])
        self.assertEqual(len(result.file_sections[0].children[0].children), 0)
        self.assertEqual(len(result.parsing_errors), 1)
        # ignore everything after duplicate section
        result = FileFormat("# A\nabc\n# Duplicate: All Final Sections\ndef\n## A.A\nghi")
        self.assertEqual(len(result.file_sections), 1)
        self.assertEqual(result.file_sections[0].lines, ['abc'])
        self.assertEqual(len(result.file_sections[0].children), 0)
        self.assertEqual(len(result.parsing_errors), 0)
        

class Test_FileSection(unittest.TestCase):
    def test_get_level(self):
        self.assertEqual(FileSection.get_level("abcdefg"), 0)
        self.assertEqual(FileSection.get_level(" # abc"), 0)
        self.assertEqual(FileSection.get_level("# abc"), 1)
        self.assertEqual(FileSection.get_level("#abc"), 1)
        self.assertEqual(FileSection.get_level("## abc"), 2)
        self.assertEqual(FileSection.get_level("##abc"), 2)
        self.assertEqual(FileSection.get_level("### abc"), 3)
        self.assertEqual(FileSection.get_level("###abc"), 3)
        self.assertEqual(FileSection.get_level("#### abc #"), 4)
        self.assertEqual(FileSection.get_level("####abc##"), 4)

if __name__ == "__main__":
    unittest.main()