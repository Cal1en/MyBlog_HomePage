#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
将不兼容知乎的 aligned 公式环境展开为多条独立展示公式。

支持两种常见写法：
1. $ \begin{aligned} ... \end{aligned} $
2. $ \begin{gather*} ... \begin{aligned} ... \end{aligned} ... \end{gather*} $

转换策略：
- 每个 aligned 的顶层公式行会被拆成一个独立的 $$ ... $$ 块
- 仅移除“顶层对齐”用的第一个 &
- 保留矩阵、颜色、pmatrix/bmatrix 等嵌套环境
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


BEGIN_ALIGNED = r"\begin{aligned}"
END_ALIGNED = r"\end{aligned}"
BEGIN_GATHER = r"\begin{gather*}"
END_GATHER = r"\end{gather*}"


def _default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_no_aligned{input_path.suffix}")


def _skip_optional_spacing(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def _split_top_level_rows(content: str) -> list[str]:
    rows: list[str] = []
    current: list[str] = []
    env_depth = 0
    i = 0

    while i < len(content):
        if content.startswith(r"\begin{", i):
            end = content.find("}", i + len(r"\begin{"))
            if end == -1:
                current.append(content[i])
                i += 1
                continue
            env_depth += 1
            current.append(content[i : end + 1])
            i = end + 1
            continue

        if content.startswith(r"\end{", i):
            end = content.find("}", i + len(r"\end{"))
            if end == -1:
                current.append(content[i])
                i += 1
                continue
            env_depth = max(0, env_depth - 1)
            current.append(content[i : end + 1])
            i = end + 1
            continue

        if env_depth == 0 and content.startswith(r"\\", i):
            rows.append("".join(current))
            current = []
            i += 2
            if i < len(content) and content[i] == "[":
                end = content.find("]", i + 1)
                if end != -1:
                    i = end + 1
            i = _skip_optional_spacing(content, i)
            continue

        current.append(content[i])
        i += 1

    if current:
        rows.append("".join(current))

    return rows


def _remove_first_top_level_alignment_marker(row: str) -> str:
    env_depth = 0
    i = 0

    while i < len(row):
        if row.startswith(r"\begin{", i):
            end = row.find("}", i + len(r"\begin{"))
            if end == -1:
                i += 1
                continue
            env_depth += 1
            i = end + 1
            continue

        if row.startswith(r"\end{", i):
            end = row.find("}", i + len(r"\end{"))
            if end == -1:
                i += 1
                continue
            env_depth = max(0, env_depth - 1)
            i = end + 1
            continue

        if env_depth == 0 and row[i] == "&":
            return row[:i] + row[i + 1 :]

        i += 1

    return row


def _format_display_math(row: str) -> str:
    cleaned = _remove_first_top_level_alignment_marker(row).strip()
    if not cleaned:
        return ""
    return "$$\n" + cleaned + "\n$$"


def _convert_aligned_content(content: str) -> str:
    rows = _split_top_level_rows(content)
    formulas = [_format_display_math(row) for row in rows]
    formulas = [item for item in formulas if item]
    return "\n\n".join(formulas)


def _replace_gather_blocks(text: str) -> tuple[str, int]:
    pattern = re.compile(r"\$\s*\\begin\{gather\*\}(.*?)\\end\{gather\*\}\s*\$", re.DOTALL)
    count = 0

    def replacer(match: re.Match[str]) -> str:
        nonlocal count
        inner = match.group(1)
        aligned_pattern = re.compile(r"\\begin\{aligned\}(.*?)\\end\{aligned\}", re.DOTALL)
        converted_parts = []

        for aligned_match in aligned_pattern.finditer(inner):
            converted = _convert_aligned_content(aligned_match.group(1))
            if converted:
                converted_parts.append(converted)

        if not converted_parts:
            return match.group(0)

        count += 1
        return "\n\n".join(converted_parts)

    return pattern.sub(replacer, text), count


def _replace_aligned_blocks(text: str) -> tuple[str, int]:
    pattern = re.compile(r"\$\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\$", re.DOTALL)
    count = 0

    def replacer(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return _convert_aligned_content(match.group(1))

    return pattern.sub(replacer, text), count


def convert_aligned_blocks(text: str) -> tuple[str, int]:
    converted_text, gather_count = _replace_gather_blocks(text)
    converted_text, aligned_count = _replace_aligned_blocks(converted_text)
    return converted_text, gather_count + aligned_count


def process_file(input_file: str, output_file: str | None = None, in_place: bool = False) -> Path:
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")

    target_path = input_path if in_place else Path(output_file) if output_file else _default_output_path(input_path)
    original_text = input_path.read_text(encoding="utf-8")
    converted_text, block_count = convert_aligned_blocks(original_text)
    target_path.write_text(converted_text, encoding="utf-8")
    print(f"处理完成: {target_path}")
    print(f"共转换 {block_count} 处包含 aligned 的公式块")
    return target_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="将 aligned 公式环境展开为多条独立展示公式")
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
