"""
代码片段转图片脚本
用法: python code-to-image.py <代码文件> [输出路径]

默认使用 monokai 主题
"""

import sys
from pathlib import Path
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name

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
    formatter = ImageFormatter(
        font_name='Consolas',  # Windows 下更清晰的等宽字体
        font_size=16,          # 稍大一点更清晰
        line_numbers=False,
        line_pad=4,            # 行间距
        image_pad=24,          # 边距
        style=style,
    )

    with open(output_path, "wb") as f:
        f.write(highlight(code, lexer, formatter))

    print(f"[OK] Generated: {output_path}")

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print("Usage: python code-to-image.py <code_file> [output_path]")
        sys.exit(1)

    input_file = args[0]
    output_file = args[1] if len(args) > 1 else None

    code_to_image(input_file, output_file)