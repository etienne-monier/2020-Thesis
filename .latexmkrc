
# Output files directory.
$out_dir = "build";

# Default file to compile
@default_files = ("main.tex");

# Sets the default behavior to build a pdf with pdflatex.
$pdf_mode = 1;

# Live preview program
$pdf_previewer = "start evince %O %S";  # Linux

# Pdflatex command
$pdflatex = "pdflatex -file-line-error -synctex=1 %O %S";

# Images dependencies.
add_cus_dep('tikz', 'pdf', 0, 'tikz2pdf');
sub tikz2pdf {
   # Get absolute file name
   $abs_path = File::Spec->rel2abs( $_[0] );
   # Separate abs. path name into directory and file name.
   ($vol, $dir, $fname) = File::Spec->splitpath($abs_path);
   # Converts file.
   system( "pdflatex --output-directory \"$dir\" \"$abs_path.tikz\"" );
}

# Nomenclature - Notations
# makeindex main.nlo -s nomencl.ist -o main.nls
add_cus_dep('nlo', 'nls', 0, 'nlo2nls');
sub nlo2nls {
   system("makeindex \"$_[0].nlo\" -s nomencl.ist -o \"$_[0].nls\"")
}
