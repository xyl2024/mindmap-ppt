#!/usr/bin/env python3
"""从 skill 内置资源创建独立静态 Mindmap PPT 项目。"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "static-template"
HELP_TEXT = """用法：python scripts/scaffold.py [输出目录] [--overwrite-app] [--overwrite-source]

创建或刷新一个独立静态 Mindmap PPT 项目。

参数：
  输出目录              可选，默认为当前目录
  --overwrite-app       覆盖 index.html 和 src 播放器文件
  --overwrite-source    覆盖 project/source.js 占位内容
  -h, --help            显示此帮助信息
"""


def copy_file(src: Path, dest: Path, *, overwrite: bool) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not overwrite:
        return "已保留"
    shutil.copy2(src, dest)
    return "已写入"


def parse_args(argv: list[str]) -> tuple[Path, bool, bool]:
    if "-h" in argv or "--help" in argv:
        print(HELP_TEXT)
        raise SystemExit(0)

    overwrite_app = False
    overwrite_source = False
    positional: list[str] = []

    for arg in argv:
        if arg == "--overwrite-app":
            overwrite_app = True
        elif arg == "--overwrite-source":
            overwrite_source = True
        elif arg.startswith("-"):
            print(f"未知参数：{arg}")
            print(HELP_TEXT)
            raise SystemExit(2)
        else:
            positional.append(arg)

    if len(positional) > 1:
        print("只能提供一个输出目录。")
        print(HELP_TEXT)
        raise SystemExit(2)

    target = Path(positional[0] if positional else ".").resolve()
    return target, overwrite_app, overwrite_source


def main() -> int:
    target, overwrite_app, overwrite_source = parse_args(sys.argv[1:])
    app_files = [
        "index.html",
        "src/main.js",
        "src/styles.css",
    ]
    source_file = "project/source.js"

    for rel in app_files:
        status = copy_file(TEMPLATE_DIR / rel, target / rel, overwrite=overwrite_app)
        print(f"{status}: {target / rel}")

    status = copy_file(TEMPLATE_DIR / source_file, target / source_file, overwrite=overwrite_source)
    print(f"{status}: {target / source_file}")
    print("直接用浏览器打开 index.html 即可预览。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
