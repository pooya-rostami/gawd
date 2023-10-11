import pytest

import diff_tool


class TestTextDiffTool:
    
    def test_distance_equal_objects(self):
        assert diff_tool.distance(42, 42) == 0 # same number
        assert diff_tool.distance('ab', 'ab') == 0 # same text
        assert diff_tool.distance(['a', 'b', 'ab'], ['a', 'b', 'ab']) == 0 # same list
        assert diff_tool.distance(['a', 'b', None], ['a', 'b', None]) == 0 # same list including None
        assert diff_tool.distance({'a':1, 'b':0, 'ab':2}, {'a':1, 'b':0, 'ab':2}) == 0 # same dictionary
        assert diff_tool.distance({'a':None, 'b':0, 'ab':None}, {'a':None, 'b':0, 'ab':None}) == 0 # same dictionary including None
        assert diff_tool.distance(None, None) == 0 # both None


    def test_distance_similarity(self):
        assert diff_tool.distance([1, 2, 3, 4], [1, 2, 3, 4]) == 0 # Assuming find_matches returns [(1, 2, 0.25), (2, 3, 0.25), (3, 4, 0.25), (4, 5, 0.25)]
        assert diff_tool.distance([1, 2, 3, 4], [2, 3, 4, 5]) == sum(score for _, _, score in diff_tool.find_matches([1, 2, 3, 4], [2, 3, 4, 5])) / len(diff_tool.find_matches([1, 2, 3, 4], [2, 3, 4, 5])) # Assuming find_matches returns [(1, 2, 0.25), (2, 3, 0.25), (3, 4, 0.25), (4, 5, 0.25)]
        assert diff_tool.distance("hello", "hola") == 0.5555555555555556 # 1 - difflib.SequenceMatcher(None, 'Hello', 'Hola').ratio()
        assert diff_tool.distance(123, "123") == 1 # two different type of object
        assert diff_tool.distance(123, None) == 1 # two different type of object
        assert diff_tool.distance(None, [1, 2, 3]) == 1 # two different type of object
        assert diff_tool.distance([1, 2, 3, 4], {2:1, 3:7, 4:3, 5:9}) == 1 # two different type of object


    def test_dict_distance(self):
        assert diff_tool.dict_distance({'a': 1, 'b': 2, 'c': 3}, {'b': 2, 'c': 4, 'd': 5}) == (diff_tool.distance(2, 2) + diff_tool.distance(3, 4) + 1 + 1) / 4
        assert diff_tool.dict_distance({}, {}) == 0 # it should not be a problem since dict distance go through distance
        assert diff_tool.dict_distance({'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'b': 2, 'c': 3}) == 0 
        assert diff_tool.dict_distance({'a': 1, 'b': 'two', 'c': [1, 2, 3]}, {'a': 1, 'b': 2, 'c': [1, 2, 3]}) ==  (diff_tool.distance('two', 2)) / 3
        assert diff_tool.dict_distance({'a': 1, 'b': 2, 'c': {1:1, 2:3, 3:5}}, {'a': 1, 'b': 2, 'c': {1:1, 2:3, 3:5}}) ==  0
        assert diff_tool.dict_distance({'a': 1, 'b': 2, 'c': 3}, {'a': None}) == 1 
        assert diff_tool.dict_distance({'a': 1, 'b': 2, 'c': 3}, {}) == 1
