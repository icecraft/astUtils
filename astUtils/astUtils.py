#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
try:
    from astor.code_gen import SourceGenerator
except:
    print 'The Version of astor must equal or greater than 0.6'
from astor.string_repr import pretty_string
from astor.source_repr import pretty_source
import os
from functools import partial
from shutil import copyfile
import _ast
from autopep8 import fix_file
from .utils import _safe_do
    
"""
the version of astor must be
__version__ = '0.6'
"""


def pep8_format(fn):
    contents = fix_file(fn)
    with open(fn, 'w') as f:
        f.write(contents)
    
        
def convert_file(sf, df, func):
    with open(df, "aw") as ofd, open(sf, 'r') as ifd:
        ast_node = ast.parse(ifd.read(), filename=sf)
        ofd.write(func(ast_node))
    pep8_format(df)
    
                           
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
                    _safe_do(copyfile, _spath(fn), _dpath(fn))


class NoDocGenerator(SourceGenerator):

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str):
            self.newline()
            return
        super(NoDocGenerator, self).visit_Expr(node)


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





                                
    
