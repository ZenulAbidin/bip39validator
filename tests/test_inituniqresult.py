from unittest import TestCase
from bip39validator.BIP39WordList import BIP39WordList

inituniq_2group_l3 = """quick
quote"""
inituniq_4group_l3 = """quick
quote
risk
rich"""


class TestInitUniqResult(TestCase):
    def test_similargroup(self):
        bip39 = BIP39WordList("inituniq_2group_l3", string=inituniq_2group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = [("quick", 1), ("quote", 2)]
        self.assertEqual(expected_res, res.similargroup("qu"))
        for t in [0, ""]:
            try:
                res.similargroup(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_similar_wordgroup(self):
        bip39 = BIP39WordList("inituniq_2group_l3", string=inituniq_2group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = ["quick", "quote"]
        self.assertEqual(expected_res, res.similar_wordgroup("qu"))
        for t in [0, ""]:
            try:
                res.similar_wordgroup(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_similar_linegroup(self):
        bip39 = BIP39WordList("inituniq_2group_l3", string=inituniq_2group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = [1, 2]
        self.assertEqual(expected_res, res.similar_linegroup("qu"))
        for t in [0, ""]:
            try:
                res.similar_linegroup(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_similargroup_many(self):
        bip39 = BIP39WordList("inituniq_4group_l3", string=inituniq_4group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = {"qu": [("quick", 1), ("quote", 2)], "ri":
            [("rich", 4), ("risk", 3)]}
        self.assertEqual(expected_res, res.similargroup_many(["qu", "ri"]))
        for t in ["abc", [], ["a"], 0]:
            try:
                res.similargroup_many(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_similar_wordgroup_many(self):
        bip39 = BIP39WordList("inituniq_4group_l3", string=inituniq_4group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = {"qu": ["quick", "quote"], "ri":
            ["rich", "risk"]}
        self.assertEqual(expected_res, res.similar_wordgroup_many(["qu", "ri"]))
        for t in ["abc", [], ["a"], 0]:
            try:
                res.similar_wordgroup_many(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_similar_linegroup_many(self):
        bip39 = BIP39WordList("inituniq_4group_l3", string=inituniq_4group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = {"qu": [1, 2], "ri":
            [4, 3]}
        self.assertEqual(expected_res, res.similar_linegroup_many(["qu", "ri"]))
        for t in ["abc", [], ["a"], 0]:
            try:
                res.similar_linegroup_many(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_similargroup_all(self):
        bip39 = BIP39WordList("inituniq_2group_l3", string=inituniq_2group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = {"qu": [("quick", 1), ("quote", 2)]}
        self.assertEqual(expected_res, res.similargroup_all(2))
        for t in [0, ""]:
            try:
                res.similargroup_all(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_similar_wordgroup_all(self):
        bip39 = BIP39WordList("inituniq_2group_l3", string=inituniq_2group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = {"qu": ["quick", "quote"]}
        self.assertEqual(expected_res, res.similar_wordgroup_all(2))
        for t in [0, ""]:
            try:
                res.similar_wordgroup_all(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_similar_linegroup_all(self):
        bip39 = BIP39WordList("inituniq_2group_l3", string=inituniq_2group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = {"qu": [1, 2]}
        self.assertEqual(expected_res, res.similar_linegroup_all(2))
        for t in [0, ""]:
            try:
                res.similar_linegroup_all(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_groups_length(self):
        bip39 = BIP39WordList("inituniq_2group_l3", string=inituniq_2group_l3)
        res = bip39.test_initial_chars(3)
        expected_res = {"qu": [("quick", 1), ("quote", 2)]}
        self.assertEqual(expected_res, res.groups_length(2))
        for t in [0, ""]:
            try:
                res.similar_wordgroup_all(t)
                self.fail()
            except AssertionError as e:
                pass
