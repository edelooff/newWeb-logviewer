"""Starts a local development server for newWeb info."""

# Application
import logviewer


def main():
  app = logviewer.main()
  app.serve()


if __name__ == '__main__':
  main()
