from src.automaton import RegexAutomaton
from src.graph import LabelGraph
from src.rpq import perform_rpq
from pygraphblas import lib
import os
import time
import glob

GRAPH_DIRS = ['LUBM300', 'uniprotkb_archea_asgard_group_1935183_0',
              'proteomes', 'LUBM1.5M', 'LUBM1M', 'LUBM1.9M',
              'geospecies', 'mappingbased_properties_en', 'LUBM500']


prefix = 'query_benchmarks/refinedDataForRPQ'

for d_name in GRAPH_DIRS:
    with open(f'query_benchmarks/{d_name}_bench.csv', 'w') as res_f:
        graph_filename = glob.glob(f"{prefix}/{d_name}/*.txt")[0]
        for regex_filename in os.listdir(f'{prefix}/{d_name}/regexes/'):
            print(f'Running {d_name} -- {regex_filename}...')
            regex_ = os.path.join(f'{prefix}/{d_name}/regexes/', regex_filename)
            # read Regex from file
            regex_string = open(regex_, 'r').read()
            regex_automaton = RegexAutomaton(regex_string)

            # read GrB matrix from file
            graph = LabelGraph().from_txt(graph_filename)

            # read start and end vertices
            start = list(range(graph.num_vert))
            end = list(range(graph.num_vert))
            times = []
            for i in range(5):
                print(f'Running {i}-th time...\n')
                start_time = time.time_ns()
                r_m = perform_rpq(graph, regex_automaton, start, end)
                end_time = time.time_ns()
                
                times.append((end_time - start_time) // (10 ** 3))
            print(f'Writing results...\n')
            with open(f'query_benchmarks/{d_name}_{regex_filename}_results.txt', 'w') as f:
                res_f.write(f'{d_name}, {regex_filename}, {r_m.nvals}, {min(times)}, {max(times)}, {sum(times) / len(times)}\n')
                for v, to, _ in zip(*r_m.select(lib.GxB_NONZERO).to_lists()):
                    f.write(f'{v} {to}\n')
            res_f.flush()

            print(f'{graph_filename} -- {regex_filename} {r_m.nvals}, finished \n')
