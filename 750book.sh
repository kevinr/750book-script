#!/bin/bash

# Takes one or more 750 Words export files as input, generates a PDF file as output.
# Output file is named after the first input file.
# Usage: 750book.sh INPUT1 [INPUT2 ..]

TEXFILE=`basename "$1" .txt`.tex

touch "$TEXFILE"
./750book-latex.py "$@" > "$TEXFILE"
echo "Updating the TOC file"
pdflatex "$TEXFILE"
echo "Final render!"
pdflatex "$TEXFILE"
