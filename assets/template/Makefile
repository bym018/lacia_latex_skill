# make light / make dark / make violet ；make all 一次出三版
EDS = light dark violet
all: $(EDS)
light:  ; $(call build,light,light)
dark:   ; $(call build,dark,dark)
violet: ; $(call build,darkpurple,violet)
define build
	xelatex -interaction=nonstopmode -jobname=main-$(2) "\def\Edition{$(1)}\input{main.tex}" >/dev/null && \
	xelatex -interaction=nonstopmode -jobname=main-$(2) "\def\Edition{$(1)}\input{main.tex}" >/dev/null && echo "built main-$(2).pdf"
endef
clean: ; rm -f *.aux *.log *.out *.toc *.listing
