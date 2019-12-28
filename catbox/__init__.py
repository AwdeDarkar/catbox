"""
  init  
====================================================================================================

Setup script for catbox app

----------------------------------------------------------------------------------------------------

**Created**
    2019-12-27
**Updated**
    2019-12-27 by Darkar
**Author**
    Darkar
**Copyright**
    This software is Free and Open Source for any purpose
"""

import os

from flask import Flask


def create_app(test_config=None):
    """ Create and configure the app """
    app = Flask(__name__, instance_relative_config=True)
