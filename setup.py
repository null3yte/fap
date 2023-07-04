from setuptools import setup
import os

os.system('pip install -r requirements.txt')

setup(
    name='fap',
    version='0.2',
    py_modules=['fap'],
    entry_points={
        'console_scripts': [
            'fap = fap:main'
        ]
    },
    url='https://github.com/null3yte/fap/',
    author='null3yte',
    author_email='nullmad.eb00@gmail.com',
    description='Web keyword extractor & customized wordlist generator for parameter FUZZing.'
)
