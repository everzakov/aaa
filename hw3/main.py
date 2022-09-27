import json
import keyword
from typing import Dict, Any
import unittest


class TitleIsNotPresentedException(Exception):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class Objectizer:
    def __init__(self, values: Dict[str, Any]):
        """Initialize Objectizer from JSON objects (get keys and make them as attributes)"""
        for key, value in values.items():
            dict_key = key
            if keyword.iskeyword(key):
                dict_key += "_"
            if isinstance(value, dict):
                self.__dict__[dict_key] = Objectizer(value)
            else:
                self.__dict__[dict_key] = value

    def __getattr__(self, item: str):
        return self.__dict__.get(item)

    def __setattr__(self, key: str, value: Any):
        self.__dict__[key] = value


class ColorizeMixin:
    repr_color_code = 32
    repr_background_color_code = 40

    def __repr__(self):
        """Add color to repr func"""
        return f'\033[1;{ColorizeMixin.repr_color_code};{ColorizeMixin.repr_background_color_code}m' \
               f'{self.title} | {self.price} ₽'


class Adverter(ColorizeMixin):
    def __init__(self, objects):
        """Initialize Adverter with JSON objects (check that we have title and check that price is correct)"""
        if "title" not in objects:
            raise TitleIsNotPresentedException("title is not presented")
        if "price" in objects and (not isinstance(objects["price"], int) or objects["price"] < 0):
            raise ValueError("must be >= 0")
        self.__dict__["_values"] = Objectizer(objects)

    def __getattr__(self, item: str):
        value = self.__dict__.get("_values").__getattr__(item)
        if value is None and item == "price":
            return 0
        return value

    def __setattr__(self, key: str, value: Any):
        if key == "price" and (not isinstance(value, int) or value < 0):
            raise ValueError("must be >= 0")
        return self.__dict__.get("_values").__setattr__(key, value)

    def __str__(self):
        return f'{self.title} | {self.price} ₽'


class TestAdverter(unittest.TestCase):

    def test_first(self):
        lesson_str = """{
                "title": "python",
                "price": 1,
                "class": 123,
                "location": {
                    "address": "город Москва, Лесная, 7",
                    "metro_stations": ["Белорусская"]
                    }
                }"""
        lesson = json.loads(lesson_str)
        lesson_ad = Adverter(lesson)
        self.assertEqual(lesson_ad.title, "python")
        self.assertEqual(lesson_ad.price, 1)
        self.assertEqual(lesson_ad.class_, 123)
        self.assertEqual(lesson_ad.location.address, "город Москва, Лесная, 7")
        self.assertEqual(lesson_ad.location.metro_stations, ["Белорусская"])
        self.assertEqual(str(lesson_ad), "python | 1 ₽")

    def test_second(self):
        lesson_str = """{
                        "title": "python",
                        "class": 123,
                        "location": {
                            "address": "город Москва, Лесная, 7",
                            "metro_stations": ["Белорусская"]
                            }
                        }"""
        lesson = json.loads(lesson_str)
        lesson_ad = Adverter(lesson)
        self.assertEqual(lesson_ad.price, 0)

    def test_third(self):
        lesson_str = """{
                        "price": 0,
                        "class": 123,
                        "location": {
                            "address": "город Москва, Лесная, 7",
                            "metro_stations": ["Белорусская"]
                            }
                        }"""
        lesson = json.loads(lesson_str)
        with self.assertRaises(TitleIsNotPresentedException) as cm:
            Adverter(lesson)
        the_exception = cm.exception
        self.assertEqual(the_exception.message, "title is not presented")

    def test_fourth(self):
        lesson_str = """{
                        "title": 123,
                        "price": -1,
                        "class": 123,
                        "location": {
                            "address": "город Москва, Лесная, 7",
                            "metro_stations": ["Белорусская"]
                            }
                        }"""
        lesson = json.loads(lesson_str)
        with self.assertRaises(ValueError) as cm:
            Adverter(lesson)


if __name__ == "__main__":
    lesson_str = """{
        "title": "python",
        "price": 1,
        "class": 123,
        "location": {
            "address": "город Москва, Лесная, 7",
            "metro_stations": ["Белорусская"]
            }
        }"""
    lesson = json.loads(lesson_str)
    lesson_ad = Adverter(lesson)
    print(repr(lesson_ad))
    print(lesson_ad)
    unittest.main()
