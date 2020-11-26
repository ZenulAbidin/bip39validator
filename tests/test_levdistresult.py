from unittest import TestCase
from bip39validator import ValidationFailed
from bip39validator.BIP39WordList import BIP39WordList

levdist_gt2 = """brown
brpyt"""
levdist_le2 = """brow
brol"""

# Expected results *must* be in word alphabetical order.

class TestLevDistResult(TestCase):
    def test_getwordpairs_eq(self):
        bip39 = BIP39WordList("levdist_le2", string=levdist_le2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [("brol", "brow")]
        self.assertEqual(expected_res, res.getwordpairs_eq(1))
        try:
            res.getwordpairs_eq(2)
            self.fail()
        except AssertionError as e:
            pass

    def test_getlinepairs_eq(self):
        bip39 = BIP39WordList("levdist_le2", string=levdist_le2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [(2,1)]
        self.assertEqual(expected_res, res.getlinepairs_eq(1))
        try:
            res.getwordpairs_eq(0)
            self.fail()
        except AssertionError as e:
            pass

    def test_getwordpairs_lt(self):
        bip39 = BIP39WordList("levdist_le2", string=levdist_le2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [("brol", "brow")]
        self.assertEqual(expected_res, res.getwordpairs_lt(2))
        try:
            res.getwordpairs_lt(0)
            self.fail()
        except AssertionError as e:
            pass

    def test_getlinepairs_lt(self):
        bip39 = BIP39WordList("levdist_le2", string=levdist_le2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [(2, 1)]
        self.assertEqual(expected_res, res.getlinepairs_lt(2))
        try:
            res.getlinepairs_lt(0)
            self.fail()
        except AssertionError as e:
            pass

    def test_getwordpairs_gt(self):
        bip39 = BIP39WordList("levdist_gt2", string=levdist_gt2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [("brown", "brpyt")]
        self.assertEqual(expected_res, res.getwordpairs_gt(2))
        try:
            res.getwordpairs_gt(0)
            self.fail()
        except AssertionError as e:
            pass

    def test_getlinepairs_gt(self):
        bip39 = BIP39WordList("levdist_gt2", string=levdist_gt2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [(1, 2)]
        self.assertEqual(expected_res, res.getlinepairs_gt(2))
        try:
            res.getlinepairs_gt(0)
            self.fail()
        except AssertionError as e:
            pass

    def test_getwordpairs_list(self):
        concat = "\n".join([levdist_le2]+["zzyzx"])
        bip39 = BIP39WordList("levdist_concat", string=concat)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [("brol", "brow")]
        self.assertEqual(expected_res, res.getwordpairs_list([1,2]))
        for t in ["abc", [], ["a"], 0]:
            try:
                res.getwordpairs_list(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getlinepairs_list(self):
        concat = "\n".join([levdist_le2]+["zzyzx"])
        bip39 = BIP39WordList("levdist_concat", string=concat)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [(2, 1)]
        self.assertEqual(expected_res, res.getlinepairs_list([1,2]))
        for t in ["abc", [], ["a"], 0]:
            try:
                res.getlinepairs_list(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getdist(self):
        bip39 = BIP39WordList("levdist_le2", string=levdist_le2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = 1
        self.assertEqual(expected_res, res.getdist("brow", "brol"))
        for t in [(1, "abc"), ("", "abc"), ("ABC", "abc"),
                  ("abc", 1), ("abc", ""), ("abc", "ABC")]:
            try:
                res.getdist(*t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getdist_all(self):
        bip39 = BIP39WordList("levdist_le2", string=levdist_le2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [(("brol", "brow"), (2, 1), 1)]
        self.assertEqual(expected_res, res.getdist_all("brow"))
        for t in [1, "", "ABC"]:
            try:
                res.getdist_all(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getdist_all_eq(self):
        bip39 = BIP39WordList("levdist_le2", string=levdist_le2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [(("brol", "brow"), (2, 1), 1)]
        self.assertEqual(expected_res, res.getdist_all_eq("brow", 1))
        for t in [1, "", "ABC"]:
            try:
                res.getdist_all_eq(t, 1)
                self.fail()
            except AssertionError as e:
                pass
            except KeyError as e:
                pass
        try:
            res.getdist_all_eq("abc", 0)
            self.fail()
        except AssertionError as e:
            pass
        except KeyError as e:
            pass

    def test_getdist_all_lt(self):
        bip39 = BIP39WordList("levdist_le2", string=levdist_le2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [(("brol", "brow"), (2, 1), 1)]
        self.assertEqual(expected_res, res.getdist_all_lt("brow", 2))
        for t in [1, "", "ABC"]:
            try:
                res.getdist_all_lt(t, 1)
                self.fail()
            except AssertionError as e:
                pass
            except KeyError as e:
                pass
        try:
            res.getdist_all_lt("abc", 0)
            self.fail()
        except AssertionError as e:
            pass
        except KeyError as e:
            pass

    def test_getdist_all_gt(self):
        bip39 = BIP39WordList("levdist_gt2", string=levdist_gt2)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [(("brpyt", "brown"), (2, 1), 3)]
        self.assertEqual(expected_res, res.getdist_all_gt("brown", 2))
        for t in [1, "", "ABC"]:
            try:
                res.getdist_all_gt(t, 1)
                self.fail()
            except AssertionError as e:
                pass
        try:
            res.getdist_all_gt("abc", 0)
            self.fail()
        except AssertionError as e:
            pass
        except KeyError as e:
            pass

    def test_getdist_all_list(self):
        concat = "\n".join([levdist_le2]+["zzyzx"])
        bip39 = BIP39WordList("concat", string=concat)
        try:
            res = bip39.test_lev_distance(2)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [(("brol", "brow"), (2, 1), 1)]
        self.assertEqual(expected_res, res.getdist_all_list("brow", [1]))
        for t in [1, "", "ABC"]:
            for u in ["abc", [], ["a"], 0]:
                try:
                    res.getdist_all_list(t, u)
                    self.fail()
                except AssertionError as e:
                    pass
                except KeyError as e:
                    pass
