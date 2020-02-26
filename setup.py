#!/usr/bin/env python3

from distutils.core import setup
from distutils.command.sdist import sdist as _sdist

class sdist(_sdist):
    def run(self):
        try:
            import sys
            sys.path.append("contrib")
            import git2changes
            print('generating CHANGES.txt')
            with open('CHANGES.txt', 'w+') as f:
                git2changes.run(f)
        except ImportError:
            pass

        _sdist.run(self)

setup(
    name='pyppd',
    version='1.1.0',
    author='Vitor Baptista',
    author_email='vitor@vitorbaptista.com',
    packages=['pyppd'],
    package_data={'pyppd': ['*.in']},
    scripts=['bin/pyppd'],
    url='https://github.com/OpenPrinting/pyppd/',
    license='MIT',
    description='A CUPS PostScript Printer Driver\'s compressor and generator',
    long_description=open('README', 'rb').read().decode('UTF-8'),
    cmdclass={'sdist': sdist},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX',
        'License :: OSI Approved :: MIT License',
        'Topic :: Printing',
        ],
)
