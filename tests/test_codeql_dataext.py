
import unittest
from ghastoolkit.codeql.dataextensions.ext import DataExtensions

from ghastoolkit.codeql.dataextensions.models import CompiledSinks


class TestDataExtModels(unittest.TestCase):
    def test_dataext(self):
        de = DataExtensions("python")
        self.assertEqual(de.pack, f"codeql/python-queries")

        
    def test_generation_compiled(self):
        mad = ["java.net", "Socket", True, "Socket", "(String,int)", "", "Argument[0]", "request-forgery", "manual"] 
        model = CompiledSinks(*mad)

        self.assertEqual(model.package, "java.net")
        self.assertEqual(model.object_type, "Socket")
        self.assertEqual(model.subtypes, True)
        self.assertEqual(model.name, "Socket")
        self.assertEqual(model.signature, "(String,int)")
        self.assertEqual(model.ext, "")
        self.assertEqual(model.object_input, "Argument[0]")
        self.assertEqual(model.kind, "request-forgery")
        self.assertEqual(model.provenance, "manual")

        self.assertEqual(model.generate(), mad)

