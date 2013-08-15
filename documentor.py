# -*- coding: utf-8 -*-
import os
import subprocess

import analyzer
import arguments
import new_conf

try:
    import nikola  # lint:ok
except:
    print """\nYou need to install Nikola in order to use Documentor, check out:

    http://nikola.ralsina.com.ar/\n\n"""
    raise Exception("Nikola is not installed.")


def document():
    project, projectname, output, email, serve = arguments.parse()
    if serve:
        doc_folder = '.'
        if output:
            doc_folder = output
        doc_folder = os.path.abspath(doc_folder)
        process = subprocess.Popen(["nikola", "serve"], cwd=doc_folder)
        process.wait()
        return

    if project is None or output is None:
            raise Exception("Invalid arguments, empty args are not allowed")

    if os.path.exists(project) and os.path.exists(output):
        project = os.path.abspath(project)
        if projectname is None:
            project_name = "documentor_%s" % os.path.basename(project)
        else:
            project_name = projectname
        output = os.path.abspath(output)
        process = subprocess.Popen(["nikola", "init", project_name], cwd=output)
        process.wait()
        output_folder = os.path.join(output, project_name)
        if os.path.exists(output_folder):
            new_conf.create_new_configuration(output_folder,
                                              project_name, email)
            analyzer.Analyzer(project, output_folder)
        else:
            print 'Something went wrong and output folder could not be created'


if __name__ == '__main__':
    document()