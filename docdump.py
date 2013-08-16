# -*- coding: utf-8 -*-
import os
import datetime

import templates


#FIXME: Improve the code for content creation


class DocDump(object):

    def __init__(self, projectname, output):
        self.projectname = projectname
        today = datetime.date.today()
        self.date = today.strftime('%Y/%m/%d %H:%M:%S')
        self.files_folder = os.path.join(output, 'files')
        self.posts_folder = os.path.join(output, 'posts')
        self.output = os.path.join(output, 'stories')

        self._create_post()

        self.__modules = []
        self.__classes = []
        self.__functions = []

    def process_symbols(self, symbols, filepath, relpath):
        basename = os.path.basename(filepath)
        name = os.path.splitext(basename)[0]
        path = os.path.join(self.output, relpath)
        htmlpath = os.path.join('/listings/', relpath, basename + '.html')
        docpath = os.path.join('/stories/', relpath, name + '.html')
        content = templates.BASE_FILE % {
            'date': self.date,
            'projectname': self.projectname,
            'filename': name
        }
        # MODULE
        module_line = templates.MODULE % {
            'name': basename,
            'link': htmlpath
        }
        content += module_line + ('=' * len(module_line)) + '\n'

        docstring = symbols.get('docstring')
        if docstring:
            docstring = '| %s' % docstring.replace(
                '*', '\\*').replace('`', '\\`').replace('_', '\_')
            doc = '| '.join([line + '\n'
                             for line in docstring.split('\n')]) + '\n'
        else:
            doc = templates.NO_DESCRIPTION + '\n'
        content += doc

        content += self._add_imports(symbols, htmlpath) + '\n'
        content += self._add_global_attributes(symbols, htmlpath) + '\n'
        content += self._add_global_functions(symbols, htmlpath, docpath) + '\n'
        content += self._add_classes(symbols, htmlpath, docpath) + '\n'

        content = content.strip()
        if content[-4:] == '----':
            content = content[:-4]
        content += '\n\n'

        self.__modules.append((basename, docpath, 0))

        if not os.path.exists(path):
            os.makedirs(path)

        write_path = os.path.join(path, name + '.txt')
        with open(write_path, 'w') as f:
            f.write(content)

    def _create_post(self):
        post = templates.POST % {
            'date': self.date,
            'projectname': self.projectname
        }

        path = os.path.join(self.posts_folder, 'index_post' + '.txt')
        with open(path, 'w') as f:
            f.write(post)

    def _add_imports(self, symbols, htmlpath):
        content = ''
        results = symbols['imports']
        imports = results['imports']
        fromImports = results['fromImports']

        if imports or fromImports:
            content += templates.IMPORTS + (
                        '-' * len(templates.IMPORTS)) + '\n'

        imports_key = sorted(imports.keys())
        for imp in imports_key:
            content += templates.LIST_LINK_ITEM % {
                'name': imp,
                'link': '%s#%s' % (htmlpath, imports[imp]['lineno'])
            } + '\n'

        fromImports_key = sorted(fromImports.keys())
        for imp in fromImports_key:
            content += templates.LIST_LINK_ITEM % {
                'name': fromImports[imp]['module'] + ".%s" % imp,
                'link': '%s#%s' % (htmlpath, fromImports[imp]['lineno'])
            } + '\n'

        return content

    def _add_global_attributes(self, symbols, htmlpath):
        content = ''
        attrs = symbols.get('attributes')
        if attrs:
            content += templates.GLOBAL_ATTRIBUTES + (
                        '-' * len(templates.GLOBAL_ATTRIBUTES)) + '\n'

            attrs_key = sorted(attrs.keys())
            for attr in attrs_key:
                content += templates.LIST_LINK_ITEM % {
                    'name': "%s [at ln:%d]" % (attr, attrs[attr]),
                    'link': '%s#%s' % (htmlpath, attrs[attr])
                } + '\n'

            content += '\n----\n'

        return content

    def _add_global_functions(self, symbols, htmlpath, docpath):
        content = ''
        funcs = symbols.get('functions')
        if funcs:
            content += templates.GLOBAL_FUNCTIONS + (
                        '-' * len(templates.GLOBAL_FUNCTIONS)) + '\n'

            funcs_key = sorted(funcs.keys())
            for func in funcs_key:
                content += self._add_function(funcs[func], htmlpath, docpath)

        return content

    def _add_function(self, symbol, htmlpath, docpath):
        content = ''
        function_name = templates.FUNCTION % {
            'name': "%s [at ln:%d]" % (symbol['name'], symbol['lineno']),
            'link': '%s#%s' % (htmlpath, symbol['lineno'])
        }
        content += function_name + ('~' * len(function_name)) + '\n'

        content += templates.CODE % {
            'code': "def %s:" % symbol['name']
        }

        docstring = symbol['docstring']
        if docstring:
            docstring = '| %s' % docstring.replace(
                '*', '\\*').replace('`', '\\`').replace('_', '\_')
            doc = '| '.join([line + '\n'
                             for line in docstring.split('\n')]) + '\n'
        else:
            doc = templates.NO_DESCRIPTION
        content += doc

        if symbol['decorators']:
            content += templates.DECORATORS
            for decorator in symbol['decorators']:
                content += '- *%s*\n' % decorator

        self.__functions.append((symbol['name'], docpath, symbol['lineno']))

        content += '\n----\n'

        return content

    def _add_classes(self, symbols, htmlpath, docpath):
        content = ''
        clazzes = symbols.get('classes', [])
        for clazz in clazzes:
            clazz_name = templates.CLASS % {
                'name': clazz,
                'link': '%s#%s' % (htmlpath, clazzes[clazz]['lineno'])
            }
            content += clazz_name + ('-' * len(clazz_name)) + '\n'

            content += templates.CODE % {
                'code': "class %s:" % clazz
            }

            docstring = clazzes[clazz]['docstring']
            if docstring:
                docstring = '| %s' % docstring.replace(
                '*', '\\*').replace('`', '\\`').replace('_', '\_')
                doc = '| '.join([line + '\n'
                                 for line in docstring.split('\n')]) + '\n'
            else:
                doc = templates.NO_DESCRIPTION
            content += doc

            attrs = clazzes[clazz]['attributes']
            if attrs:
                content += templates.ATTRIBUTES + (
                            '~' * len(templates.ATTRIBUTES)) + '\n'

                attrs_key = sorted(attrs.keys())
                for attr in attrs_key:
                    content += templates.LIST_LINK_ITEM % {
                        'name': "%s [at ln:%d]" % (attr, attrs[attr]),
                        'link': '%s#%s' % (htmlpath, attrs[attr])
                    } + '\n'

            funcs = clazzes[clazz]['functions']
            if funcs:
                funcs_key = sorted(funcs.keys())
                for func in funcs_key:
                    content += self._add_function(funcs[func], htmlpath,
                        docpath)
            else:
                content += '\n----\n'

            self.__classes.append((clazz, docpath, clazzes[clazz]['lineno']))

        return content

    def create_html_sections(self):
        # Modules
        html = templates.HTML_FILES_HEADER % {
            'projectname': self.projectname,
            'type': 'Modules'
        }
        for mod in sorted(self.__modules, key=lambda x: x[0]):
            html += templates.HTML_FILES_BODY % {
                'link': mod[1],
                'name': mod[0]
            }
        html += templates.HTML_FILES_FOOTER % {
            'year': str(datetime.date.today().year),
            'projectname': self.projectname
        }

        path = os.path.join(self.files_folder, 'documentor_modules.html')
        with open(path, 'w') as f:
            f.write(html)

        # Classes
        html = templates.HTML_FILES_HEADER % {
            'projectname': self.projectname,
            'type': 'Classes'
        }
        for cla in sorted(self.__classes, key=lambda x: x[0]):
            html += templates.HTML_FILES_BODY % {
                'link': "%s#%d" % (cla[1], cla[2]),
                'name': cla[0]
            }
        html += templates.HTML_FILES_FOOTER % {
            'year': str(datetime.date.today().year),
            'projectname': self.projectname
        }

        path = os.path.join(self.files_folder, 'documentor_classes.html')
        with open(path, 'w') as f:
            f.write(html)

        # Functions
        html = templates.HTML_FILES_HEADER % {
            'projectname': self.projectname,
            'type': 'Functions'
        }
        for fun in sorted(self.__functions, key=lambda x: x[0]):
            html += templates.HTML_FILES_BODY % {
                'link': "%s#%d" % (fun[1], fun[2]),
                'name': fun[0]
            }
        html += templates.HTML_FILES_FOOTER % {
            'year': str(datetime.date.today().year),
            'projectname': self.projectname
        }

        path = os.path.join(self.files_folder, 'documentor_functions.html')
        with open(path, 'w') as f:
            f.write(html)