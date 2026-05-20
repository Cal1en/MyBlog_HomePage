#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移除 Markdown 正文中“行内代码”里的 ** 标记。

特性：
1. 只处理行内代码，不处理三反引号/三波浪号围起来的代码块。
2. 支持单反引号和多反引号包裹的行内代码。
3. 默认输出为“原文件名_clean.md”，也可通过参数指定输出路径或原地覆盖。
"""

from __future__ import annotations

import argparse
from pathlib import Path


def _default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}_clean{input_path.suffix}")


def _is_fence_start(line: str) -> tuple[str, int] | None:
    stripped = line.lstrip()
    if stripped.startswith("```"):
        return ("`", len(stripped) - len(stripped.lstrip("`")))
    if stripped.startswith("~~~"):
        return ("~", len(stripped) - len(stripped.lstrip("~")))
    return None


def _process_inline_code_in_line(line: str) -> tuple[str, int]:
    result: list[str] = []
    i = 0
    replacements = 0
    length = len(line)

    while i < length:
        if line[i] != "`":
            result.append(line[i])
            i += 1
            continue

        tick_count = 1
        while i + tick_count < length and line[i + tick_count] == "`":
            tick_count += 1

        delimiter = "`" * tick_count
        end = line.find(delimiter, i + tick_count)
        if end == -1:
            result.append(delimiter)
            i += tick_count
            continue

        code_content = line[i + tick_count:end]
        cleaned_content = code_content.replace("**", "")
        replacements += code_content.count("**")
        result.append(delimiter)
        result.append(cleaned_content)
        result.append(delimiter)
        i = end + tick_count

    return "".join(result), replacements


def remove_bold_from_inline_code(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    output_lines: list[str] = []
    total_replacements = 0
    in_fenced_code = False
    current_fence_char = ""
    current_fence_len = 0

    for line in lines:
        fence = _is_fence_start(line)
        if not in_fenced_code and fence:
            current_fence_char, current_fence_len = fence
            in_fenced_code = True
            output_lines.append(line)
            continue

        if in_fenced_code:
            stripped = line.lstrip()
            if stripped.startswith(current_fence_char * current_fence_len):
                in_fenced_code = False
                current_fence_char = ""
                current_fence_len = 0
            output_lines.append(line)
            continue

        cleaned_line, replacements = _process_inline_code_in_line(line)
        output_lines.append(cleaned_line)
        total_replacements += replacements

    return "".join(output_lines), total_replacements


def process_file(input_file: str, output_file: str | None = None, in_place: bool = False) -> Path:
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")

    target_path = input_path if in_place else Path(output_file) if output_file else _default_output_path(input_path)
    original_text = input_path.read_text(encoding="utf-8")
    cleaned_text, replacement_count = remove_bold_from_inline_code(original_text)
    target_path.write_text(cleaned_text, encoding="utf-8")
    print(f"处理完成: {target_path}")
    print(f"共移除 {replacement_count} 个行内代码中的 '**' 标记")
    return target_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="移除 Markdown 行内代码中的 ** 标记")
    parser.add_argument("input_file", help="输入 Markdown 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径，不传则生成 *_clean.md")
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
