#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import date
import unittest

from invoicegenerator.config import ConfigStore

class TestDateSorting(unittest.TestCase):
    "Test sorting and retrieval of complete dates"

    def setUp(self):
        self.lines = \
            ["[bar]", "valid_from='06.01.1980'", "data='bar'",
             "[doe]", "valid_from='11.01.1980'", "data='doe'", 
             "[foo]", "valid_from='01.01.1980'", "data='foo'", ]
        ConfigStore.read_configuration(self.lines)

    def tearDown(self):
        ConfigStore.reset()

    def test_getconfig(self):
        """Test that the newest configuration is returned if no date was 
        specified."""
        config = ConfigStore.get_configuration()
        self.assertEqual("doe", config["data"])
        
    def test_datesorting(self):
        "Test that the read sections are ordered by date."
        data = ["foo", "bar", "doe"]
        for i, config in enumerate(ConfigStore.get_configurations()):
            self.assertEqual(data[i], config["data"])
    
    def test_get_by_date(self):
        "Test that configurations can be retrieved by data"
        data = [("foo", 1), ("foo", 2), ("foo", 5), 
                ("bar", 7), 
                ("doe", 20), ("doe", 28), ]
        for data_string, day in data:
            some_date = date(year=1980, month=1, day=day)
            config = ConfigStore.get_configuration(when=some_date)
            self.assertEqual(data_string, config["data"])


class TestRangeIncomplete(unittest.TestCase):
    """Test that sorting/retrieval works even if the 'valid from' field is 
    missing."""

    def setUp(self):
        self.lines = \
            ["[bar]", "data='bar'",
             "[foo]", "valid_from='10.01.1980'", "data='foo'", ]
        ConfigStore.read_configuration(self.lines)

    def tearDown(self):
        ConfigStore.reset()

    def test_get_by_date(self):
        """Test that a configuration without valid_from is being considered 
        valid from 0 to the next configuration with this field."""
        data = [("bar", 1), ("foo", 10), ]
        for data_string, day in data:
            some_date = date(year=1980, month=1, day=day)
            config = ConfigStore.get_configuration(when=some_date)
            self.assertEqual(data_string, config["data"])

            
class TestInheritance(unittest.TestCase):
    """Test that values are retrieved from earlier configurations if they are 
    not present in the current one."""

    def setUp(self):
        self.lines = \
            ["[bar]", "valid_from='06.01.1980'", "data='bar'", "bardata='abc'",
             "[foo]", "valid_from='01.01.1980'", "data='foo'", "data2='doe'", ]
        ConfigStore.read_configuration(self.lines)

    def tearDown(self):
        ConfigStore.reset()

    def test_inherit(self):
        """Test that values are inherited from older configurations if the 
        requested field is not present in the current configuration."""
        config = ConfigStore.get_configuration()
        self.assertEqual("bar", config["data"])
        self.assertEqual("doe", config["data2"])

    def test_inherit_not_present(self):
        """Test that values which are not present in any configuration will
        cause a KeyError as normal."""
        config = ConfigStore.get_configuration()
        try:
            config["doesnotexist"]
            self.fail("Invalid key did not raise a KeyError")
        except KeyError, e:
            print e

if __name__ == "__main__":
    unittest.main()

