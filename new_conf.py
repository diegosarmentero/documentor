# -*- coding: utf-8 -*-
import os

NEW_CONFIGURATION = """
BLOG_AUTHOR = "%(projectname)s"
BLOG_TITLE = "%(projectname)s Documentation"
BLOG_EMAIL = "%(email)s"

SIDEBAR_LINKS = {
    DEFAULT_LANG: (
        ('/documentor_modules.html', 'Modules'),
        ('/documentor_classes.html', 'Classes'),
        ('/documentor_functions.html', 'Functions'),
        ('/documentor_attributes.html', 'Attributes'),
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
    global NEW_CONFIGURATION
    NEW_CONFIGURATION = NEW_CONFIGURATION % {
        'projectname': projectname,
        'email': email
        }
    config_path = os.path.join(output, "conf.py")
    with open(config_path, 'a') as f:
        f.write('\n')
        f.write(NEW_CONFIGURATION)
