# latexmk configuration for the NTCIR-19 AgenticInstruction overview paper.
# Reproduce the PDF with:  cd paper && latexmk
# Clean with:              latexmk -C

$pdf_mode = 1;                 # build with pdflatex
$bibtex_use = 2;               # run bibtex as needed, clean .bbl with -C
@default_files = ('overview-ntcir19-agenticinstruction.tex');
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error -file-line-error %O %S';
