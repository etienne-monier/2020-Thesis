# -*- coding: utf-8 -*-

import pathlib
import re

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


grammar = Grammar(
    r"""
    expr        = (commentary / entry / emptyline)*
    entry       = type lpar key sep ws pair+ rpar

    type        = "@" word
    key         = word
    pair        = tag equal value sep? ws+

    tag         = word+
    value       = (word / quoted / quoted_bis)+

    word        = ~r"[\w&]+"
    text        = ~r"[^\n]*"

    quoted      = ~'{([^{}]*|{[^{}]*})*}'
    quoted_bis  = ~'".*"(?=( )*,\s*)'
    equal       = ws? "=" ws?

    lpar        = "{"
    rpar        = "}"
    sep         = ","
    commentary  = ~"\s*%[^\n]*"
    ws          = ~"\s*"
    emptyline   = ws+
    """
)


class IniVisitor(NodeVisitor):
    def visit_expr(self, node, visited_children):
        """ Returns the overall output. """
        output = {}
        for child in visited_children:
            if isinstance(child[0], dict):
                output.update(child[0])
        return output

    def visit_entry(self, node, visited_children):
        """ Makes a dict of the section (as key) and the key/value pairs. """
        key = visited_children[2].text
        return {key: node.text}

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node


if __name__ == '__main__':

    proj_dir = pathlib.Path(__file__).parent.parent

    # Get list of keys
    #
    bbl_file = proj_dir / 'build' / 'main.bbl'

    with open(bbl_file, 'r') as file:
        content = file.read()

    # Set match pattern.
    p = re.compile('bibitem{(\w+)}')

    # Scan lines
    res = p.findall(content)

    # Get References
    #
    bib_file = proj_dir / 'bib' / 'biblio.bib'

    # Read content
    with open(bib_file, 'r') as file:
        content = file.read()

    # Parsing file
    tree = grammar.parse(content)
    iv = IniVisitor()
    output = iv.visit(tree)

    # Print output
    #
    new_bib = ''
    for cnt, key in enumerate(res):
        new_bib += '% Publi #{}\n{}\n\n'.format(cnt+1, output[key])
        output.pop(key)

    if output != {}:
        new_bib += "\n%% Non-used part\n%%\n%%\n\n"
        for cnt, value in enumerate(output.values()):
            new_bib += '% Supp #{}\n{}\n\n'.format(cnt+1, value)

    # Save output
    bib_out_file = proj_dir / 'bib' / 'biblio_out.bib'

    # Read content
    with open(bib_out_file, 'w') as file:
        content = file.write(new_bib)
