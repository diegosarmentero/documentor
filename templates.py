# -*- coding: utf-8 -*-

BASE_FILE = """.. link:
.. description:
.. tags:
.. date: %(date)s
.. title: %(projectname)s
.. slug: %(filename)s

.. class:: alert alert-info pull-top

.. contents::

"""

MODULE = "\n*Module:* `%(name)s <%(link)s>`_ API\n"  # ==
IMPORTS = "\n*Imports:*\n"  # --
GLOBAL_ATTRIBUTES = "\n*Global Attributes:*\n"  # --
GLOBAL_FUNCTIONS = "\n*Global Functions:*\n"  # --
CLASS = "\n*Class:* `%(name)s <%(link)s>`_\n"  # --
CODE = """\n.. code:: python
   :number-lines:

       %(code)s

"""
PARENTS = "\n*Parents*\n"  # ~~
ATTRIBUTES = "\n*Attributes*\n"  # ~~
FUNCTION = "\n*Function:* `%(name)s <%(link)s>`_\n"  # ~~
NO_DESCRIPTION = "\nNo description.\n\n"
ARGUMENTS = "\n**Arguments:**\n"
DECORATORS = "\n**Decorators:**\n\n"
LIST_LINK_ITEM = '- `%(name)s <%(link)s>`_\n'

###############################################################################

POST = """
.. link:
.. description:
.. tags:
.. date: %(date)s
.. title: %(projectname)s
.. slug: documentor

`Modules </documentor_modules.html>`_
=========================================
Check out the Modules of the project

----

`Classes </documentor_classes.html>`_
=========================================
Check out the Classes of the project

----

`Functions </documentor_functions.html>`_
=============================================
Check out the functions of the project

"""

HTML_FILES_HEADER = """
<!DOCTYPE html><html lang="en">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <meta charset="utf-8">
    <meta name="description" content="">
    <meta name="author" content="%(projectname)s">
    <title>%(projectname)s | %(projectname)s Documentation</title>
            <link href="../../assets/css/bootstrap.min.css" rel="stylesheet" type="text/css">
            <link href="../../assets/css/bootstrap-responsive.min.css" rel="stylesheet" type="text/css">
        <link href="../../assets/css/rst.css" rel="stylesheet" type="text/css">
        <link href="../../assets/css/code.css" rel="stylesheet" type="text/css">
        <link href="../../assets/css/colorbox.css" rel="stylesheet" type="text/css">
        <link href="../../assets/css/theme.css" rel="stylesheet" type="text/css">
        <link rel="alternate" type="application/rss+xml" title="RSS" href="../../rss.xml">
</head>
<body>
<!-- Menubar -->
<div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
        <div class="container">
        <!-- .btn-navbar is used as the toggle for collapsed navbar content -->
        <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
        </a>
            <a class="brand" href="../../">
            %(projectname)s Documentation
            </a>
            <!-- Everything you want hidden at 940px or less, place within here -->
            <div class="nav-collapse collapse">
                <ul class="nav">
            <li><a href="../../documentor_modules.html">Modules</a>
            </li><li><a href="../../documentor_classes.html">Classes</a>
            </li><li><a href="../../documentor_functions.html">Functions</a>
                </li></ul>
            </div>
        </div>
    </div>
</div>
<!-- End of Menubar -->
<div class="container-fluid" id="container-fluid">
    <!--Body content-->
    <div class="row-fluid">
    <div class="span2"></div>
    <div class="span8">

    <h1>%(projectname)s</h1>
    <div class="contents alert alert-info pull-top topic" id="contents">
<p class="topic-title first">Index</p>
<ul class="simple">
<li><a class="reference internal" href="../../documentor_modules.html" id="id1"><em>Modules</em></a>
<li><a class="reference internal" href="../../documentor_classes.html" id="id1"><em>Classes</em></a>
<li><a class="reference internal" href="../../documentor_functions.html" id="id1"><em>Functions</em></a>
</li>
</ul>
</div>
<div class="section" id="classes">
<h2><em>%(type)s:</em></h2>
<div class="section" id="classes">
<ul class="simple">
"""

HTML_FILES_BODY = """
<li><a class="reference external" href="%(link)s">%(name)s</a></li>"""

HTML_FILES_FOOTER = """
</ul>
</div>
<div class="footerbox">
    Contents © %(year)s         <a href="#">%(projectname)s</a> - Powered by         <a href="http://nikola.ralsina.com.ar">Nikola</a> and <a href="https://github.com/diegosarmentero/documentor">Documentor</a>
</div>
            <script src="../../assets/js/jquery-1.7.2.min.js" type="text/javascript"></script>
            <script src="../../assets/js/bootstrap.min.js" type="text/javascript"></script>
        <script src="../../assets/js/jquery.colorbox-min.js" type="text/javascript"></script>
    <script type="text/javascript">jQuery("a.image-reference").colorbox({rel:"gal",maxWidth:"80%%",maxHeight:"80%%",scalePhotos:true});</script>
</body>
</html>
"""