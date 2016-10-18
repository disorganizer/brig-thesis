#!/bin/bash

find ../images -type f -iname '*.png' -o -iname '*.pdf' | while read path; do
	new_path=${path:3}
	parent=$(dirname $new_path)

	echo "Creating parent dir $parent, $new_path, $path"
	mkdir -p $parent
	if [ ${path: -4} == ".pdf" ]; then
		echo "Converting $path to ${new_path%.*}.png"
		inkscape --without-gui $path --export-png=${new_path%.*}.png --export-dpi 150
	else
		echo "Copying $path to $new_path"
		cp $path $new_path
	fi
done

# Fix pdf references:
sed -i 's#images/\(.*\).pdf#images/\1.png#g' thesis.html

# Get rid of <embed>
sed -i 's#<embed #<img #g' thesis.html

# Add title image:
inkscape --without-gui ../images/title.pdf --export-png=title.png -d 150
sed -i 's#^true$#<img src="title.png" />#g' thesis.html
