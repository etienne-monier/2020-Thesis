pwd = $(shell pwd)

.PHONY: all, init, clean

all:
	latexmk -pdf main.tex

# To init style.
init:
	rm -f ~/.texmf/tex/latex/style
	ln -s "$(pwd)/style/" ~/.texmf/tex/latex/

# To clean repository.
clean:
	latexmk -c
