from unittest import TestCase, main

from code.strategy_helpers.helpers import remove_prefix_from_keys


class TestCopertHelpers(TestCase):

    def test_remove_prefix_from_keys(self):
        # Test that when a naming conflict exists after the prefix "cold_" is stripped, the value
        # from the key that had the prefix is kept.

        dict = {"value": 5, "cold_value": 10}

        dict_after_processing = remove_prefix_from_keys("cold_", dict)

        self.assertEqual(dict_after_processing, {"value": 10})

    def test_remove_prefix_from_keys_does_not_modify_dict_in_args(self):

        dict = {"value": 5, "cold_value": 10}

        remove_prefix_from_keys("cold_", dict)

        self.assertEqual(dict, {"value": 5, "cold_value": 10})


if __name__ == '__main__':
    main()
