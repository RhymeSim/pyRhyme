from setuptools import setup
from distutils.command.build_py import build_py as _build_py
import py_rhyme.tests.chombo as _chombo
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class CreateTestChombo(_build_py):
    '''Custom build command to create a test CHOMBO file'''

    def run(self):
        '''run `python setup.py chombo` to create a new test file'''
        _chombo.create()
        _build_py.run(self)


setup(
    name='py_rhyme',
    version='0.0',
    description='Simple code to read and process Rhyme outputs',
    long_description=read('README.md'),
    url='https://gitlab.com/rhyme-org/py-rhyme.git',
    keywords='Rhyme radiation hydrodynamics simulation',
    author='Saeed Sarpas',
    author_email='saeed.sarpas@phys.ethz.ch',
    license='GPLv3',
    packages=['py_rhyme'],
    install_requires=[
        'h5py',
        'numpy'
    ],
    scripts=[
        'scripts/rhyme_slice',
        'scripts/rhyme_lineout',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    cmdclass={
        'chombo': CreateTestChombo,
    },
    zip_safe=False,
)
