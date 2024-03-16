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

    def test_update_footprint_field_with_library(self):
        start_sexp = """
(kicad_symbol_lib (version 20220914) (generator kicad_symbol_editor)
  (symbol "a_source_chip" (in_bom yes) (on_board yes)
    (property "Footprint" "some_lib:SOT23-3" (at 0 0 0)
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

    def test_footprint_has_model(self):
        footprint_with_model = """
(module "some-module" (layer F.Cu)
  (descr "some-module")
  (tags "Accelerometer")
  (attr smd)
  (model KX122-1037.stp
    (at (xyz 0 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
  )
)
            """

        footprint_without_model = """
(module "some-module" (layer F.Cu)
  (descr "some-module")
  (tags "Accelerometer")
  (attr smd)
)
            """
        footprint_with_model_data = sexp_to_list(footprint_with_model)
        footprint_without_model_data = sexp_to_list(footprint_without_model)
        self.assertTrue(has_3dmodel(footprint_with_model_data))
        self.assertFalse(has_3dmodel(footprint_without_model_data))

    def test_update_3dmodel(self):
        footprint_sexp = """
(module "some-module" (layer F.Cu)
  (tags "Accelerometer")
)
        """
        footprint_data = sexp_to_list(footprint_sexp)
        footprint_data = update_3dmodel(footprint_data, "test-model.stp")

        target_sexp = """
(module "some-module" (layer F.Cu)
  (tags "Accelerometer")
  (model test-model.stp
    (at (xyz 0 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
  )
)
        """
        target_data = sexp_to_list(target_sexp)
        self.assertEqual(target_data, footprint_data)

    def test_update_3dmodel_inplace(self):
        shutil.copy('./test_data/footprint-nomodel.kicad_mod', './test_data/footprint-model.kicad_mod')
        update_3dmodel_inplace('./test_data/footprint-model.kicad_mod', 'test.stp')
        size = os.path.getsize('./test_data/footprint-model.kicad_mod')
        # doing it again should do nothing
        update_3dmodel_inplace('./test_data/footprint-model.kicad_mod', 'test.stp')
        self.assertEqual(size, os.path.getsize('./test_data/footprint-model.kicad_mod'))


if __name__ == "__main__":
    unittest.main()
