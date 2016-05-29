#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from astor.code_gen import SourceGenerator
from astor.string_repr import pretty_string
from astor.source_repr import pretty_source
import os
import click
import warnings
from functools import partial
from shutil import copyfile
import _ast


"""
the version of astor must be
__version__ = '0.6'
"""


def _safe_do(func, *args):
    try:
            return func(*args)
    except:
            return None


def convert_file(sf, df, func):
    with open(df, "aw") as ofd, open(sf, 'r') as ifd:
        ast_node = ast.parse(ifd.read(), filename=sf)
        ofd.write(func(ast_node))

                           
def convert_dirs(ind, outd, func):
    for root, dirs, files in os.walk(ind):
        _dpath = partial(os.path.join, outd, root)
        _spath = partial(os.path.join, root)
        _safe_do(os.makedirs, _dpath())
        for fn in files:
                try:
                    convert_file(_spath(fn),
                                 _dpath(fn), func)
                except:
                    copyfile(_spath(fn),
                             _dpath(fn))
                                

class NoDocSourceGenerator(SourceGenerator):

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str):
            self.newline()
            return
        super(NoDocSourceGenerator, self).visit_Expr(node)


class decoWrapGenerator(SourceGenerator):
        
    def visit_Module(self, node):
        self.result.append('\nfrom decoUtils import *')
        self.write(*node.body)
        
    def decorators(self, node, extra):
        if node.__class__ is _ast.FunctionDef:
            self.result.append('\n@logWrap')
        else:
            self.result.append('\n@methodWrap')
            
        for decorator in node.decorator_list:
            self.statement(decorator, '@', decorator)
        
        
def to_source(implclass, node, indent_with=' ' * 4, add_line_information=False,
              pretty_string=pretty_string, pretty_source=pretty_source):

    generator = implclass(indent_with, add_line_information,
                          pretty_string)
    generator.visit(node)
    generator.result.append('\n')
    return pretty_source(str(s) for s in generator.result)


noComment = lambda node: to_source(NoSourceGenerator, node)
decoWrap = lambda node: to_source(decoWrapGenerator, node)


ast_func = {'noComment': noComment,
            'decoWrap': decoWrap}
            
            
@click.command()
@click.option('--inputf', '-m', multiple=True,
              help='input files or directory')
@click.option('--outputd', default='Converted',
              help='output directory')
@click.option('--op', type=click.Choice(['noComment', 'decoWrap']),
              default='noComment', help='choose the operation')
def run_args(inputf, outputd, op):
    if not os.path.exists(outputd):
            os.mkdir(outputd)
    for fn in inputf:
        if os.path.isfile(fn) and ".py" in fn[-3:]:
            _safe_do(os.remove, os.path.join(outputd,
                                             fn))
        
            convert_file(fn, os.path.join(outputd, fn),
                         ast_func[op])

        elif os.path.isdir(fn):
            _safe_do(os.rmdir, os.path.join(outputd,
                                            fn))

            convert_dirs(fn, os.path.join(outputd, fn),
                         ast_func[op])

        else:
            warnings.warn("Invalid file name %s" % fn)
                

if __name__ == '__main__':
        run_args()



                                
    
