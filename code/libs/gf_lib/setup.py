from setuptools import setup, find_packages

setup(
    name='gf_lib',
    description='Core library for Good Fundamentals',
    version='0.0.1',
    author='James Dooley',
    author_email='james@developernotes.org',
    packages=find_packages(exclude=('test',)),
    url='https://www.developernotes.org'
)
