from setuptools import setup

setup(
    name='dcator',
    version=1.0,
    packages=['dcator'],
    install_requires=['click', 'krakenex', 'pytest'],
    entry_points={'console_scripts': ['kraken = dcator.cli:cli']}
)
