#!/bin/bash

# Takes one or more 750 Words export files as input, generates a PDF file as output.
# Output file is named after the first input file.
# Usage: 750book.sh INPUT1 [INPUT2 ..]

TEXFILE=`basename "$1" .txt`.tex

rm -f "$TEXFILE"
./750book-latex.py "$@" > "$TEXFILE" &&
pdflatex "$TEXFILE" &&
pdflatex "$TEXFILE"
