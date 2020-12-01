from src.antlr_utils import generate_dot
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Graph DB query language script to DOT converter')
    parser.add_argument(
        '--script', required=True, type=str,
        help='path to script file'
    )
    parser.add_argument(
        '--output', required=True, type=str,
        help='path to output DOT file'
    )
    parser.add_argument('--view', action='store_true')
    args = parser.parse_args()
    script = open(args.script, 'r').read()
    out_path = args.output
    generate_dot(script, out_path, args.view)
