#!/bin/sh

python plot_speed.py
for path in *.svg; do
	inkscape ${path} --export-pdf=${path%.svg}.pdf
done
