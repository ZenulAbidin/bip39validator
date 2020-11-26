from unittest import TestCase
from bip39validator import ValidationFailed
from bip39validator.BIP39WordList import BIP39WordList

maxlength_l4 = """blocks
block
bloc
blo"""

class TestMaxLengthResult(TestCase):
    def test_getwords_long(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(4)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = ["block", "blocks"]
        self.assertEqual(expected_res, res.getwords_long())

    def test_getlines_long(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(4)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [2, 1]
        self.assertEqual(expected_res, res.getlines_long())

    def test_getwords_eq(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(1)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = ["bloc"]
        self.assertEqual(expected_res, res.getwords_eq(4))
        for t in [0, ""]:
            try:
                res.getwords_eq(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getlines_eq(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(1)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [3]
        self.assertEqual(expected_res, res.getlines_eq(4))
        for t in [0, ""]:
            try:
                res.getlines_eq(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getwords_lt(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(1)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = ["blo"]
        self.assertEqual(expected_res, res.getwords_lt(4))
        for t in [0, ""]:
            try:
                res.getwords_eq(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getlines_lt(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(1)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [4]
        self.assertEqual(expected_res, res.getlines_lt(4))
        for t in [0, ""]:
            try:
                res.getlines_lt(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getwords_gt(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(1)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = ["block", "blocks"]
        self.assertEqual(expected_res, res.getwords_gt(4))
        for t in [0, ""]:
            try:
                res.getwords_gt(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getlines_gt(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(1)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [2, 1]
        self.assertEqual(expected_res, res.getlines_gt(4))
        for t in [0, ""]:
            try:
                res.getlines_gt(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getwords_list(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(1)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = ["blo", "blocks"]
        self.assertEqual(expected_res, res.getwords_list([3, 6]))
        for t in ["abc", [], ["a"], 0]:
            try:
                res.getwords_list(t)
                self.fail()
            except AssertionError as e:
                pass

    def test_getlines_list(self):
        bip39 = BIP39WordList("maxlength_l4", string=maxlength_l4)
        try:
            res = bip39.test_max_length(1)
        except ValidationFailed as e:
            res = e.status_obj
        expected_res = [4, 1]
        self.assertEqual(expected_res, res.getlines_list([3, 6]))
        for t in ["abc", [], ["a"], 0]:
            try:
                res.getlines_list(t)
                self.fail()
            except AssertionError as e:
                pass