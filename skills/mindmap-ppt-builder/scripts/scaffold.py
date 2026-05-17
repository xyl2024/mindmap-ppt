#!/usr/bin/env python3
"""从 skill 内置资源创建独立静态 Mindmap PPT 项目。"""

from __future__ import annotations

import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "static-template"
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
HELP_TEXT = """用法：python scripts/scaffold.py <项目名> [输出目录] [--title <标题>] [--overwrite-app] [--overwrite-source]

创建或刷新一个独立静态 Mindmap PPT 项目。

参数：
  项目名                必填，用作输出目录下的项目文件夹名称
  输出目录              可选，默认为当前目录；最终生成路径为 <输出目录>/<项目名>/
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


def ensure_dir(path: Path) -> str:
    existed = path.exists()
    path.mkdir(parents=True, exist_ok=True)
    return "已存在" if existed else "已创建"


def print_tree(root: Path) -> None:
    print("目录结构：")
    print(f"{root.name}/")

    def sort_key(path: Path) -> tuple[int, str]:
        return (1 if path.is_file() else 0, path.name.lower())

    def walk(directory: Path, prefix: str = "") -> None:
        entries = sorted(directory.iterdir(), key=sort_key)
        for index, entry in enumerate(entries):
            is_last = index == len(entries) - 1
            connector = "└── " if is_last else "├── "
            suffix = "/" if entry.is_dir() else ""
            print(f"{prefix}{connector}{entry.name}{suffix}")
            if entry.is_dir():
                extension = "    " if is_last else "│   "
                walk(entry, prefix + extension)

    walk(root)


def validate_project_name(project_name: str) -> str:
    project_path = Path(project_name)
    if (
        not project_name.strip()
        or project_name in {".", ".."}
        or project_path.is_absolute()
        or project_path.name != project_name
    ):
        print("项目名必须是单层文件夹名称，不能是路径。")
        print(HELP_TEXT)
        raise SystemExit(2)
    return project_name


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

    if not positional:
        print("需要提供项目名。")
        print(HELP_TEXT)
        raise SystemExit(2)

    if len(positional) > 2:
        print("只能提供一个项目名和一个输出目录。")
        print(HELP_TEXT)
        raise SystemExit(2)

    project_name = validate_project_name(positional[0])
    output_dir = Path(positional[1] if len(positional) == 2 else ".").resolve()
    target = output_dir / project_name
    return target, title, overwrite_app, overwrite_source


def main() -> int:
    target, title, overwrite_app, overwrite_source = parse_args(sys.argv[1:])
    app_file = "index.html"
    source_file = "project/source.js"

    status = copy_file(TEMPLATE_DIR / app_file, target / app_file, overwrite=overwrite_app, title=title)
    print(f"{status}: {target / app_file}")

    status = copy_file(TEMPLATE_DIR / source_file, target / source_file, overwrite=overwrite_source)
    print(f"{status}: {target / source_file}")

    for dirname in ("images", "codes"):
        directory = target / "project" / dirname
        status = ensure_dir(directory)
        print(f"{status}: {directory}")

    print()
    print_tree(target)
    print()
    print("直接用浏览器打开 index.html 即可预览。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
