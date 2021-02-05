import ast
import json
import builtins

from IPython.core.magic import register_cell_magic


class DummyImport(object):
    def __init__(self, name, source):
        self.__source = source
        self.__name = name

    def __resolve_import__(self):
        exec(self.__source, globals())

    def __dir__(self):
        self.__resolve_import__()
        return eval(f"dir({self.__name})")

    def __getattr__(self, attribute):
        self.__resolve_import__()
        return eval(f"{self.__name}.{attribute}")

    def __call__(self, *args, **kwargs):
        self.__resolve_import__()
        return eval(self.__name)(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return f"Lazy loaded import for '{self.__source}'"


@register_cell_magic
def lazyimport(line, cell):
    modules = {}
    
    for node in ast.iter_child_nodes(ast.parse(cell)):
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            for name in [n.asname or n.name for n in node.names]:
                source = ast.get_source_segment(cell, node)
                setattr(builtins, name, DummyImport(name, source))
                modules[name] = source
        else:
            raise RuntimeError(f'Unrecognized import: "{source}"')
            
    if 'debug' in line.lower():
        print("Lazily imported packages are (name -> import statement):")
        print(json.dumps(modules, indent=2))
