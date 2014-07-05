#!/usr/bin/python
"""A web interface to view log files as generated by uWeb"""

# Standard modules
import os

# Third-party modules
import uweb

# Application components
from . import viewer


def main():
  """Sets up the application for the logviewer."""
  config = os.path.join(os.path.dirname(__file__), 'config.ini')
  routes = [
      ('/', 'Index'),
      ('/db/(.*)', 'Database'),
      ('/static/(.*)', 'Static'),
      ('/(.*)', 'Invalidcommand')]
  return uweb.NewWeb(viewer.Viewer, routes, config=uweb.read_config(config))