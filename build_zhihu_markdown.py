#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
一键将 Markdown 文档处理为更适合知乎发布的版本。

处理顺序：
1. 移除行内代码中的 ** 标记
2. 去掉语雀 ::: 高亮块外壳
3. 将 aligned 公式拆成多条独立展示公式
4. 移除 LaTeX \color{...} 命令
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from convert_aligned_blocks import convert_aligned_blocks
from convert_highlight_blocks import convert_highlight_blocks
from remove_bold_from_code import remove_bold_from_inline_code
from remove_latex_color import remove_latex_color


def _default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_zhihu{input_path.suffix}")


def build_zhihu_markdown(text: str) -> tuple[str, dict[str, int]]:
    stats: dict[str, int] = {}

    text, bold_count = remove_bold_from_inline_code(text)
    stats["inline_code_bold"] = bold_count

    text, highlight_count = convert_highlight_blocks(text, mode="unwrap")
    stats["highlight_blocks"] = highlight_count

    text, aligned_count = convert_aligned_blocks(text)
    stats["aligned_blocks"] = aligned_count

    text, color_count = remove_latex_color(text)
    stats["latex_colors"] = color_count

    return text, stats


def process_file(input_file: str, output_file: str | None = None) -> Path:
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")

    target_path = Path(output_file) if output_file else input_path
    original_text = input_path.read_text(encoding="utf-8")
    final_text, stats = build_zhihu_markdown(original_text)
    target_path.write_text(final_text, encoding="utf-8")

    print(f"处理完成: {target_path}")
    print("处理统计：")
    print(f"- 清理的行内代码加粗标记数: {stats['inline_code_bold']}")
    print(f"- 处理的 ::: 高亮块数: {stats['highlight_blocks']}")
    print(f"- 转换的 aligned 公式块数: {stats['aligned_blocks']}")
    print(f"- 移除的 LaTeX 颜色命令数: {stats['latex_colors']}")
    return target_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="一键生成适合知乎发布的 Markdown 文档")
    parser.add_argument("input_file", help="输入 Markdown 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径，不传则直接修改源文件")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    process_file(args.input_file, args.output)


if __name__ == "__main__":
    main()
