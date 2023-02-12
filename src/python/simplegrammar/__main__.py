from .grammar import SimpleGrammar
import json
import sys
import os


input_string = sys.argv[1]

if os.path.isfile(input_string):
	input_json = input_string
	with open(input_json, 'r') as f:
	    grammar_input = json.load(f)
else:
	if input_string[0] == "[":
		grammar_input = input_string.replace("[", "").replace("]", "").split(",")
	else:
		grammar_input = json.loads(input_string)

print(SimpleGrammar.parse(grammar_input))
