# -*- coding: utf-8 -*-
#
# This file is part of NINJA-IDE (http://ninja-ide.org).
#
# NINJA-IDE is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# NINJA-IDE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NINJA-IDE; If not, see <http://www.gnu.org/licenses/>.
import _ast
import ast
import os

#from ninja_ide.tools.completion import analyzer

_map_type = {
    _ast.Tuple: 'tuple',
    _ast.List: 'list',
    _ast.Str: 'str',
    _ast.Dict: 'dict',
    _ast.Num: 'int',
    _ast.Call: 'function()',
}


class Analyzer(object):

    def __init__(self, project, output):
        self.files_folder = os.path.join(output, 'files')
        self.posts_folder = os.path.join(output, 'posts')
        self.stories_folder = os.path.join(output, 'stories')
        self.listings_folder = os.path.join(output, 'listings')

    def expand_attribute(self, attribute):
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
        assigns = {}
        attributes = {}
        for var in symbol.targets:
            if var.__class__ == ast.Attribute:
                attributes[var.attr] = var.lineno
            elif var.__class__ == ast.Name:
                assigns[var.id] = var.lineno
        return (assigns, attributes)

    def _parse_class(self, symbol, with_docstrings):
        docstring = {}
        attr = {}
        func = {}
        clazz = {}
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
                result = self._parse_function(sym, with_docstrings)
                attr.update(result['attrs'])
                if with_docstrings:
                    docstring.update(result['docstring'])
                func[result['name']] = {'lineno': result['lineno'],
                    'functions': result['functions']}
            elif sym.__class__ is ast.ClassDef:
                result = self._parse_class(sym, with_docstrings)
                clazz[result['name']] = {'lineno': result['lineno'],
                    'members': {'attributes': result['attributes'],
                    'functions': result['functions']}}
                docstring.update(result['docstring'])
        if with_docstrings:
            docstring[symbol.lineno] = ast.get_docstring(symbol, clean=True)

        lineno = symbol.lineno
        for decorator in symbol.decorator_list:
            lineno += 1

        return {'name': name, 'attributes': attr, 'functions': func,
            'lineno': lineno, 'docstring': docstring, 'classes': clazz}

    def _parse_function(self, symbol, with_docstrings):
        docstring = {}
        attrs = {}
        func = {'functions': {}}

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
            elif sym.__class__ is ast.FunctionDef:
                result = self._parse_function(sym, with_docstrings)
                if with_docstrings:
                    docstring.update(result['docstring'])
                func['functions'][result['name']] = {'lineno': result['lineno'],
                    'functions': result['functions']}

        if with_docstrings:
            docstring[symbol.lineno] = ast.get_docstring(symbol, clean=True)

        lineno = symbol.lineno
        for decorator in symbol.decorator_list:
            lineno += 1

        return {'name': func_name, 'lineno': lineno,
            'attrs': attrs, 'docstring': docstring, 'functions': func}

    def obtain_symbols(self, source, with_docstrings=False, filename=''):
        """Parse a module code to obtain: Classes, Functions and Assigns."""
        try:
            module = ast.parse(source)
        except:
            print "The file contains syntax errors: %s" % filename
            return {}
        symbols = {}
        globalAttributes = {}
        globalFunctions = {}
        classes = {}
        docstrings = {}

        for symbol in module.body:
            if symbol.__class__ is ast.Assign:
                result = self._parse_assign(symbol)
                globalAttributes.update(result[0])
                globalAttributes.update(result[1])
            elif symbol.__class__ is ast.FunctionDef:
                result = self._parse_function(symbol, with_docstrings)
                if with_docstrings:
                    docstrings.update(result['docstring'])
                globalFunctions[result['name']] = {'lineno': result['lineno'],
                    'functions': result['functions']}
            elif symbol.__class__ is ast.ClassDef:
                result = self._parse_class(symbol, with_docstrings)
                classes[result['name']] = {'lineno': result['lineno'],
                    'members': {'attributes': result['attributes'],
                    'functions': result['functions'],
                    'classes': result['classes']}}
                docstrings.update(result['docstring'])
        if globalAttributes:
            symbols['attributes'] = globalAttributes
        if globalFunctions:
            symbols['functions'] = globalFunctions
        if classes:
            symbols['classes'] = classes
        if docstrings and with_docstrings:
            symbols['docstrings'] = docstrings

        return symbols

    def obtain_imports(self, source='', body=None):
        if source:
            try:
                module = ast.parse(source)
                body = module.body
            except:
                print "A file contains syntax errors"
        #Imports{} = {name: asname}, for example = {sys: sysAlias}
        imports = {}
        #From Imports{} = {name: {module: fromPart, asname: nameAlias}}
        fromImports = {}
        for sym in body:
            if type(sym) is ast.Import:
                for item in sym.names:
                    imports[item.name] = {'asname': item.asname,
                        'lineno': sym.lineno}
            if type(sym) is ast.ImportFrom:
                for item in sym.names:
                    fromImports[item.name] = {'module': sym.module,
                        'asname': item.asname, 'lineno': sym.lineno}
        return {'imports': imports, 'fromImports': fromImports}
