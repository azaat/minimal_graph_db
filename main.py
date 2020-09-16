from src.automaton import RegexAutomaton
from src.graph import LabelGraph
import argparse
from src.rpq import perform_rpq


def main():
    parser = argparse.ArgumentParser(description='Basic graph DB')
    parser.add_argument(
        '--graph', required=True, type=str,
        help='path to graph file'
    )
    parser.add_argument(
        '--regex', required=True, type=str,
        help='path to regex file'
    )
    parser.add_argument(
        '--start', required=False, type=str,
        help='path to given starting vertices'
    )
    parser.add_argument(
        '--end', required=False, type=str,
        help='path to given end vertices'
    )
    args = parser.parse_args()

    # read Regex from file
    regex_string = open(args.regex, 'r').read()
    regex_automaton = RegexAutomaton(regex_string)

    # read GrB matrix from file
    graph = LabelGraph().from_txt(args.graph)

    # read start and end vertices
    start = []
    if (args.start is not None):
        with open(args.start, 'r') as f:
            for line in f:
                start.append(int(line))
    else:
        start = list(range(graph.num_vert))

    end = []
    if (args.end is not None):
        with open(args.end, 'r') as f:
            for line in f:
                end.append(int(line))
    else:
        end = list(range(graph.num_vert))

    perform_rpq(graph, regex_automaton, start, end)


if __name__ == "__main__":
    main()
