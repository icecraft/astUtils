#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import argparse
from astor.code_gen import SourceGenerator, set_precedence
from astor.string_repr import pretty_string
from astor.source_repr import pretty_source
import os
import sys

__all__=['to_source']

"""
the version of astor must be
__version__ = '0.6'
"""

def to_source(node, indent_with=' ' * 4, add_line_information=False,
                            pretty_string=pretty_string, pretty_source=pretty_source):

        generator = NoDocSourceGenerator(indent_with, add_line_information,
                                pretty_string)
        generator.visit(node)
        generator.result.append('\n')
        return pretty_source(str(s) for s in generator.result)

class NoDocSourceGenerator(SourceGenerator):

    def visit_Expr(self, node):
            if isinstance(node.value, ast.Str):
                    self.newline()
                    return
            super(NoDocSourceGenerator, self).visit_Expr(node)

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("--verbosity", help="increase output verbosity")
        parser.add_argument("--output", action="store", dest="output", default="noComent",
                            help="output directory")
        parser.add_argument("--input", nargs='*', dest='inputs', default=None, \
                             action="store", help="the input file or directory names")
        args = parser.parse_args()

        """
        with open('tt.py') as f:
                contents = f.read()

        cc = ast.parse(contents, filename='tt.py')
        print to_source(cc)
        """
        if os.path.exists(args.output):
                print >> sys.stderr, "%r already exists! " % args.output
                sys.exit(1)
        else:
             os.mkdir(args.output)

        def convert_file(rootdir, inputfile):
                if os.path.isfile(os.path.join(rootdir, inputfile)) and \
                   ".py" in inputfile[-3:] :
                   with open( os.path.join( args.output, rootdir, inputfile), "aw") as ofd:
                           with open(os.path.join(rootdir,inputfile)) as ifd:
                                   contents = ifd.read()
                           file_to_ast = ast.parse(contents, filename=inputfile)
                           ofd.write( to_source(file_to_ast))

        def convert_dirs(dirname):
                 for root, dirs, files in os.walk(dirname):
                       if not os.path.exists( os.path.join( args.output, root)):
                                os.mkdir( os.path.join( args.output, root))
                       for filename in files:
                                convert_file(root, filename)
        try :                        
                for inputf in args.inputs:
                        if os.path.isfile(inputf):
                                convert_file("", inputf)
                        else:
                                convert_dirs(inputf)
        except Exception as e:
                                print e
                                


                                
    
