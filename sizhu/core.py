from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


GANS = "甲乙丙丁戊己庚辛壬癸"
ZHIS = "子丑寅卯辰巳午未申酉戌亥"

GAN_TO_WUXING: Dict[str, str] = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

GAN_TO_YINYANG: Dict[str, str] = {
    "甲": "阳", "乙": "阴",
    "丙": "阳", "丁": "阴",
    "戊": "阳", "己": "阴",
    "庚": "阳", "辛": "阴",
    "壬": "阳", "癸": "阴",
}

ZHI_TO_MAIN_WUXING: Dict[str, str] = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}

# 常用地支藏干表
ZHI_TO_HIDDEN_GANS: Dict[str, List[str]] = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

GENERATES: Dict[str, str] = {
    "木": "火",
    "火": "土",
    "土": "金",
    "金": "水",
    "水": "木",
}

CONTROLS: Dict[str, str] = {
    "木": "土",
    "土": "水",
    "水": "火",
    "火": "金",
    "金": "木",
}

GENERATED_BY: Dict[str, str] = {v: k for k, v in GENERATES.items()}
CONTROLLED_BY: Dict[str, str] = {v: k for k, v in CONTROLS.items()}


@dataclass(frozen=True)
class Pillar:
    gan: str
    zhi: str

    def __post_init__(self) -> None:
        if self.gan not in GANS:
            raise ValueError(f"无效天干: {self.gan}")
        if self.zhi not in ZHIS:
            raise ValueError(f"无效地支: {self.zhi}")

    @classmethod
    def from_text(cls, text: str) -> "Pillar":
        text = text.strip()
        if len(text) != 2:
            raise ValueError(f"柱必须是2个汉字，例如“甲子”，收到: {text}")
        return cls(gan=text[0], zhi=text[1])

    @property
    def text(self) -> str:
        return f"{self.gan}{self.zhi}"


@dataclass(frozen=True)
class Bazi:
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar

    @classmethod
    def from_texts(cls, year: str, month: str, day: str, hour: str) -> "Bazi":
        return cls(
            year=Pillar.from_text(year),
            month=Pillar.from_text(month),
            day=Pillar.from_text(day),
            hour=Pillar.from_text(hour),
        )

    @property
    def day_master(self) -> str:
        return self.day.gan


def get_shishen(day_master_gan: str, other_gan: str) -> str:
    """
    以“日主天干”为参照，计算另一个天干对应的十神。
    """
    if day_master_gan not in GAN_TO_WUXING:
        raise ValueError(f"无效日主天干: {day_master_gan}")
    if other_gan not in GAN_TO_WUXING:
        raise ValueError(f"无效目标天干: {other_gan}")

    dm_wx = GAN_TO_WUXING[day_master_gan]
    other_wx = GAN_TO_WUXING[other_gan]
    same_polarity = GAN_TO_YINYANG[day_master_gan] == GAN_TO_YINYANG[other_gan]

    # 同我
    if dm_wx == other_wx:
        return "比肩" if same_polarity else "劫财"

    # 我生
    if GENERATES[dm_wx] == other_wx:
        return "食神" if same_polarity else "伤官"

    # 我克
    if CONTROLS[dm_wx] == other_wx:
        return "偏财" if same_polarity else "正财"

    # 生我
    if GENERATED_BY[dm_wx] == other_wx:
        return "偏印" if same_polarity else "正印"

    # 克我
    if CONTROLLED_BY[dm_wx] == other_wx:
        return "七杀" if same_polarity else "正官"

    raise RuntimeError("十神计算出现未覆盖分支")


def count_visible_wuxing(bazi: Bazi) -> Dict[str, int]:
    """
    只统计明面上的八个字：
    4个天干 + 4个地支主气
    """
    result = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for pillar in [bazi.year, bazi.month, bazi.day, bazi.hour]:
        result[GAN_TO_WUXING[pillar.gan]] += 1
        result[ZHI_TO_MAIN_WUXING[pillar.zhi]] += 1
    return result


def get_hidden_stem_details(branch: str, day_master_gan: str) -> List[Dict[str, str]]:
    hidden = []
    for gan in ZHI_TO_HIDDEN_GANS[branch]:
        hidden.append(
            {
                "天干": gan,
                "五行": GAN_TO_WUXING[gan],
                "阴阳": GAN_TO_YINYANG[gan],
                "十神": get_shishen(day_master_gan, gan),
            }
        )
    return hidden


def analyze_bazi(bazi: Bazi) -> Dict[str, object]:
    """
    第一版最小分析器：
    - 四柱结构
    - 日主
    - 其余三干相对日主的十神
    - 四支藏干及其十神
    - 明面五行统计
    """
    day_master = bazi.day_master

    stem_relations = {
        "年干": {
            "天干": bazi.year.gan,
            "十神": get_shishen(day_master, bazi.year.gan),
        },
        "月干": {
            "天干": bazi.month.gan,
            "十神": get_shishen(day_master, bazi.month.gan),
        },
        "日干": {
            "天干": bazi.day.gan,
            "十神": "日主",
        },
        "时干": {
            "天干": bazi.hour.gan,
            "十神": get_shishen(day_master, bazi.hour.gan),
        },
    }

    hidden_relations = {
        "年支": {
            "地支": bazi.year.zhi,
            "藏干": get_hidden_stem_details(bazi.year.zhi, day_master),
        },
        "月支": {
            "地支": bazi.month.zhi,
            "藏干": get_hidden_stem_details(bazi.month.zhi, day_master),
        },
        "日支": {
            "地支": bazi.day.zhi,
            "藏干": get_hidden_stem_details(bazi.day.zhi, day_master),
        },
        "时支": {
            "地支": bazi.hour.zhi,
            "藏干": get_hidden_stem_details(bazi.hour.zhi, day_master),
        },
    }

    return {
        "四柱": {
            "年柱": bazi.year.text,
            "月柱": bazi.month.text,
            "日柱": bazi.day.text,
            "时柱": bazi.hour.text,
        },
        "日主": {
            "天干": day_master,
            "五行": GAN_TO_WUXING[day_master],
            "阴阳": GAN_TO_YINYANG[day_master],
        },
        "天干十神": stem_relations,
        "地支藏干十神": hidden_relations,
        "明面五行统计": count_visible_wuxing(bazi),
    }