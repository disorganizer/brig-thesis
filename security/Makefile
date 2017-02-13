all:
	pandoc \
		--filter pandoc-fignos \
		--filter pandoc-tablenos \
		--metadata link-citations \
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
		--top-level-division=chapter \
		-A tex/statement.tex \
		--highlight-style tango \
		-o pdf/thesis.tex \
		*.md

	cd pdf && latexmk -silent -pdf thesis.tex

title:
	latexmk -pdf tex/hsa-title.tex -output-directory=pdf

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

bench:
	./scripts/plot.py ./scripts/aesni-impact.json
	./scripts/plot.py ./scripts/keygenoverhead-profile.json
	./scripts/plot.py ./scripts/low-end-performance.json
	./scripts/plot.py ./scripts/read-performance-blocksize.json
	./scripts/plot.py ./scripts/write-performance-blocksize.json

.PHONY: html
