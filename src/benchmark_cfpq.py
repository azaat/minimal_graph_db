from src.grammar_cnf import GrammarCNF
from src.graph import LabelGraph
from src.cfpq import cfpq_hellings, cfpq_matrix_mult, cfpq_tensor_product
from pygraphblas import lib
import os
import time
import glob

GRAPH_DIRS = ['WorstCase']

bench_prefix = 'cfpq_benchmarks/DataForFLCourse'
graph_dir = 'graphs'
grammar_dir = 'grammars'

for d_name in GRAPH_DIRS:
    for graph_filename in os.listdir(f"{bench_prefix}/{d_name}/{graph_dir}/"):
        graph_path = os.path.join(f'{bench_prefix}/{d_name}/{graph_dir}/', graph_filename)
        with open(f'{bench_prefix}/{d_name}/{graph_filename}_bench.csv', 'w') as res_f:
            for cfg_filename in os.listdir(f'{bench_prefix}/{d_name}/{grammar_dir}/'):
                print(f'Running {graph_path} -- {cfg_filename}...')
                cfg_path = os.path.join(f'{bench_prefix}/{d_name}/{grammar_dir}/', cfg_filename)
                # read CFG from file
                cnf = GrammarCNF.from_txt(cfg_path)
                
                # read GrB matrix from file
                graph = LabelGraph().from_txt(graph_path)


                # benchmarking hellings
                times = []
                nvals = 0
                method = 'hellings';
                print(f'Running method {method}...\n')
                for i in range(1):
                    print(f'Running {i} time...\n')
                    start = time.time_ns()
                    nvals = cfpq_hellings(graph, cnf).nvals;

                    total_time = time.time_ns() - start
                    
                    # getting time in μs
                    times.append(
                        total_time // (10 ** 3)
                    )
                
                print(f'Writing results...\n')
                res_f.write(
                    f'{graph_path}, {cfg_filename}, {method}, {nvals}, {sum(times) / len(times)}\n'
                )
                res_f.flush()
                print(f'{graph_path} -- {cfg_filename}, {method}: {nvals}, finished \n')
                


                # benchmarking mult
                times = []
                nvals = 0
                method = 'mult';
                print(f'Running method {method}...\n')
                for i in range(1):
                    print(f'Running {i} time...\n')
                    start = time.time_ns()
                    nvals = cfpq_matrix_mult(graph, cnf).nvals;

                    total_time = time.time_ns() - start
                    
                    # getting time in μs
                    times.append(
                        total_time // (10 ** 3)
                    )
                
                print(f'Writing results...\n')
                res_f.write(
                    f'{graph_path}, {cfg_filename}, {method}, {nvals}, {sum(times) / len(times)}\n'
                )
                res_f.flush()
                print(f'{graph_path} -- {cfg_filename}, {method}: {nvals}, finished \n')



                # benchmarking tensor
                times = []
                nvals = 0
                method = 'tensor';
                print(f'Running method {method}...\n')
                for i in range(1):
                    print(f'Running {i} time...\n')
                    start = time.time_ns()
                    nvals = cfpq_tensor_product(graph, cnf).nvals;

                    total_time = time.time_ns() - start
                    
                    # getting time in μs
                    times.append(
                        total_time // (10 ** 3)
                    )
                
                print(f'Writing results...\n')
                res_f.write(
                    f'{d_name}, {cfg_filename}, {method}, {nvals}, {sum(times) / len(times)}\n'
                )
                res_f.flush()

                print(f'{graph_filename} -- {cfg_filename}, {method}: {nvals}, finished \n')


                