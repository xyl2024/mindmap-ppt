#!/usr/bin/env python3
"""从 skill 内置资源创建独立静态 Mindmap PPT 项目。"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "static-template"
HELP_TEXT = """用法：python scripts/scaffold.py [输出目录] [--title <标题>] [--overwrite-app] [--overwrite-source]

创建或刷新一个独立静态 Mindmap PPT 项目。

参数：
  输出目录              可选，默认为当前目录
  --title <标题>        可选，设置 index.html 的 <title> 标签；默认文本为 "Mindmap PPT Demo"
  --overwrite-app       覆盖 index.html 播放器文件
  --overwrite-source    覆盖 project/source.js 占位内容
  -h, --help            显示此帮助信息
"""


def copy_file(src: Path, dest: Path, *, overwrite: bool, title: str | None = None) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not overwrite:
        return "已保留"
    content = src.read_text(encoding="utf-8")
    if title is not None:
        content = content.replace("Mindmap PPT Demo", title)
    dest.write_text(content, encoding="utf-8")
    return "已写入"


def parse_args(argv: list[str]) -> tuple[Path, str | None, bool, bool]:
    if "-h" in argv or "--help" in argv:
        print(HELP_TEXT)
        raise SystemExit(0)

    overwrite_app = False
    overwrite_source = False
    title: str | None = None
    positional: list[str] = []
    consumed: set[int] = set()

    for i, arg in enumerate(argv):
        if i in consumed:
            continue
        if arg == "--title":
            if i + 1 < len(argv):
                title = argv[i + 1]
                consumed.add(i + 1)
            else:
                print("--title 需要提供标题文本。")
                print(HELP_TEXT)
                raise SystemExit(2)
        elif arg == "--overwrite-app":
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
    return target, title, overwrite_app, overwrite_source


def main() -> int:
    target, title, overwrite_app, overwrite_source = parse_args(sys.argv[1:])
    app_file = "index.html"
    source_file = "project/source.js"

    status = copy_file(TEMPLATE_DIR / app_file, target / app_file, overwrite=overwrite_app, title=title)
    print(f"{status}: {target / app_file}")

    status = copy_file(TEMPLATE_DIR / source_file, target / source_file, overwrite=overwrite_source)
    print(f"{status}: {target / source_file}")
    print("直接用浏览器打开 index.html 即可预览。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())