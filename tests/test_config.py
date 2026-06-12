
import pytest
import os
from src.config import Config

class TestConfigClass:
    def test_import(self):
        config = Config(".env.test")

        assert config.get_value("TEST_KEY") == "TEST_VALUE"
    
    def test_set(self):
        config = Config(".env.test")

        config.set_value("TEST_KEY_2", "TEST_VALUE_2")

        assert config.get_value("TEST_KEY_2") == "TEST_VALUE_2"

    def test_error(self):
        config = Config(".env.test")

        with pytest.raises(KeyError):
            config.get_value("TEST_KEY_2")




