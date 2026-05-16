# 项目格式参考

## 产物结构

完整的 Mindmap PPT 产物是一个零依赖静态文件夹：

```text
<输出目录>/
├── index.html
├── src/
│   ├── main.js
│   └── styles.css
└── project/
    ├── source.js
    └── <本地图片资源>
```

直接用浏览器打开 `index.html` 即可预览。

## 静态播放器模板

播放器文件已随 skill 内置：

```text
assets/static-template/index.html
assets/static-template/src/main.js
assets/static-template/src/styles.css
assets/static-template/project/source.js
```

新建 mindmap-ppt 时，先复制播放器模板，再用生成内容替换 `project/source.js`。更新已有 mindmap-ppt 时，除非用户要求刷新播放器，否则只编辑 `project/source.js` 和图片资源。

## `project/source.js`

使用这个结构：

```js
window.sourceMarkdown = `
- Markdown Mindmap
  项目汇报思维导图演示
  @image overview.png
    - 需求分析
      用户目标与演示场景
`;
```

解析规则：

- 匹配 `- text` 的行会创建节点。
- 缩进的连续行会追加到当前节点标签中。
- `@image path` 会给当前节点附加一张图片，并且不会显示为节点文字。
- 短图片路径如 `overview.png` 会解析为 `./project/overview.png`。
- 嵌套短路径如 `image-asset-1/a.jpg` 会解析为 `./project/image-asset-1/a.jpg`。
- 以 `./`、`../`、`/`、`http:`、`https:` 或 `data:` 开头的显式路径会原样使用。
- 同一节点出现多行 `@image` 时，最后一行生效。
- 整棵树按 preorder 遍历。

## 节点文字

两行节点约定：

- 第一行：副标题/分类，显示为较小文字。
- 第二行：主标题，显示为普通标题文字。

单行节点只显示为标题。

控制区读数会把多行标签折叠成 `副标题 / 主标题`。

## 图片行为

图片显示在节点卡片内部：

- 选中的图片节点：文字下方显示展开图片。
- 未选中的图片节点：文字下方显示缩略图。
- 没有图片的节点：不预留图片空间。

支持浏览器 `<img>` 能加载的 PNG、JPG/JPEG、SVG 等格式。

## 交互

- 上下方向键、Page Up/Page Down、滚轮和顶部按钮按 preorder 切换节点。
- 进度滑条跳转到指定序号。
- Zoom 滑条缩放画布。
- 点击可见节点只平移镜头，不改变选中节点，也不展开该节点图片。