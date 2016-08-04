# -*- coding: utf-8 -*-
import click
import os
from astUtils.utils import _safe_do
from astUtils import convert_file, convert_dirs
import warnings


noComment = lambda node: to_source(NoDocGenerator, node)
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

            convert_dirs(fn, outputd,
                         ast_func[op])

        else:
            warnings.warn("Invalid file name %s" % fn)
                



