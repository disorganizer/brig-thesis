all:
	pandoc \
		--filter pandoc-fignos \
		--filter pandoc-tablenos \
		--smart \
		--bibliography thesis.bib \
		--csl tex/ieee.csl \
		-B tex/title.tex -H tex/header.tex -N \
		-o pdf/thesis.tex -V lang=de-DE --chapters \
		-A tex/statement.tex \
		*.md

	cd pdf && latexmk -pdf thesis.tex
