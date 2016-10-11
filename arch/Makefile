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
		-M "lstPrefix=Listing" \
		-V lang=de-DE \
		--chapters \
		-A tex/statement.tex \
		--highlight-style tango \
		-o pdf/thesis.tex \
		*.md
	sed -i 's/\\label{lst:/\\label[Listing]{lst:/g' pdf/thesis.tex
	cd pdf && latexmk -pdf thesis.tex

final: all
	gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dQUIET -dBATCH -sOutputFile=thesis.pdf pdf/thesis.pdf


html:
	pandoc \
		--toc \
		--filter pandoc-fignos \
		--filter pandoc-tablenos \
		--filter pandoc-crossref \
		--smart \
		--bibliography thesis.bib \
		--csl tex/acm.csl \
		-B  ../common/html/template.html \
		-N \
		-S \
		--highlight-style tango \
		-V lang=de-DE --chapters \
		*.md \
		-o html/thesis.html

.PHONY: html
