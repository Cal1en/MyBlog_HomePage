#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
移除 Markdown/LaTeX 公式中的 \color{...} 命令，保留原有公式内容。

示例：
{\color{red} P_f}          -> {P_f}
\color{red}\text{标题}      -> \text{标题}
$ \color{red}a = b $       -> $ a = b $
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


COLOR_PATTERN = re.compile(r"\\color\s*\{[^}]+\}\s*")


def _default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_no_color{input_path.suffix}")


def remove_latex_color(text: str) -> tuple[str, int]:
    cleaned_text, count = COLOR_PATTERN.subn("", text)
    return cleaned_text, count


def process_file(input_file: str, output_file: str | None = None, in_place: bool = False) -> Path:
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")

    target_path = input_path if in_place else Path(output_file) if output_file else _default_output_path(input_path)
    original_text = input_path.read_text(encoding="utf-8")
    cleaned_text, count = remove_latex_color(original_text)
    target_path.write_text(cleaned_text, encoding="utf-8")
    print(f"处理完成: {target_path}")
    print(f"共移除 {count} 处 LaTeX 颜色命令")
    return target_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="移除文档中的 LaTeX \\color{...} 命令")
    parser.add_argument("input_file", help="输入 Markdown 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--in-place", action="store_true", help="直接覆盖原文件")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.in_place and args.output:
        parser.error("--in-place 与 --output 不能同时使用")

    process_file(args.input_file, output_file=args.output, in_place=args.in_place)


if __name__ == "__main__":
    main()
