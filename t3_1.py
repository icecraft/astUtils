from astor.code_gen import SourceGenerator
from astor.string_repr import pretty_string
from astor.source_repr import pretty_source


def to_source(node, indent_with=' ' * 4, add_line_information=False,
              pretty_string=pretty_string, pretty_source=pretty_source):
    
    generator = NoDocSourceGenerator(indent_with, add_line_information,
                                     pretty_string)
    generator.visit(node)
    generator.result.append('\n')
    return pretty_source(str(s) for s in generator.result)

 
class NoDocSourceGenerator(SourceGenerator):
    def decorators(self, node, extra):
        self.result.append('@cc')
        for decorator in node.decorator_list:
            self.statement(decorator, '@', decorator)

        
        
