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

Experimental report can be found in Analysis.pdf. CSV files used in analysis are in ./query_benchmarks.

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

## Assignment_7: Graph DB Query Language Syntax

### Syntax documentation

Statements in the script should be separated with ``` ; ```, tokens and keywords - with arbitrary amount of whitespace. Strings are defined like this: ```"example_string"```, supported string characters: (```/```, ```.```, ```_```, ```0-9```, ```a-z```)
. Int type describes natural numbers. 

Description of the possible database statements:
- ```connect [PATH]``` - connects to the database with the specified path, path should be of string type.
  Example usage:
  ```
  connect "azat/home/db" ;
  ```

- ```select [TARGET] from [GRAPH]``` - selects specified target from the graph or graph expression.

  **Possible ```[TARGET]``` values:**
  - ```edges``` - if you need to select a set of edges
  - ```filter [EDGE EXPRESSION] with [PREDICATE]``` - if you need to filter edges with some predicate. Edge expression can be either ```edges``` or filter of edges.

    - Predicate format:
      ```satisfies [BOOLEAN EXPRESSION]```
      For the triple (v, label, u) returns boolean value for a combination of boolean predicates of the form:

      ```
      isStart [VERTEX NAME]
      isFinal [VERTEX NAME]
      labelIs [LABEL NAME]
      ```
      where isStart, isFinal return whether vertex is start or final. Vertex and variable names should start with letter character, the rest of the name can contain numbers.

      Combined expressions with these predicates can be specified with ```and```, ```or```,  ```not```.

      Example usage:
      ```
      select filter edges with 
            ( u, l, v ) satisfies l labelIs "ar" or ( isStart u and isFinal v ) 
                    from name "sparsegraph" ;
      ```

  - ```count [EDGE EXPRESSION]``` - if you need to select the count of edges. Edge expression can be either ```edges``` or filter of edge expression.
  
  **```GRAPH``` expression can be one of:**
    - ```name [GRAPH NAME]```
    - ```query [PATTERN]```
      - ```PATTERN``` represesnts a non-empty user-defined reqular expression.
      Supported operators are ```alt``` -alternative, ```plus``` - one or more occurences, ```star``` - * operator, ```opt``` - optional character. User-defined epsilon is ```ptEps```. Both terminals and nonterminals are defined asTerminals are preceded with ```term``` keyword, nonterminals - with ```var```.

      Example usage: ```query term "a" concat var "s" concat term "b" concat var "s" ;```

    - ```[GRAPH EXPRESSION] intersect [GRAPH EXPRESSION] ``` - intersection of graph automata
    - ```startAndFinal [VERTICES] [VERTICES] of [GRAPH EXPRESSION]``` - specifies start and final vertices for the graph or graph expression
      -  ```VERTICES``` can be specified as a set of numbers (```set 1 2 3 4 ...```) or as a range: ```range ( start , end )```

- ```define [PATTERN] as [PATTERN NAME] of [GRAPH EXPRESSION]``` - this statement should be used to define named patterns to build grammar productions.

## Asssignment 8

Minor **syntax updates**:

1. In the patterns ```term "a"```, ```var "b"``` should now be used as ```term("a")```, ```var("b")```. Same with ```labelIs, isFinal, isStart``` predicates (e.g. ```isStart(u)```)
2. Now you can also specify regex pattern with characters  ```+, ?, *, .```, examples: 
    ```
    term("a").var("s").term("b").var("s")
    
    define term("a")*.term("b")?.var("s")+ as "my_pattern" ;
    
    ```
3. Set syntax: ```set(1,2,3,5)```

To use antlr_parser.py, install antlr, then run ```conda install -c conda-forge antlr-python-runtime ```

