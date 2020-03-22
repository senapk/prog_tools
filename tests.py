#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from hs import Case, HFile, HMain

class TestHS(unittest.TestCase):
    def setUp(self):
        self.data = """
```
a == b
```
a == b
```hs
--IN : Lista xs e um natural n
--OUT: N-ésimo termo de xs
outro lixo qualquer sem igual igual
elemento 2 [2,7,3,9] banana == 3
case 0 4.4 [1,2,3] 5 [2,7,3,9] == [1,3,4,5,6]
case 1 [1,2,3] 5 [2,7,3,9] == 1 [1,3,4,5,6]
```
```hs
soma 2.4 [2.4,7.3,3.1,9.9] 7banana == 3
```

"""
    def test_load(self):
        tests = HFile.load_from_text(self.data)
        self.assertEqual(tests[0], Case("elemento", "2\n[2,7,3,9]\nbanana", "3"))
        self.assertEqual(tests[1], Case("case", "0\n4.4\n[1,2,3]\n5\n[2,7,3,9]", "[1,3,4,5,6]"))
        self.assertEqual(tests[2], Case("case", "1\n[1,2,3]\n5\n[2,7,3,9]", "1 [1,3,4,5,6]"))
        self.assertEqual(tests[3], Case("soma", "2.4\n[2.4,7.3,3.1,9.9]\n7banana", "3"))
        

class Test2HS(unittest.TestCase):

    def test_hmain_0(self):
        main_gen = HMain.format_main(Case("elemento", "2\n[2,7,3,9]\nbanana", "3"))
        main_str = """main = do
    a <- readLn :: IO Int
    b <- readLn :: IO [Int]
    c <- getLine
    print $ elemento a b c
"""
        self.assertEqual(main_gen, main_str)


if __name__ == '__main__':
    unittest.main()

