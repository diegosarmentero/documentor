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

"""Add extra configurations to Nikola."""

NEW_CONFIGURATION = """
BLOG_AUTHOR = "%(projectname)s"
BLOG_TITLE = "%(projectname)s Documentation"
BLOG_EMAIL = "%(email)s"

SIDEBAR_LINKS = {
    DEFAULT_LANG: (
        ('/documentor_modules.html', 'Modules'),
        ('/documentor_classes.html', 'Classes'),
        ('/documentor_functions.html', 'Functions'),
    ),
}

CONTENT_FOOTER = 'Contents &copy; {date}         <a href="mailto:{email}">{author}</a> - Powered by         <a href="http://nikola.ralsina.com.ar">Nikola</a> and <a href="https://github.com/diegosarmentero/documentor">Documentor</a>'
CONTENT_FOOTER = CONTENT_FOOTER.format(email=BLOG_EMAIL,
                                       author=BLOG_AUTHOR,
                                       date=time.gmtime().tm_year)

ADD_THIS_BUTTONS = False
DISQUS_FORUM = False
"""


def create_new_configuration(output, projectname, email):
    """Append some extra configurations to the conf.py file from Nikola."""
    global NEW_CONFIGURATION
    NEW_CONFIGURATION = NEW_CONFIGURATION % {
        'projectname': projectname,
        'email': email
        }
    config_path = os.path.join(output, "conf.py")
    with open(config_path, 'a') as f:
        f.write('\n')
        f.write(NEW_CONFIGURATION)
