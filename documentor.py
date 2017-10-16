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
import subprocess

import analyzer
import arguments
import new_conf

"""Main file of Documentor."""


def _get_project_name(projectname, project):
    """Build a project name or use the one provided by the user."""
    if projectname is None:
        project_name = "documentor_%s" % os.path.basename(project)
    else:
        project_name = projectname
    return project_name


def _deploy(output, deploy):
    """Deploy the site to Github Pages."""
    print('\nDeploy...\n')
    output_folder = os.path.join(output, 'output')
    commands = [
        ["git", "init"],
        ["git", "remote", "add", "origin", deploy],
        ["git", "checkout", "--orphan", "gh-pages"],
        ["git", "pull", deploy],
        ["git", "rm", "-rf", "."],
        ["git", "add", "."],
        ["git", "commit", "-a", "-m", "'documentator deploy'"],
        ["git", "push", "origin", "gh-pages"]
    ]
    for command in commands:
        process = subprocess.Popen(command, cwd=output_folder)
        process.wait()
    print('\nDeploy Complete!\n')


def _serve(output):
    """Serve the application in localhost."""
    doc_folder = '.'
    if output:
        doc_folder = output
    doc_folder = os.path.abspath(doc_folder)
    process = subprocess.Popen(["nikola", "serve"], cwd=doc_folder)
    process.wait()


def document():
    """Run the commands selected by the user with Documentor."""
    project, projectname, output, email, serve, deploy = arguments.parse()
    if deploy:
        output = os.path.abspath(output)
        _deploy(output, deploy)
        return
    elif serve:
        _serve(output)
        return

    if project is None or output is None:
            raise Exception("Invalid arguments, empty args are not allowed")

    if os.path.exists(project) and os.path.exists(output):
        project = os.path.abspath(project)
        project_name = _get_project_name(projectname, project)
        output = os.path.abspath(output)
        process = subprocess.Popen(["nikola", "init", project_name], cwd=output)
        process.wait()
        output_folder = os.path.join(output, project_name)
        if os.path.exists(output_folder):
            new_conf.create_new_configuration(output_folder,
                                              project_name, email)
            worker = analyzer.Analyzer(project, output_folder, project_name)
            worker.scan()
            process = subprocess.Popen(["nikola", "build"], cwd=output_folder)
            process.wait()
        else:
            print('Something went wrong and output folder could not be created')


if __name__ == '__main__':
    document()