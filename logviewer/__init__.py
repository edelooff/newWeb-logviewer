#!/usr/bin/python
"""A web interface to view log files as generated by uWeb"""

# Standard modules
import os

# Third-party modules
import newweb

# Application components
from . import viewer


def main():
  """Sets up the application for the logviewer."""
  config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
  config = newweb.read_config(config_file)
  routes = [
      ('/', 'Index'),
      ('/db/(.*)', 'Database'),
      ('/static/(.*)', 'Static'),
      ('/(.*)', 'Invalidcommand')]
  return newweb.NewWeb(viewer.Viewer, routes, config=config)
