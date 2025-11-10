import unittest
from cls_file_format import *

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