from src.automaton import RegexAutomaton
from src.graph import LabelGraph
from src.rpq import perform_rpq
from pygraphblas import lib
import os
import time
import glob

GRAPH_DIRS_ = ['LUBM300', 'uniprotkb_archea_asgard_group_1935183_0',
              'proteomes', 'LUBM1.5M', 'LUBM1M', 'LUBM1.9M',
              'geospecies', 'mappingbased_properties_en', 'LUBM500']
GRAPH_DIRS = ['proteomes', 'mappingbased_properties', 'geospecies']

bench_prefix = 'query_benchmarks/refinedDataForRPQ'

for d_name in GRAPH_DIRS:
    with open(f'query_benchmarks/{d_name}_bench.csv', 'w') as res_f:

        #collected_ = list(
        #    map ( lambda x: x[1],
        #          list(map(lambda x: x.split(', '), res_f.readlines()))
        #    )
        #
        collected = []

        graph_filename = glob.glob(f"{bench_prefix}/{d_name}/*.txt")[0]
        for regex_filename in os.listdir(f'{bench_prefix}/{d_name}/regexes/'):
            if regex_filename in collected:
                print(f'{regex_filename} already done')
            else:
                print(f'Running {d_name} -- {regex_filename}...')
                regex_ = os.path.join(f'{bench_prefix}/{d_name}/regexes/', regex_filename)
                # read Regex from file
                regex_string = open(regex_, 'r').read()
                regex_automaton = RegexAutomaton(regex_string)

                # read GrB matrix from file
                graph = LabelGraph().from_txt(graph_filename)

                # benchmarking 2 methods of transitive closure
                for tc_method in range(2):
                    # read start and end vertices
                    start = list(range(graph.num_vert))
                    end = list(range(graph.num_vert))
                    times = []
                    nvals = 0
                    print(f'Running method {tc_method}...\n')
                    for i in range(5):
                        print(f'Running {i} time...\n')
                        start = time.time_ns()
                        nvals = perform_rpq(graph, regex_automaton,
                                            start, end, bool(tc_method))[1]

                        total_time = time.time_ns() - start

                        
                        # getting time in seconds
                        times.append(
                            total_time / (10 ** 9)
                        )
                    
                    print(f'Writing results...\n')
                    res_f.write(
                        f'{d_name}, {regex_filename}, {tc_method}, {nvals}, {sum(times) / len(times)}\n'
                    )
                    res_f.flush()

                    print(f'{graph_filename} -- {regex_filename}, method {tc_method}: {nvals}, finished \n')
