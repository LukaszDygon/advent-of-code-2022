import setuptools

setuptools.setup(
    name='aoc_helpers',  
    version='0.1',
    scripts=['aoc_helpers/input_helper.py'],
    author="Lukasz Dygon",
    author_email="",
    description="A set of helper functions for Advent of Code",
    long_description="A set of helper functions for Advent of Code",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )