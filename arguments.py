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

from __future__ import absolute_import

import argparse


usage = ("$documentor -p project_path -o output_path "
         "[--projectname name, --email address]")

epilog = ("This program comes with ABSOLUTELY NO WARRANTY."
          "This is free software, and you are welcome to redistribute "
          "it under certain conditions; for details see LICENSE.txt.")


def parse():
    global usage
    global epilog
    project = None
    projectname = None
    output = None
    email = None
    serve = False

    try:
        parser = argparse.ArgumentParser(description=usage, epilog=epilog)

        parser.add_argument('-p', '--project', metavar='project', type=str,
            help='Create documentation for this project',
            default=".")
        parser.add_argument('-o', '--output', metavar='Output Folder', type=str,
            help='Place to locate the outpur result', default=None)
        parser.add_argument('--projectname', metavar='projectname', type=str,
            help=('Project Name, if not provided the name is generated'
                  'using: documentor_PATHBASENAME'), default=None)
        parser.add_argument('--email', metavar='email', type=str,
            help='email address of the project', default=None)
        parser.add_argument('--serve', metavar='False/True: default False',
            type=str, help='Serve Documentation site', default=False)

        opts = parser.parse_args()
        project = opts.project
        projectname = opts.projectname
        output = opts.output
        email = opts.email
        serve = opts.serve
    except Exception as reason:
        print("Args couldn't be parsed.")
        print(reason)
    return (project, projectname, output, email, serve)
