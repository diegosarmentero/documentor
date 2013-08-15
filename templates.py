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

MODULE = "*Module:* `%(name)s <%(link)s>`_ API"  # ==
IMPORTS = "*Imports:*"  # --
GLOBAL_ATTRIBUTES = "*Global Attributes:*"  # --
CLASS = "*Class:* `%(name)s <%(link)s>`_"  # --
CODE = """.. code:: python
   :number-lines:

       %(code)s
"""
PARENTS = "*Parents*"  # ~
ATTRIBUTES = "*Attributes*"  # ~
FUNCTION = "*Function:* `%(name)s <%(link)s>`_"
NO_DESCRIPTION = "No description."
ARGUMENTS = "**Arguments:**"
DECORATORS = "**Decorators:**"