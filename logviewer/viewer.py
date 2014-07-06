#!/usr/bin/python
"""HTML generators for the logging web frontend"""

__version__ = '0.5'

# Standard modules
import datetime
import pytz
import time
import os

# Third-party modules
import babel.dates
import newweb

# Application modules
from . import model


class Viewer(newweb.DebuggingPageMaker):
  """Holds all the html generators for the logger web frontend

  Each page as a separate method.
  """
  PUBLIC_DIR = 'static'
  TEMPLATE_DIR = 'templates'

  def _PostInit(self):
    self.parser.RegisterFunction('datetime', DateFormat)
    self.parser.RegisterFunction('time_ago', time_ago)
    self.parser.RegisterFunction('duration', duration_milliseconds)
    self.parser.RegisterFunction('80cols', cut_after(80))
    self.paths = list(self._LogPaths())

  def _LogPaths(self):
    for path in self.options['paths']['logs'].split(os.path.pathsep):
      if path.strip():
        yield os.path.expanduser(path.strip())

  def _OpenLogDatabase(self, db_name):
    db_path = os.path.normpath(db_name)
    for path in self.paths:
      if db_path.startswith(path):
        break
    else:
      raise newweb.ImmediateResponse(self.InvalidDatabase(db_path))
    try:
      return model.LogDb(db_path)
    except model.DatabaseError, error:
      raise newweb.ImmediateResponse(self.InvalidDatabase(error))

  def Index(self):
    logs = model.Logging(self.paths, self.options['paths']['filemask'])
    return self.parser.Parse(
        'index.html', logfiles=logs.ListFiles(), **self.CommonBlocks('Home'))

  def Database(self, db_name):
    log_db = self._OpenLogDatabase(db_name)
    count = int(self.get.getfirst('count', 20))
    offset = int(self.get.getfirst('offset', 0))
    query = self.get.getfirst('query', '')
    level = self.get.getfirst('level', 0)

    events = log_db.Events(offset=offset, count=count, query=query, level=level)
    pagelinks = []
    if offset > 0:
      pagelinks.append(self.parser.Parse(
          'pagination_link.html', count=count, level=level,
          offset=max(offset - count, 0), query=query, title='Previous Page'))
    #XXX(Elmer): This may generate a false last next-link, because there is
    # no way to tell whether there are more files. It's a good bet though.
    if len(events) == count:
      pagelinks.append(self.parser.Parse(
          'pagination_link.html', count=count, level=level,
          offset=offset + count, query=query, title='Next Page'))
    if pagelinks:
      pagination = self.parser.Parse('pagination.html',
                                     pagelinks=''.join(pagelinks))
    else:
      pagination = ''

    return self.parser.Parse(
        'database.html',
        pagination=pagination,
        db_name=db_name,
        req_vars={'query': query, 'count': count, 'level': level},
        events=events,
        **self.CommonBlocks(db_name, scripts=(
            'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
            '/static/database.js')))

  def Invalidcommand(self, path):
    """Returns an error message"""
    self.req.registry.logger.warning('Bad page %r requested', path)
    self.req.response.httpcode = 404
    return self.parser.Parse(
        '404.html', error=path, **self.CommonBlocks('Page not found'))

  def InvalidDatabase(self, path):
    """Returns an error message"""
    self.req.registry.logger.warning('Bad database %r requested', path)
    self.req.response.httpcode = 404
    return self.parser.Parse(
        'invaliddb.html', error=path, **self.CommonBlocks('Database not found'))

  def Header(self, title='Available databases', page_id=None):
    """Returns the header template, filled out from the given title and page_id.

    Arguments:
      @ title: str
        The page's title as it should be in the html
      % page_id: str
        The page_id as it should occur on the body tag. If left undefined, the
        page title is used, replacing spaces with underscores.
    """
    if not page_id:
      page_id = title.replace(' ', '_').lower()
    return self.parser.Parse('header.html', title=title, page_id=page_id)

  def Footer(self, scripts):
    """Returns the footer html"""
    return self.parser.Parse(
        'footer.html',
        scripts=scripts,
        year=time.strftime('%Y'),
        version={'newweb': newweb.__version__, 'logviewer': __version__})

  def Sidebar(self):
    logs = model.Logging(self.paths, self.options['paths']['filemask'])
    return self.parser.Parse('sidebar.html', logfiles=logs.ListFiles())

  def CommonBlocks(self, title, page_id=None, scripts=()):
    return {'sidebar': self.Sidebar(),
            'header': self.Header(title, page_id),
            'footer': self.Footer(scripts)}


def cut_after(length):
  """Returns a function that cuts the string short after `length` characters."""
  def _cut_after(text, length=length):
    if len(text) > length:
      text = text[:length - 1] + u'\N{HORIZONTAL ELLIPSIS}'
    return text
  return _cut_after


def DateFormat(dtime):
  """Returns only the date portion (as string) of a datetime object."""
  return dtime.strftime('%F %T')


def duration_milliseconds(milliseconds):
  """Returns a timedelta input in milliseconds as a human readable string."""
  return format_delta(datetime.timedelta(milliseconds=milliseconds))


def time_ago(dtime):
  """Returns the amount of time something happened in the past."""
  return format_delta(pytz.utc.localize(datetime.datetime.utcnow()) - dtime)


def format_delta(delta):
  """Returns a string describing the timedelta in natural language."""
  return babel.dates.format_timedelta(delta, threshold=1.5, locale='en')
