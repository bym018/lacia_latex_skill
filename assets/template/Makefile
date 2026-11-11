# make all：先跑 symcheck，再出三版；make light / dark / violet 单出一版
# 用 latexmk 编译到 aux 稳定（符号旁注依赖上一轮的位置记录，固定两遍不够）
EDS = light dark violet
all: symcheck $(EDS)
symcheck: ; python3 symcheck.py chapters
light:  ; $(call build,light,light)
dark:   ; $(call build,dark,dark)
violet: ; $(call build,darkpurple,violet)
define build
	latexmk -xelatex -interaction=nonstopmode -halt-on-error -jobname=main-$(2) -usepretex='\def\Edition{$(1)}' main.tex >/dev/null 2>&1 && echo "built main-$(2).pdf" || (grep -m5 -A4 "^!" main-$(2).log; false)
endef
clean: ; rm -f *.aux *.log *.out *.toc *.listing *.fls *.fdb_latexmk *.xdv
.PHONY: all symcheck light dark violet clean
