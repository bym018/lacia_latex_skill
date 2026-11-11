# 符号登记表、旁注与符号表（lacia-symbols）

读者常跳着读，会忘记 $\overset{+}{\Rightarrow}$、$\mathrm{PS}$、项目圆点这类专用记号的含义。这个组件做三件事：

1. **旁注**：每节第一次出现带旁注的符号时，在右页边给出极短释义；
2. **符号表**：附录里的符号表从登记表自动生成，不手写；
3. **检查**：`symcheck.py` 扫描正文，报告漏登记、裸写和一符多义。

分工原则：**登记表保真，宏易用，检查保全面。**三者不要合并成“自动识别符号再自动加注”。

## 文件

| 文件 | 作用 |
|---|---|
| `lacia-symbols.sty` | 组件本体；在 `lacia.sty` 之后加载 |
| `symbols.tex` | 本讲义的登记表，旁注和符号表的唯一来源 |
| `symcheck.py` | 检查脚本，只报告不修改；`make symcheck`，`make all` 会先跑它 |
| `symcheck-ignore.txt` | 检查的忽略表 |

## 登记表写法

```latex
\LaciaSymGroup{grammar}{文法与推导（第 2 章）}        % 组 = 符号表的一节，按声明顺序输出

% 带宏：正文用 \dstar；第 6 个参数非空才有旁注
\LaciaNewSym{\dstar}{dstar}{grammar}
  {\overset{*}{\Rightarrow}}                         % 宏的排版内容
  {\alpha\overset{*}{\Rightarrow}\beta}              % 符号表/旁注里的展示形式，空 = 同上
  {0 步或多步}                                        % 旁注短释义，空 = 不加旁注
  {经过 0 步或多步推导得到 $\beta$；0 步时 $\alpha=\beta$}   % 符号表长释义

% 不带宏，只进符号表（正文照常裸写，如 \mathrm{GEN}[B]）
\LaciaSymEntry{genB}{flow}{\mathrm{GEN}[B]}{基本块 $B$ 内产生、并能到达块出口的定值}

% 一符多义：正文裸写时 symcheck 报 C 类，要求人工判断
\LaciaSymWatch{\Rightarrow}{一步推导改用 \derive；推出/变换改用 \imp}
```

- 同一个记号的短释义、长释义写在同一条里，改一处全书同步。
- 短释义要能放进约 6 个汉字宽的页边：箭头本身已表示“推导”，释义只写“0 步或多步”“最右推导 1 步”。
- 有名字的集合（First、Follow）通常只进表不加旁注，否则页边过密。
- 已有的同名宏（如 `\eps`、`\First`）要从 preamble 里删掉，改由登记表定义。

## 正文写法

- 专用记号一律用登记过的宏，不裸写。
- **正文正在定义这个符号的地方**用 `\nonote{\dplus}`：不加旁注，但算作本节已出现。
- 不提供 `\dplus*` 写法：正文常有 `T\dq*F` 这种紧跟乘号的写法，星号语法会把乘号吞掉。
- **一符多义**拆成不同的宏，各自登记、在表里并列说明区别。例：$\Rightarrow$ 拆成 `\derive`（直接推导）与 `\imp`（推出、变换为）；字形相同，含义不同。
- 符号宏是 robust 命令；若出现在 `\section` 标题里，用 `\pdfstringdefDisableCommands{\def\eps{ε}}` 给书签一个文本替身。

## 附录

```latex
\appendix
\chapter{符号表}
（一两句说明旁注和本表的关系）
\LaciaSymbolTable                 % 输出全部组
% 或逐组输出，组间可插手写段落（如“字母约定”）：
\LaciaSymbolSection{grammar}
\textbf{字母约定。}……
\LaciaSymbolSection{regular}
```

展示列宽默认 30mm（`\renewcommand\LaciaSymbolColumnWidth{..}`）。展示形式太宽会溢出：缩短写法（`\mathrm{enter}(n,o)`）或拆成两条，不要加宽列。

## symcheck 报告的四类

| 类 | 含义 | 处理 |
|---|---|---|
| A 裸写 | 已登记带宏的符号被直接写出 | 改用宏，否则没有旁注 |
| B 未登记 | 像记号的写法（`\mathrm{Name}(`/`[`、`\overset{..}{\cmd}` 等）出现 ≥N 次但没登记 | 读上下文后登记（释义从正文定义里取，不要编）；关键字之类加入忽略表 |
| C 歧义 | `\LaciaSymWatch` 的记号被裸写 | 逐处判断含义，换成对应的宏 |
| D 未使用 | 登记了但正文没用 | 删掉或保留（例如为了表的完整性）；取不到辨识特征的条目不判 |

交付前要求 A、C 为 0；B 用 `--min 1` 再看一遍单次出现的。`--strict` 时 A/C 非空返回 1，可接进构建。

忽略表一行一个；`re:` 开头的按正则整体匹配（规范化去空白后）。`\overset{(3)}{\Rightarrow}` 这类单字符参数的变体与登记的 `\overset{(k)}{\Rightarrow}` 视为同一记号。

## 技术说明与限制

- **原理**：符号处只把（页, 纵坐标）写进 aux，下一轮在 shipout 前景层统一画出。所以在色块、表格、TikZ 结点、公式里都能用，旁注不占版面、不改变分页。
- **必须编译到 aux 稳定**：用 latexmk。固定跑两遍不够（第二遍加目录后页码会移动）。只跑一遍时旁注缺失或错位。
- **改了 aux 记录格式**（升级本组件后）先 `make clean`，旧 aux 会导致报错。
- **页边**：旁注从版心右缘外 2.5mm 起，宽度自动取到纸边 3.5mm 为止；右页边小于约 20mm 时会警告。打印时离纸边近，可能被不可打印边距裁掉。
- **避让**：同页两条相撞时后一条下移，可能和对应行错开一两行。
- **范围**：`\mainmatter` 后开启、`\appendix` 后关闭；没有 `\mainmatter` 的文档类（ctexart）全程开启。按“章.节”区分，`\subsection` 不重新计数。
- **不要**：从正文自动猜符号含义（正则或 LLM 都会把错误含义印在页边）；每次出现都加旁注。
