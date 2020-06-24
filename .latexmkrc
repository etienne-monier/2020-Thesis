#
# Manuscript .latexmk file
# 


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



# Custom dependencies ##################################################

sub path_decompose {
    # Get absolute file name
   $abs_path = File::Spec->rel2abs( $_[0] );
   
   # Separate abs. path name into directory and file name.
   ($vol, $dir, $fname) = File::Spec->splitpath($abs_path);

   return ($vol, $dir, $fname)
}


# Tikz dependencies. ########################

add_cus_dep('tikz', 'pdf', 0, 'tikz2pdf');

sub tikz2pdf {
    # Decompose path
    ($vol, $dir, $fname) = path_decompose($_[0]);

    # Converts file.
    system( "pdflatex --output-directory \"$dir\" \"$abs_path.tikz\"" );
}

# Glossaries dependencies ###################

add_cus_dep('glo', 'gls', 0, 'glo2gls');
add_cus_dep('acn', 'acr', 0, 'glo2gls');

add_cus_dep("slo1", "sls1", 0, 'glo2gls');
add_cus_dep("slo2", "sls2", 0, 'glo2gls');
add_cus_dep("slo3", "sls3", 0, 'glo2gls');
add_cus_dep("slo4", "sls4", 0, 'glo2gls');
add_cus_dep("slo5", "sls5", 0, 'glo2gls');
add_cus_dep("slo6", "sls6", 0, 'glo2gls');
add_cus_dep("slo7", "sls7", 0, 'glo2gls');
add_cus_dep("slo8", "sls8", 0, 'glo2gls');
add_cus_dep("slo9", "sls9", 0, 'glo2gls');
add_cus_dep("slo10", "sls10", 0, 'glo2gls');

sub glo2gls {
    # Decompose path
    ($vol, $dir, $fname) = path_decompose($_[0]);
    
    # run makeglossaries
    if ( $silent ) {
        system("makeglossaries -q -d $out_dir '$fname'");
    }
    else {
        system("makeglossaries -d $out_dir '$fname'");
    };
}
