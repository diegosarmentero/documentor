# -*- coding: utf-8 -*-
#
# This file is part of Documentor
# (https://github.com/diegosarmentero/documentor).
#
# Documentor is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Documentor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Documentor; If not, see <http://www.gnu.org/licenses/>.
import os
import ast
import _ast
import shutil

import docdump

_map_type = {
    _ast.Tuple: 'tuple',
    _ast.List: 'list',
    _ast.Str: 'str',
    _ast.Dict: 'dict',
    _ast.Num: 'int',
    _ast.Call: 'function()',
}


"""Scan each file and generate a representation of the content using AST."""


def get_python_files(path):
    """Return a dict structure containing the info inside a folder."""
    if not os.path.exists(path):
        raise Exception("The folder does not exist")
    d = {}
    for root, dirs, files in os.walk(path, followlinks=True):
        d[root] = [[f for f in files
                if (os.path.splitext(f.lower())[-1]) == '.py'],
                dirs]
    return d


class Analyzer(object):
    """Explore recursively the project folder and scan the info of each file."""

    def __init__(self, project, output, projectname):
        self.project = project
        self.output = output
        self.listings_folder = os.path.join(output, 'listings')
        self.dump = docdump.DocDump(projectname, output)

    def scan(self):
        """Initialize the scan process."""
        self.structure = get_python_files(self.project)
        path = os.path.join(self.project, '')[:-1]
        self.parse_folder(path, '')
        self.dump.create_html_sections()

    def parse_folder(self, folderpath, relpath):
        """Parse the folders and files contained inside folderpath."""
        print('Parsing folder: %s' % folderpath)
        files, folders = self.structure[folderpath]

        for file_ in files:
            filepath = os.path.join(folderpath, file_)
            self.parse_file(filepath, relpath)

        for folder in folders:
            path = os.path.join(folderpath, folder)
            self.parse_folder(path, os.path.join(relpath, folder))

    def parse_file(self, filepath, relpath):
        """Parse the file and create a representation with all the info about:
        - Imports
        - Classes
        - Functions
        - Attributes
        - Decorators
        - etc"""
        print('Parsing file: %s' % filepath)
        codefolder = os.path.join(self.listings_folder, relpath)
        if not os.path.exists(codefolder):
            os.makedirs(codefolder)
        shutil.copy(filepath, codefolder)

        source = ""
        with open(filepath, 'r') as f:
            source = f.read()
        if source:
            symbols = self.obtain_symbols(source, filepath)
            self.dump.process_symbols(symbols, filepath, relpath)

    def obtain_symbols(self, source, filename=''):
        """Parse a module code to obtain: Classes, Functions and Assigns."""
        try:
            module = ast.parse(source)
        except:
            print("The file contains syntax errors: %s" % filename)
            return {}
        symbols = {}
        globalAttributes = {}
        globalFunctions = {}
        classes = {}

        for symbol in module.body:
            if symbol.__class__ is ast.Assign:
                result = self._parse_assign(symbol)
                globalAttributes.update(result[0])
                globalAttributes.update(result[1])
            elif symbol.__class__ is ast.FunctionDef:
                result = self._parse_function(symbol)
                globalFunctions[result['name']] = result
            elif symbol.__class__ is ast.ClassDef:
                result = self._parse_class(symbol)
                classes[result['name']] = result
        if globalAttributes:
            symbols['attributes'] = globalAttributes
        if globalFunctions:
            symbols['functions'] = globalFunctions
        if classes:
            symbols['classes'] = classes
        symbols['imports'] = self._parse_imports(module)
        symbols['docstring'] = ast.get_docstring(module, clean=True)

        return symbols

    def expand_attribute(self, attribute):
        """Expand the node to obtain the expanded representation."""
        parent_name = []
        while attribute.__class__ is ast.Attribute:
            parent_name.append(attribute.attr)
            attribute = attribute.value
        name = '.'.join(reversed(parent_name))
        attribute_id = ''
        if attribute.__class__ is ast.Name:
            attribute_id = attribute.id
        elif attribute.__class__ is ast.Call:
            if attribute.func.__class__ is ast.Attribute:
                attribute_id = '%s.%s()' % (
                    self.expand_attribute(attribute.func.value),
                    attribute.func.attr)
            else:
                attribute_id = '%s()' % attribute.func.id
        name = attribute_id if name == '' else ("%s.%s" % (attribute_id, name))
        return name

    def _parse_assign(self, symbol):
        """Parse assign and extract the info from the node."""
        assigns = {}
        attributes = {}
        for var in symbol.targets:
            if var.__class__ == ast.Attribute:
                attributes[var.attr] = var.lineno
            elif var.__class__ == ast.Name:
                assigns[var.id] = var.lineno
        return (assigns, attributes)

    def _parse_class(self, symbol):
        """Parse class and extract the info from the node."""
        docstring = ""
        attr = {}
        func = {}
        decorators = []
        name = symbol.name + '('
        name += ', '.join([
            self.expand_attribute(base) for base in symbol.bases])
        name += ')'
        for sym in symbol.body:
            if sym.__class__ is ast.Assign:
                result = self._parse_assign(sym)
                attr.update(result[0])
                attr.update(result[1])
            elif sym.__class__ is ast.FunctionDef:
                result = self._parse_function(sym)
                attr.update(result['attrs'])
                func[result['name']] = result

        docstring = ast.get_docstring(symbol, clean=True)

        lineno = symbol.lineno
        for decorator in symbol.decorator_list:
            decorators.append(self.expand_attribute(decorator))

        return {'name': name, 'attributes': attr, 'functions': func,
            'lineno': lineno, 'docstring': docstring, 'decorators': decorators}

    def _parse_function(self, symbol):
        """Parse function and extract the info from the node."""
        docstring = ""
        attrs = {}
        decorators = []

        func_name = symbol.name + '('
        #We store the arguments to compare with default backwards
        defaults = []
        for value in symbol.args.defaults:
            #TODO: In some cases we can have something like: a=os.path
            defaults.append(value)
        arguments = []
        for arg in reversed(symbol.args.args):
            if arg.__class__ is not _ast.Name or arg.id == 'self':
                continue
            argument = arg.id
            if defaults:
                value = defaults.pop()
                arg_default = _map_type.get(value.__class__, None)
                if arg_default is None:
                    if value.__class__ is _ast.Attribute:
                        arg_default = self.expand_attribute(value)
                    elif value.__class__ is _ast.Name:
                        arg_default = value.id
                    else:
                        arg_default = 'object'
                argument += '=' + arg_default
            arguments.append(argument)
        func_name += ', '.join(reversed(arguments))
        if symbol.args.vararg is not None:
            if not func_name.endswith('('):
                func_name += ', '
            func_name += '*' + symbol.args.vararg
        if symbol.args.kwarg is not None:
            if not func_name.endswith('('):
                func_name += ', '
            func_name += '**' + symbol.args.kwarg
        func_name += ')'

        for sym in symbol.body:
            if sym.__class__ is ast.Assign:
                result = self._parse_assign(sym)
                attrs.update(result[1])

        docstring = ast.get_docstring(symbol, clean=True)

        lineno = symbol.lineno
        for decorator in symbol.decorator_list:
            decorators.append(self.expand_attribute(decorator))

        return {'name': func_name, 'lineno': lineno,
            'attrs': attrs, 'docstring': docstring, 'decorators': decorators}

    def _parse_imports(self, module):
        """Parse imports and extract the info from the node."""
        #Imports{} = {name: asname}, for example = {sys: sysAlias}
        imports = {}
        #From Imports{} = {name: {module: fromPart, asname: nameAlias}}
        fromImports = {}
        for sym in module.body:
            if type(sym) is ast.Import:
                for item in sym.names:
                    imports[item.name] = {'asname': item.asname,
                        'lineno': sym.lineno}
            if type(sym) is ast.ImportFrom:
                for item in sym.names:
                    fromImports[item.name] = {'module': sym.module,
                        'asname': item.asname, 'lineno': sym.lineno}
        return {'imports': imports, 'fromImports': fromImports}
