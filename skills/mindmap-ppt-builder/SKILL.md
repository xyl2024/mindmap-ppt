---
name: mindmap-ppt-builder
description: 根据提供的资料生成思维导图式的交互式演讲稿（mindmap-ppt），以静态网页提供产物。
---

# Mindmap PPT 生成器

## 目标

生成一个可以直接双击打开的静态思维导图 PPT。完整产物包含：

- `index.html`：静态页面外壳。
- `src/main.js` 和 `src/styles.css`：内置播放器 UI、布局、动画和交互。
- `project/source.js`：用 `window.sourceMarkdown` 保存的 Markdown 导图内容。
- `project/`：由 `@image` 引用的本地图片资源。

用户可以双击 `index.html` 预览。后续只修改内容时，保留播放器文件，只更新 `project/source.js` 和必要的 `project/` 资源。

只有在需要确认精确语法或图片路径规则时，才读取 `references/project-format.md`。

## 内置静态模板

本 skill 已在 `assets/static-template/` 内置可复制的播放器模板。

推荐在 skill 目录中运行脚手架命令：

```bash
python scripts/scaffold.py <输出目录>
```

可选参数：

- `--overwrite-app`：用内置模板刷新 `index.html`、`src/main.js` 和 `src/styles.css`。
- `--overwrite-source`：用占位内容替换 `project/source.js`；更新已有 mindmap-ppt 时不要使用，除非用户要求重置。

如果不能运行脚本，就手动复制：

- `assets/static-template/index.html` -> `<输出目录>/index.html`
- `assets/static-template/src/` -> `<输出目录>/src/`
- `assets/static-template/project/source.js` -> `<输出目录>/project/source.js`，仅新建 mindmap-ppt 时复制

## 工作区规则

- 只在当前目录或用户明确指定的输出目录内工作。
- 新建 mindmap-ppt ：先从 `assets/static-template/` 创建或刷新播放器文件，再写入 `project/source.js` 和图片资源。
- 更新已有 mindmap-ppt ：如果 `index.html`、`src/main.js`、`src/styles.css` 已存在，除非用户要求更新播放器，否则不要改这些文件；只修改 `project/source.js` 和 `project/` 资源。
- 不要删除已有 `project/` 资源，除非用户明确要求清理。

## 工作流程

1. 判断任务类型：
   - 新建 mindmap-ppt ：目录中没有 `index.html`，或用户要求生成完整 PPT 产物。
   - 更新 mindmap-ppt ：播放器文件已存在，或用户要求修改已有内容。
2. 获取原始材料：
   - 优先使用对话中粘贴的文本。
   - 如果用户提供本地文件路径，只读取该文件。
   - 如果没有文本也没有可读取文件，先向用户索要材料。
3. 新建 mindmap-ppt 时，用 `scripts/scaffold.py` 或手动复制 `assets/static-template/`，把静态播放器放入输出目录。
4. 阅读材料并提炼主线：
   - 默认跟随原文语言：中文输入 -> 中文输出；英文输入 -> 英文输出。
   - 谨慎保留事实；发现明显矛盾时说明问题，不要悄悄改写。
   - 材料很长时，优先保留原有章节结构。
5. 构建清晰的 preorder 逻辑树：
   - 根节点：材料标题或主题。
   - 主分支：通常 2-4 个部分，但以材料逻辑为准。
   - 子节点：原因、证据、例子、流程步骤、对比、风险或补充。
   - 只有在能增强理解时才增加层级。
6. 按以下格式写入 `project/source.js`：

```js
window.sourceMarkdown = `
- 副标题
  主标题
    - 分支
      关键观点
`;
```

把用户文本写入 JavaScript 模板字符串前，必须转义反引号和 `${...}` 序列。

7. 谨慎选择配图节点：
   - 图片是可选的。
   - 通常选择 3-8 个信息密度高的节点；短材料可以 0-2 个。
   - 优先给框架、对比、流程、时间线、架构、清单、建议或风险模型节点配图。
8. 在 `project/` 或其子目录下创建/生成本地插图：
   - 生成式位图优先用 PNG。
   - 简单图解优先用 SVG。
   - 照片类素材可用 JPG。
   - 如果无法生成图片，需要配图时可创建克制风格的 SVG 占位图。
9. 图片元数据写在节点可见标签之后、子节点之前：

```md
  @image diagrams/process-overview.svg
```

10. 结束前检查：
    - 完整的 mindmap-ppt 必须包含 `index.html`、`src/main.js`、`src/styles.css` 和 `project/source.js`。
    - `project/source.js` 必须给 `window.sourceMarkdown` 赋值，并且模板字符串已闭合。
    - 每个 `@image` 都指向存在的本地资源；明确使用外部链接或 data URL 的情况除外。
    - 不需要 `npm run`、本地服务器或构建步骤；直接用浏览器打开 `index.html` 预览。

## 导图写作规则

- 每个树节点对应一个无序列表 Markdown 条目。
- 优先使用两行标签：第一行是小号副标题/分类，第二行是主标题。
- 每行尽量简洁：中文约 30 字以内，英文约 8 个词以内。
- 单行节点只在标签已经足够短且清楚时使用。
- 遵循原文顺序；播放器按 preorder 展示节点。
- 不要在子节点重复根节点主题；子节点应该推进叙事。
- 把相近含义归到同一父节点下，让背景、标准、风险、建议和结论各自成组。
- 主节点承载判断，子节点承载证据、原因、例子或补充。
- 每个父节点最多 5 个子节点；超过时增加分组节点。
- 工具/产品只有在原文逐一分析时才拆开；如果只是顺带列举，应合并处理。
- 一个节点表达一个完整小观点，不要只是句子碎片，也不要包含多个无关观点。
- 父节点负责概括和导航，子节点负责展开细节。

## Markdown 与图片示例

```js
window.sourceMarkdown = `
- 产品发布
  三分钟讲清楚新功能
  @image overview.png
    - 用户痛点
      当前流程成本很高
      @image image-asset-1/pain-points.jpg
    - 解决方案
      自动整理文稿和插图
    - 演示效果
      像 PPT 一样逐步展开
      @image diagrams/demo-flow.svg
`;
```

图片路径默认相对于 `project/`：

- `@image overview.png` -> `./project/overview.png`
- `@image image-asset-1/pain-points.jpg` -> `./project/image-asset-1/pain-points.jpg`
- `@image diagrams/demo-flow.svg` -> `./project/diagrams/demo-flow.svg`

## 图片风格

生成插图时使用这个提示词：

```text
为浅色 PPT 思维导图节点创建一张干净的演示插图。
主题：<节点核心意思>。
包含：<来自原文的 2-4 个具体视觉元素>。
风格：克制的矢量感编辑插画，暖白背景，深青色 #183a4a，浅绿色 #eef7f3，橙色强调 #d8894f，简单几何形状，轻微阴影，8px 小圆角卡片感，不要照片写实，不要 logo，不要复杂装饰；只有在有助于理解时使用极少量短文字。
构图：居中，留白充足，缩略图尺寸下仍可读，16:10 比例。
```

创建 SVG 占位图时：

- 尺寸用 `1280x800`。
- 暖白背景，深青色 `#183a4a`，浅绿色 `#eef7f3`，橙色强调 `#d8894f`。
- 使用抽象流程块、箭头、卡片、时间线或简单图解。
- 只有在有助于理解时使用极少量短文字。