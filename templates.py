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