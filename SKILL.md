---
name: lacia-notes
description: 用 Lacia Pale Periwinkle 版式生成独立使用的 LaTeX/xelatex 学习讲义（中文，ctexbook）。当用户要求制作、重排、改写课程讲义、复习笔记、知识整理类 PDF，或提到 Lacia 模板、亮色/暗色讲义时使用。包含模板本体、内容编排规则与限制。
---

# lacia-notes

用统一的版式与配色，把课程资料整理成**独立使用**的 PDF 讲义。模板本体在 `assets/template/`，内容编排规则在下面和 `references/`。

## 工作流

1. 把 `assets/template/` 整个复制到用户指定的工作目录（不要原地编译，不要改动 skill 目录）。
2. 先读 `references/content-rules.md`，在动笔前确定每章的结构与概述写法。
3. 改 `main.tex` 的标题、`\LaciaHeadLText`、`\hypersetup{pdftitle=...}`；删掉示例章节 `chapters/01-binary-search.tex`，按需新增 `chapters/NN-xxx.tex` 并在 `main.tex` 里 `\input`。
4. 重写 `chapters/00-howto.tex`（"如何使用这份讲义"），内容见规则第 1 条。
5. `make all` 一次出三版；只要一版就 `make light` / `make dark` / `make violet`。
6. 编译后必须检查：无 LaTeX 报错、无溢出到版心外的行、色块没有孤标题、目录与页眉正确。看渲染后的页面，不要只看日志。

## 版本

| 选项 | Makefile 目标 | 用途 |
|---|---|---|
| `light` | `make light` | 亮色版，屏幕与打印共用；页面纯白不铺底色 |
| `dark` | `make dark` | 暗色·深冰蓝 |
| `darkpurple` | `make violet` | 暗色·紫墨 |

三版排版与组件完全相同，只有 `lacia-palette-*.def` 不同。

## 内容规则（限制）

这些是硬性要求，生成内容时逐条自查，违反即重写。完整说明与反例见 `references/content-rules.md`。

1. **封面只放标题。** 大标题下不放副标题、关键词串、流程示意条；整份讲义的概览写进"如何使用这份讲义"一节。允许在概览节中作图。
2. **不写无用文字。** 不出现"依据某日期整理"、"配色：xxx"、"另有暗色版"、"以 N 份资料重制"之类制作说明或自我介绍。
3. **必须独立成立。** 正文不得引用外部文件、脚本路径、示例链接、"课件原图"等读者手里没有的东西。需要的内容直接写进讲义。
4. **每章概述可选，写就写完整。** 用 `overview` 环境，必须说清：上一阶段的做法、它的局限、本章换了什么、读完能做什么。不得只放关键词或一张图。允许在概览节中作图。
5. **色块克制使用。** 一页内同类色块不连放；不要为了装饰加色块。四种色块各有固定语义，不得混用（见 `references/components.md`）。
6. **不自造颜色。** 只使用 `LaciaXxx` 调色板里的颜色；需要新语义先改调色板文件，三版同步。

## 技术限制

- 编译器：**xelatex**（`ctexbook`）。不要换成 pdflatex。
- 依赖字体：Noto Serif/Sans/Sans Mono CJK SC、DejaVu Sans Mono。缺字体时先告知用户，不要静默替换。
- 代码块 `code` 环境基于 `listings`，**不要**加载 `lstlinebgrd`（与本机 listings 版本冲突，会让整份文档编译崩溃）。
- 四种色块不可跨页（避免孤标题）；单个色块过长时拆成两个或改为普通段落。
- `lacia.sty` 里超链接颜色写作 `LaciaViolet!100`，这是绕过一个未查明根因的 `LACIAVIOLET` 报错的写法，不要改回去。
- 不要修改 `lacia.sty` 的组件定义来"凑合"某段内容；需要新组件先和用户确认。

## 文件地图

- `assets/template/lacia.sty` 模板本体；`lacia-palette-*.def` 三套配色
- `assets/template/main.tex`、`chapters/`、`Makefile` 可直接复制使用的骨架与示例
- `references/content-rules.md` 内容规则全文与反例
- `references/components.md` 组件清单与用法
- `references/palette.md` 色值、对比度与设计决策
