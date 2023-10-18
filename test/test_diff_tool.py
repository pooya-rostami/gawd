import pytest

import gawd


class TestTextDiffTool:

    def test_distance_equal_objects(self):
        assert gawd.distance(42, 42) == 0 # same number
        assert gawd.distance('ab', 'ab') == 0 # same text
        assert gawd.distance(['a', 'b', 'ab'], ['a', 'b', 'ab']) == 0 # same list
        assert gawd.distance(['a', 'b', None], ['a', 'b', None]) == 0 # same list including None
        assert gawd.distance({'a':1, 'b':0, 'ab':2}, {'a':1, 'b':0, 'ab':2}) == 0 # same dictionary
        assert gawd.distance({'a':None, 'b':0, 'ab':None}, {'a':None, 'b':0, 'ab':None}) == 0 # same dictionary including None
        assert gawd.distance(None, None) == 0 # both None


    def test_distance_similarity(self):
        assert gawd.distance([1, 2, 3, 4], [1, 2, 3, 4]) == 0 # Assuming find_list_matches returns [(1, 2, 0.25), (2, 3, 0.25), (3, 4, 0.25), (4, 5, 0.25)]
        assert gawd.distance([1, 2, 3, 4], [2, 3, 4, 5]) == sum(score for _, _, score in gawd.find_list_matches([1, 2, 3, 4], [2, 3, 4, 5])) / len(gawd.find_list_matches([1, 2, 3, 4], [2, 3, 4, 5])) # Assuming find_list_matches returns [(1, 2, 0.25), (2, 3, 0.25), (3, 4, 0.25), (4, 5, 0.25)]
        assert gawd.distance("hello", "hola") == 0.5555555555555556 # 1 - difflib.SequenceMatcher(None, 'Hello', 'Hola').ratio()
        assert gawd.distance(123, "123") == 1 # two different type of object
        assert gawd.distance(123, None) == 1 # two different type of object
        assert gawd.distance(None, [1, 2, 3]) == 1 # two different type of object
        assert gawd.distance([1, 2, 3, 4], {2:1, 3:7, 4:3, 5:9}) == 1 # two different type of object


    def test_dict_distance(self):
        assert gawd.dict_distance({'a': 1, 'b': 2, 'c': 3}, {'b': 2, 'c': 4, 'd': 5}) == (gawd.distance(2, 2) + gawd.distance(3, 4) + 1 + 1) / 4
        assert gawd.dict_distance({}, {}) == 0 # it should not be a problem since dict distance go through distance
        assert gawd.dict_distance({'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 2, 'c': 3}) == 0
        assert gawd.dict_distance({'a': 1, 'b': 'two', 'c': [1, 2, 3]}, {'a': 1, 'b': 2, 'c': [1, 2, 3]}) ==  (gawd.distance('two', 2)) / 3
        assert gawd.dict_distance({'a': 1, 'b': 2, 'c': {1:1, 2:3, 3:5}}, {'a': 1, 'b': 2, 'c': {1:1, 2:3, 3:5}}) ==  0
        assert gawd.dict_distance({'a': 1, 'b': 2, 'c': 3}, {'a': None}) == 1
        assert gawd.dict_distance({'a': 1, 'b': 2, 'c': 3}, {}) == 1
