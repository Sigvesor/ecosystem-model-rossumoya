from setuptools import setup
import codecs
import os


def read_readme():
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setup(
        # Basic information
        name='Modelling the Ecosystem of Rossumoya',
        version='1.0.0',
        # Packages to include
        packages=['biosim', 'biosim.tests'],
        # Required packages not included in Python standard
        # library:
        requires=['numpy (>=1.8.1)', 'matplotlib (>= 1.3.1)', 'Pandas'],
        # metadata
        description='A Chutes & Ladders Simulation',
        long_description=read_readme(),
        author='Sigve Sørensen & Filip Rotnes, NMBU',
        author_email='hans.ekkehard.plesser@nmbu.no',
        url='https://bitbucket.org/heplesser/nmbu_inf200_h17',
        keywords='simulation game',
        license='MIT License',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Science :: Stochastic processes',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
]
)