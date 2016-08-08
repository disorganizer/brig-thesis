all:
	pandoc \
		--filter pandoc-fignos \
		--filter pandoc-tablenos \
		--filter pandoc-crossref \
		--smart \
		--number-sections \
		--bibliography thesis.bib \
		--csl tex/ieee.csl \
		-H tex/vars.tex \
		-H tex/header.tex \
		-B tex/title.tex \
		-N \
		-V lang=de-DE \
		--chapters \
		-A tex/statement.tex \
		--highlight-style tango \
		-o pdf/thesis.tex \
		*.md

	cd pdf && latexmk -pdf thesis.tex

html:
	pandoc \
		--toc \
		--filter pandoc-fignos \
		--filter pandoc-tablenos \
		--filter pandoc-crossref \
		--smart \
		--bibliography thesis.bib \
		--csl tex/ieee.csl \
		-B  ../common/html/template.html \
		-N \
		-S \
		--highlight-style tango \
		-V lang=de-DE --chapters \
		*.md \
		-o html/thesis.html

.PHONY: html
