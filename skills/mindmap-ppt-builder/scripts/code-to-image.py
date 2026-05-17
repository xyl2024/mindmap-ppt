"""
代码片段转图片脚本
用法: python code-to-image.py <代码文件> [输出路径]

默认使用 monokai 主题
"""

import os
import sys
from pathlib import Path
from pygments import highlight
from pygments.lexers import guess_lexer, TextLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name


FONT_ENV_VAR = "CODE_TO_IMAGE_FONT"


def find_cjk_font():
    """返回一个尽量支持中文的字体文件路径，找不到时回退到 Consolas。"""
    custom_font = os.environ.get(FONT_ENV_VAR)
    if custom_font:
        custom_font = Path(custom_font).expanduser()
        if custom_font.exists():
            return str(custom_font)

    candidate_paths = [
        # Windows
        Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"),
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
        Path(r"C:\Windows\Fonts\Deng.ttf"),
        # macOS
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
        # Linux / common CJK font packages
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf"),
        Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
        Path("/usr/share/fonts/opentype/adobe-source-han-sans/SourceHanSansSC-Regular.otf"),
    ]

    for font_path in candidate_paths:
        if font_path.exists():
            return str(font_path)

    if custom_font:
        print(f"[WARN] {FONT_ENV_VAR} points to a missing font: {custom_font}")

    return "Consolas"

def code_to_image(input_path, output_path=None):
    input_path = Path(input_path)

    # 读取代码
    code = input_path.read_text(encoding="utf-8")

    # 确定 lexer
    try:
        lexer = guess_lexer(code)
    except:
        lexer = TextLexer()

    # 输出路径
    if not output_path:
        output_path = input_path.with_suffix(".png")
    else:
        output_path = Path(output_path)
        if output_path.is_dir():
            # 如果是目录，生成同名 png 文件
            output_path = output_path / (input_path.stem + ".png")

    # 计算合适宽度（每字符约 9px）
    lines = code.split("\n")
    max_line_len = max(len(line) for line in lines)
    width = min(max(max_line_len * 9 + 80, 600), 1200)

    # 行高约 24px
    height = len(lines) * 24 + 80

    # 使用 monokai 主题
    style = get_style_by_name('monokai')

    # 生成图片 - 使用高质量设置
    font_name = find_cjk_font()
    formatter = ImageFormatter(
        font_name=font_name,   # 优先使用支持中文的字体，避免中文渲染成方块
        font_size=16,          # 稍大一点更清晰
        line_numbers=False,
        line_pad=4,            # 行间距
        image_pad=24,          # 边距
        style=style,
    )

    with open(output_path, "wb") as f:
        f.write(highlight(code, lexer, formatter))

    print(f"[OK] Generated: {output_path}")
    print(f"[OK] Font: {font_name}")

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print("Usage: python code-to-image.py <code_file> [output_path]")
        sys.exit(1)

    input_file = args[0]
    output_file = args[1] if len(args) > 1 else None

    code_to_image(input_file, output_file)
