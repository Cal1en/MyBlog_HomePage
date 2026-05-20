#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理语雀风格的 ::: 高亮块。

默认行为：
1. 去掉起始行如 :::info、:::warning、:::tip、:::color4
2. 去掉结束行 :::
3. 保留块内正文不变

也支持把块内容转成引用块，便于在知乎里保留“提示感”。
"""

from __future__ import annotations

import argparse
from pathlib import Path


def _default_output_path(input_path: Path, mode: str) -> Path:
    suffix = "_unwrapped" if mode == "unwrap" else "_quote"
    return input_path.with_name(f"{input_path.stem}{suffix}{input_path.suffix}")


def _is_highlight_start(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith(":::") and stripped != ":::"


def _is_highlight_end(line: str) -> bool:
    return line.strip() == ":::"


def _convert_block(lines: list[str], mode: str) -> list[str]:
    if mode == "unwrap":
        return lines

    if mode == "quote":
        converted: list[str] = []
        for line in lines:
            content = line.rstrip("\r\n")
            newline = line[len(content):]
            if content:
                converted.append(f"> {content}{newline}")
            else:
                converted.append(f">{newline}")
        return converted

    raise ValueError(f"不支持的模式: {mode}")


def convert_highlight_blocks(text: str, mode: str = "unwrap") -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    inside_block = False
    block_lines: list[str] = []
    block_count = 0

    for line in lines:
        if not inside_block and _is_highlight_start(line):
            inside_block = True
            block_lines = []
            block_count += 1
            continue

        if inside_block and _is_highlight_end(line):
            output.extend(_convert_block(block_lines, mode))
            inside_block = False
            block_lines = []
            continue

        if inside_block:
            block_lines.append(line)
        else:
            output.append(line)

    if inside_block:
        output.append(f":::未闭合高亮块，已按普通文本保留\n")
        output.extend(block_lines)

    return "".join(output), block_count


def process_file(input_file: str, output_file: str | None = None, in_place: bool = False, mode: str = "unwrap") -> Path:
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")

    target_path = input_path if in_place else Path(output_file) if output_file else _default_output_path(input_path, mode)
    original_text = input_path.read_text(encoding="utf-8")
    converted_text, block_count = convert_highlight_blocks(original_text, mode=mode)
    target_path.write_text(converted_text, encoding="utf-8")
    print(f"处理完成: {target_path}")
    print(f"共处理 {block_count} 个 ::: 高亮块")
    print(f"处理模式: {mode}")
    return target_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="移除或转换语雀 ::: 高亮块")
    parser.add_argument("input_file", help="输入 Markdown 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--in-place", action="store_true", help="直接覆盖原文件")
    parser.add_argument(
        "--mode",
        choices=["unwrap", "quote"],
        default="unwrap",
        help="unwrap=去掉 ::: 外壳并保留正文；quote=转成引用块",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.in_place and args.output:
        parser.error("--in-place 与 --output 不能同时使用")

    process_file(
        args.input_file,
        output_file=args.output,
        in_place=args.in_place,
        mode=args.mode,
    )


if __name__ == "__main__":
    main()
