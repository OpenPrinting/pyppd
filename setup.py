from distutils.core import setup

setup(
    name='pyppd',
    version='0.1.4',
    author='Vitor Baptista',
    author_email='vitor@vitorbaptista.com',
    packages=['pyppd'],
    package_data={'pyppd': ['*.in']},
    scripts=['bin/pyppd'],
    url='http://gitorious.org/vitorbaptista/pyppd/',
    license='GPLv3',
    long_description=open('README.txt').read(),
)
