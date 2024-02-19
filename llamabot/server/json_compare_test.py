#!/usr/bin/env python
import unittest
import json
from json_compare import compare_json_by_type

class TestCompareJsonByType(unittest.TestCase):

    def test_same_type(self):
        self.assertFalse(compare_json_by_type({"a": 1}, {"b": 2}))

    def test_different_type(self):
        self.assertFalse(compare_json_by_type({"a": 1}, ["a", 2]))

    #def test_nested_same_type(self):
    #    json1 = {"a": {"b": 1}}
    #    json2 = {"c": {"d": 2}}
    #    self.assertTrue(compare_json_by_type(json1, json2))

    def test_nested_different_type(self):
        json1 = {"a": {"b": 1}}
        json2 = {"c": ["d", 2]}
        self.assertFalse(compare_json_by_type(json1, json2))

    def test_empty_objects(self):
        self.assertTrue(compare_json_by_type({}, {}))

    def test_empty_vs_nonempty(self):
        self.assertFalse(compare_json_by_type({}, {"a": 1}))

# This allows running the tests from the command line
if __name__ == '__main__':
    unittest.main()
