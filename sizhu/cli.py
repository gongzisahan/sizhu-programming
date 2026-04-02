from __future__ import annotations

import argparse
import json

from .core import Bazi, analyze_bazi


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="四柱编程最小命盘分析器")
    parser.add_argument("--year", required=True, help="年柱，例如 甲子")
    parser.add_argument("--month", required=True, help="月柱，例如 丙寅")
    parser.add_argument("--day", required=True, help="日柱，例如 丁酉")
    parser.add_argument("--hour", required=True, help="时柱，例如 庚戌")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    bazi = Bazi.from_texts(
        year=args.year,
        month=args.month,
        day=args.day,
        hour=args.hour,
    )
    result = analyze_bazi(bazi)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()