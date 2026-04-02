import unittest

from sizhu.core import Bazi, analyze_bazi, get_shishen


class TestShiShen(unittest.TestCase):
    def test_same_element(self):
        self.assertEqual(get_shishen("甲", "甲"), "比肩")
        self.assertEqual(get_shishen("甲", "乙"), "劫财")

    def test_output_element(self):
        self.assertEqual(get_shishen("甲", "丙"), "食神")
        self.assertEqual(get_shishen("甲", "丁"), "伤官")

    def test_wealth(self):
        self.assertEqual(get_shishen("甲", "戊"), "偏财")
        self.assertEqual(get_shishen("甲", "己"), "正财")

    def test_officer(self):
        self.assertEqual(get_shishen("甲", "庚"), "七杀")
        self.assertEqual(get_shishen("甲", "辛"), "正官")

    def test_resource(self):
        self.assertEqual(get_shishen("甲", "壬"), "偏印")
        self.assertEqual(get_shishen("甲", "癸"), "正印")

    def test_analyze_bazi(self):
        bazi = Bazi.from_texts("甲子", "丙寅", "丁酉", "庚戌")
        result = analyze_bazi(bazi)

        self.assertEqual(result["四柱"]["年柱"], "甲子")
        self.assertEqual(result["日主"]["天干"], "丁")
        self.assertEqual(result["天干十神"]["年干"]["十神"], "正印")
        self.assertIn("明面五行统计", result)


if __name__ == "__main__":
    unittest.main()