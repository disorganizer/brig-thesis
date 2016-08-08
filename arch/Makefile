all:
	pandoc \
		--filter pandoc-fignos \
		--filter pandoc-tablenos \
		--filter pandoc-crossref \
		--smart \
		--number-sections \
		--bibliography thesis.bib \
		--csl tex/ieee.csl \
		-B tex/title.tex -H tex/header.tex -N \
		-o pdf/thesis.tex -V lang=de-DE --chapters \
		-A tex/statement.tex \
		--highlight-style tango \
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
		-B  html/template.html \
		-N \
		-S \
		--highlight-style tango \
		-V lang=de-DE --chapters \
		*.md \
		-o html/thesis.html

.PHONY: html
