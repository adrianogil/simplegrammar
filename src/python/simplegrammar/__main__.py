from .grammar import SimpleGrammar

import argparse
import json
import os


def load_grammar_input(input_string):
    if os.path.isfile(input_string):
        with open(input_string, 'r') as f:
            return json.load(f)

    if input_string[0] == "[":
        return input_string.replace("[", "").replace("]", "").split(",")

    return json.loads(input_string)


def build_parser():
    parser = argparse.ArgumentParser(description="Expand a simplegrammar grammar")
    parser.add_argument("grammar", help="JSON grammar, list expression, or path to a JSON file")
    parser.add_argument("--seed", help="seed used for deterministic grammar expansion")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    grammar_input = load_grammar_input(args.grammar)

    print(SimpleGrammar.parse(grammar_input, seed=args.seed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
