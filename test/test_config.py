"""
Test the configuration files
"""

from io import config


def test_load_files():
    config_output = config.import_yaml_files(".", ["dbconfig.yaml", "countries.yaml", "access.yaml"])
    assert config_output != []
