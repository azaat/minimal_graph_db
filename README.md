# SPbU Formal Languages Course assignments
[![Build Status](https://travis-ci.org/azaat/formal_languages_course.svg?branch=master)](https://travis-ci.org/azaat/formal_languages_course)

## Assignment 1

Basic tests for pyformlang and pygraphblas functions are in ```./tests/test_1```

Installation uses [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) package manager.
In order to run tests locally, use: 
```
conda create -q -n test-env python=3.8 pygraphblas pytest
conda activate test-env
pip3 install pyformlang                                                   
```
Then, while in the root directory, simply run:
```
pytest
```