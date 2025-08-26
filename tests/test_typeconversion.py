"""Test type conversion functionality in RestRequest."""

import unittest
from dataclasses import dataclass
from typing import List, Union, Optional

from ghastoolkit.octokit.octokit import RestRequest, OctoItem, loadOctoItem


# Define test classes
@dataclass
class TestItem(OctoItem):
    """Test OctoItem class for testing type conversion."""
    id: int
    name: str
    active: bool = True


@dataclass
class TestNestedItem(OctoItem):
    """Test OctoItem with nested structure for testing complex type conversion."""
    id: int
    details: Optional[dict] = None


class TestTypeConversion(unittest.TestCase):
    """Test case for type conversion functionality in RestRequest."""

    def test_convert_dict_to_octoitem(self):
        """Test converting a dictionary to an OctoItem."""
        data = {"id": 123, "name": "test item", "active": True}
        
        result = RestRequest.convert_to_return_type(data, TestItem)
        
        self.assertIsInstance(result, TestItem)
        self.assertEqual(result.id, 123)
        self.assertEqual(result.name, "test item")
        self.assertEqual(result.active, True)

    def test_convert_list_to_octoitems(self):
        """Test converting a list of dictionaries to a list of OctoItems."""
        data = [
            {"id": 1, "name": "item 1"},
            {"id": 2, "name": "item 2"},
            {"id": 3, "name": "item 3", "active": False},
        ]
        
        result = RestRequest.convert_to_return_type(data, List[TestItem])
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], TestItem)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[1].name, "item 2")
        self.assertEqual(result[2].active, False)
        # First two items should have default value for active
        self.assertEqual(result[0].active, True)

    def test_convert_list_manual_method(self):
        """Test using the explicit convert_list_to_octoitems method."""
        data = [
            {"id": 1, "name": "item 1"},
            {"id": 2, "name": "item 2"},
        ]
        
        result = RestRequest.convert_list_to_octoitems(data, TestItem)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], TestItem)
        self.assertEqual(result[0].id, 1)
        self.assertEqual(result[1].name, "item 2")

    def test_convert_with_extra_data(self):
        """Test conversion when extra data is present in the dictionary."""
        data = {
            "id": 42, 
            "name": "test", 
            "extra_field": "extra value",
            "another_field": 123
        }
        
        result = RestRequest.convert_to_return_type(data, TestItem)
        
        self.assertIsInstance(result, TestItem)
        self.assertEqual(result.id, 42)
        self.assertEqual(result.name, "test")
        # Extra data should be available via __data__
        self.assertEqual(result.extra_field, "extra value")
        self.assertEqual(result.another_field, 123)

    def test_convert_nested_structure(self):
        """Test conversion with nested structure."""
        data = {
            "id": 99,
            "details": {
                "created_at": "2025-01-01",
                "status": "active"
            }
        }
        
        result = RestRequest.convert_to_return_type(data, TestNestedItem)
        
        self.assertIsInstance(result, TestNestedItem)
        self.assertEqual(result.id, 99)
        self.assertIsInstance(result.details, dict)
        self.assertEqual(result.details["status"], "active")

    def test_convert_union_type(self):
        """Test that Union types are ignored."""
        data = {"id": 123, "name": "test item"}
        
        result = RestRequest.convert_to_return_type(data, Union[TestItem, dict])
        
        self.assertIsNone(result)  # Union types are ignored, should return None

    def test_convert_invalid_input(self):
        """Test conversion with invalid input."""
        # List when expecting a dict
        result = RestRequest.convert_to_return_type([1, 2, 3], TestItem)
        self.assertIsNone(result)
        
        # Dict missing required fields when expecting a list of TestItems
        result = RestRequest.convert_to_return_type({"key": "value"}, List[TestItem])
        self.assertIsNone(result)
        
        # Invalid data types
        result = RestRequest.convert_to_return_type(None, TestItem)
        self.assertIsNone(result)
        
        result = RestRequest.convert_to_return_type("string", List[TestItem])
        self.assertIsNone(result)

    def test_convert_list_to_octoitems_invalid(self):
        """Test convert_list_to_octoitems with invalid inputs."""
        # Not a list
        result = RestRequest.convert_list_to_octoitems({"not": "a list"}, TestItem)
        self.assertEqual(result, {"not": "a list"})
        
        # Not an OctoItem subclass
        result = RestRequest.convert_list_to_octoitems([1, 2, 3], dict)
        self.assertEqual(result, [1, 2, 3])
        
    def test_convert_single_dict_to_list(self):
        """Test converting a single dict to a list of OctoItems when list type is expected."""
        data = {"id": 42, "name": "single item"}
        
        result = RestRequest.convert_to_return_type(data, List[TestItem])
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], TestItem)
        self.assertEqual(result[0].id, 42)
        self.assertEqual(result[0].name, "single item")
        
    def test_convert_list_when_single_expected(self):
        """Test converting a list to a single OctoItem type."""
        data = [
            {"id": 99, "name": "first item"},
            {"id": 100, "name": "second item"}
        ]
        
        result = RestRequest.convert_to_return_type(data, TestItem)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], TestItem)
        self.assertEqual(result[0].id, 99)
        self.assertEqual(result[1].name, "second item")


if __name__ == "__main__":
    unittest.main()
