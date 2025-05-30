import unittest
from Typo import Bad_AI

class TestTypo(unittest.TestCase):
    def test_empty_dictionary(self):
        ai = Bad_AI([])
        self.assertEqual(ai.check_word("any"), [])

    def test_empty_strings(self):
        ai = Bad_AI(["", "a", "b"])
        self.assertEqual(ai.check_word(""), [])

    def test_three_letter_words(self):
        words = ["car", "cat", "bar"]
        ai = Bad_AI(words)
        result = ai.check_word("car")
        self.assertCountEqual(result, ["bar", "cat"])

    def test_four_letter_words(self):
        words = ["test", "best", "tent"]
        ai = Bad_AI(words)
        result = ai.check_word("test")
        self.assertCountEqual(result, ["best", "tent"])

    def test_three_words_one_match(self):
        words = ["abcd", "abcf", "wxyz"]
        ai = Bad_AI(words)
        result = ai.check_word("abcd")
        self.assertEqual(result, ["abcf"])

    def test_multiple_words_dog(self):
        words = ["dog", "dig", "dag", "dot"]
        ai = Bad_AI(words)
        first = ai.check_word("dog")
        self.assertCountEqual(first, ["dig", "dag", "dot"])
        second = ai.check_word("dig")
        self.assertCountEqual(second, ["dog", "dag"])

    def test_bee_movie(self):
        words = [
            "according", "to", "all", "known", "laws",
            "of", "aviation", "there", "is", "no",
            "way", "a", "bee", "should", "be",
            "able", "to", "fly"
        ]
        ai = Bad_AI(list(set(words)))
        input_words = [
            "acfording", "tx", "agl", "khown", "lass",
            "ou", "aviatzon", "thyre", "zs", "qo",
            "wak", "l", "vee", "spould", "bq",
            "alle", "ao", "gly"
        ]
        for i in range(len(input_words)):
            self.assertIn(words[i], ai.check_word(input_words[i]))

    def test_example_case(self):
        words = ["aaa", "abc", "xyz", "aba", "aaaa"]
        ai = Bad_AI(words)
        sus_list = ["aaa", "axa", "ab", "xxx", "aaab"]
        expected = [["aba"], ["aaa", "aba"], [], [], ["aaaa"]]
        for sus, exp in zip(sus_list, expected):
            with self.subTest(sus_word=sus):
                result = ai.check_word(sus)
                self.assertCountEqual(result, exp)
                self.assertEqual(result, exp)

if __name__ == '__main__':
    unittest.main()