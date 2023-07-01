from setuptools import setup

setup(
    name='fap',
    version='0.1',
    py_modules=['fap'],
    entry_points={
        'console_scripts': [
            'fap = fap:main'
        ]
    },
    url='https://github.com/null3yte/fap/',
    install_requires=[
        'requests',
        'bs4'
    ],
    author='null3yte',
    author_email='nullmad.eb00@gmail.com',
    description='Web keyword extractor & customized wordlist generator for parameter FUZZing.'
)
