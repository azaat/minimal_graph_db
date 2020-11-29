# SPbU Formal Languages Course assignments
[![Build Status](https://travis-ci.org/azaat/formal_languages_course.svg?branch=master)](https://travis-ci.org/azaat/formal_languages_course)

## Assignment 1

Basic tests for pyformlang and pygraphblas functions are in ```./tests/test_1```

Installation uses [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) package manager.
In order to run tests locally, use: 
```
conda create -q -n test-env python=3.8 pygraphblas pytest numpy
conda activate test-env
pip3 install pyformlang                                                   
```
Then, while in the root directory, simply run:
```
pytest
```

## Assignment_2: Simple graph DB

Minimal Graph DB accepts graphs in simple triples format, uses pyformlang regex format to specify queries.
```
usage: main.py [-h] --graph GRAPH --regex REGEX [--start START] [--end END]

optional arguments:
  -h, --help     show this help message and exit
  --graph GRAPH  path to graph file
  --regex REGEX  path to regex file
  --start START  path to given starting vertices
  --end END      path to given end vertices
  ```

Test with ```python3 -m pytest```

## Assignment_3

Experimental report can be found in ```RPQAnalysis.pdf```. CSV files used in analysis are in ./query_benchmarks.

## Assignment_4

Added wrapper for Context-Free grammars in pyformlang which uses my implementation of CYK algorithm for the ```contains``` method.

Module ```src.cfpq``` implements the extended version of this algorithm to perform context-free path querying.

## Assignment_5

Two more cfpq implementations were added in ```src.cfpq```: with matrix multiplication and with transitive closure

CFG is accepted as text file with lines ```HEAD BODY``` delimited with space symbols. The format allows production body to contain regular expression:

```
S (a S b)*
```

All variables should be uppercase, terminals - lowercase.


## Assignment_6

Experimental report with different CFPQ algorithms can be found in ```CFPQAnalysis.pdf```. The plots were generated using the Seaborn library, algorithms were launched with ```timeout 30m``` shell command, to avoid hanging benchmarks on one iteration.