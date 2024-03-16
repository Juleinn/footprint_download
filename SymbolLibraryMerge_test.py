import unittest
from SymbolLibraryMerge import *

class TestSymbolLibraryMerge(unittest.TestCase):
    def test_sexp_to_list(self):
        sexp = """(test 1 2 (sub 1 2))"""
        l = sexp_to_list(sexp)
        self.assertEqual(l, ["test", "1", "2", ["sub", "1", "2"]])

    def test_sexp_to_list_parenthesis_in_field(self):
        sexp = """(test 1 2 ("sub(test" 1 2))"""
        l = sexp_to_list(sexp)
        self.assertEqual(l, ['test', '1', '2', ['"sub(test"', '1', '2']])
        
    def test_extract_archive(self):
        files_list = extract_archive('./test_data/archive-demo.zip')
        self.assertNotEqual(files_list[0], "")
        self.assertNotEqual(files_list[1], [])
        self.assertEqual(len(files_list[1]), 1)

    def test_merge_symbol_libraries(self):
        shutil.copy("./test_data/destination_template.kicad_sym","./test_data/destination.kicad_sym")
        merge_symbol_libraries("./test_data/destination.kicad_sym", "./test_data/source_0.kicad_sym")
        merge_symbol_libraries("./test_data/destination.kicad_sym", "./test_data/source_1.kicad_sym")
        self.assertEqual(os.path.getsize("./test_data/target_merged.kicad_sym"), os.path.getsize("./test_data/destination.kicad_sym"))

    def test_update_footprint_field(self):
        start_sexp = """
(kicad_symbol_lib (version 20220914) (generator kicad_symbol_editor)
  (symbol "a_source_chip" (in_bom yes) (on_board yes)
    (property "Footprint" "SOT23-3" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )
)
        """

        target_sexp = """
(kicad_symbol_lib (version 20220914) (generator kicad_symbol_editor)
  (symbol "a_source_chip" (in_bom yes) (on_board yes)
    (property "Footprint" "footprint_download:SOT23-3" (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )
)
        """
        start_data = sexp_to_list(start_sexp) 
        target_data = sexp_to_list(target_sexp) 

        self.assertEqual(update_footprint_field(start_data), target_data) 

if __name__ == "__main__":
    unittest.main()
