from distutils.core import setup

setup(
    name='pyppd',
    version='0.1.5',
    author='Vitor Baptista',
    author_email='vitor@vitorbaptista.com',
    packages=['pyppd'],
    package_data={'pyppd': ['*.in']},
    scripts=['bin/pyppd'],
    url='http://gitorious.org/vitorbaptista/pyppd/',
    license='GPLv3',
    description='A CUPS PostScript Printer Driver\'s compressor and generator',
    long_description=open('README.txt').read(),
)
