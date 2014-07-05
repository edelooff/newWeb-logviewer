"""Starts a local development server for newWeb info."""

# Third-party modules
import uweb

# Application
import logviewer


def main():
  app = logviewer.main()
  app.serve()


if __name__ == '__main__':
  main()
