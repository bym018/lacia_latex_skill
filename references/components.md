# 组件清单

所有环境由 `lacia.sty` 提供，三个版本通用。

| 环境/命令 | 用途 | 颜色 |
|---|---|---|
| `\begin{overview}` | 章概述，置于 `\chapter` 之后；上下细线夹着正文 | Violet 抬头 |
| `\begin{keypoint}` | 关键点：值得记住的结论、判断方法 | Violet |
| `\begin{pitfall}` | 易错：手算或编程最容易错的地方 | Rose |
| `\begin{errata}` | 勘误：原始资料的错误及修正 | Coral |
| `\begin{supp}` | 补充：超出主线的内容 | Teal |
| `\begin{code}{文件名}` | VS Code 风格代码块：标签栏 + 行号栏，默认语言 C | 语法色见 palette.md |
| `\tm{...}` | 行内代码/标识符 | Violet 等宽 |
| `\lth{...}` | 表头单元格 | Pale 底 + Deep 字 |
| `\LaciaNewSym` 等 | 符号登记（`lacia-symbols.sty`，写在 `symbols.tex`），见 `symbols.md` | — |
| `\nonote{\宏}` | 正在定义符号处：不加旁注，算作本节已出现 | — |
| 旁注 | 每节首次出现的登记符号，右页边自动给出 | 符号 Violet，释义 Muted |
| `\LaciaSymbolTable` / `\LaciaSymbolSection{组}` | 由登记表生成符号表附录 | 表头同 `\lth` |

## 用法要点

- `code` 环境改语言：`\begin{code}[listing options={language=Python}]{demo.py}`，右上角标签用 `\renewcommand{\LaciaLang}{Python}`。
- 表格用 `booktabs`（`\toprule \midrule \bottomrule`），表头每格套 `\lth{}`，不画竖线。
- 列表用 `itemize` / `enumerate`，符号已设为 Violet。
- 色块内可以有多段与公式，但不可跨页；过长就拆。
- 标题层级：`\chapter`（章）、`\section`、`\subsection`；章号 Violet，标题 Deep。
