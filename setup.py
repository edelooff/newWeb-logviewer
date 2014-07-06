import os
from setuptools import setup, find_packages

REQUIREMENTS = [
    'babel',
    'uweb',
]


def readme():
  with file(os.path.join(os.path.dirname(__file__), 'readme.md')) as r_file:
    return r_file.read()


setup(
    name='newweb_logviewer',
    version='0.5',
    description='Viewer for uWeb log databases (SQLite)',
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: newWeb",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"],
    dependency_links=[
        'https://github.com/edelooff/newWeb/tarball/master#egg=uweb',],
    author='Elmer de Looff',
    author_email='elmer.delooff@gmail.com',
    url='https://github.com/edelooff/newWeb-logviewer',
    keywords='web sqlite newweb',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS)
