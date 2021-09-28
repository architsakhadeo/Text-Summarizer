# Copyright (c) 2016, Philippe Remy <github: philipperemy>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from __future__ import print_function

import os
from argparse import ArgumentParser
from subprocess import Popen
from sys import argv
from sys import stderr
import nltk

stoplistlines = open("stopwords1.txt",'r').readlines()
stoplist = []
for i in stoplistlines:
	stoplist.append(i.strip().lower())

JAVA_BIN_PATH = 'java'
DOT_BIN_PATH = 'dot'
STANFORD_IE_FOLDER = 'stanford-openie'

tmp_folder = '/tmp/openie/'
if not os.path.exists(tmp_folder):
	os.makedirs(tmp_folder)


def arg_parse():
	arg_p = ArgumentParser('Stanford IE Python Wrapper')
	arg_p.add_argument('-f', '--filename', type=str, default=None)
	arg_p.add_argument('-v', '--verbose', action='store_true')
	arg_p.add_argument('-g', '--generate_graph', action='store_true')
	return arg_p


def debug_print(log, verbose):
	if verbose:
		print(log)


def process_entity_relations(entity_relations_str, verbose=True):
	# format is ollie.
	entity_relations = list()
	for s in entity_relations_str:
		entity_relations.append(s[s.find("(") + 1:s.find(")")].split(';'))
	return entity_relations


def generate_graphviz_graph(entity_relations, verbose=True):
	"""digraph G {
	# a -> b [ label="a to b" ];
	# b -> c [ label="another label"];
	}"""
	graph = list()
	graph.append('digraph {')
	for er in entity_relations:
		graph.append('"{}" -> "{}" [ label="{}" ];'.format(er[0], er[2], er[1]))
	graph.append('}')

	out_dot = tmp_folder + 'out.dot'
	with open(out_dot, 'w') as output_file:
		output_file.writelines(graph)

	out_png = tmp_folder + 'out.png'
	command = '{} -Tpng {} -o {}'.format(DOT_BIN_PATH, out_dot, out_png)
	debug_print('Executing command = {}'.format(command), verbose)
	dot_process = Popen(command, stdout=stderr, shell=True)
	dot_process.wait()
	assert not dot_process.returncode, 'ERROR: Call to dot exited with a non-zero code status.'
	print('Wrote graph to {} and {}'.format(out_dot, out_png))


def stanford_ie(input_filename, verbose=True, generate_graphviz=True):
	out = tmp_folder + 'out.txt'
	input_filename = input_filename.replace(',', ' ')

	new_filename = ''
	for filename in input_filename.split():
		if filename.startswith('/'):  # absolute path.
			new_filename += '{} '.format(filename)
		else:
			new_filename += '../{} '.format(filename)

	absolute_path_to_script = os.path.dirname(os.path.realpath(__file__)) + '/'
	command = 'cd {};'.format(absolute_path_to_script)
	command += 'cd {}; {} -mx4g -cp "stanford-openie.jar:stanford-openie-models.jar:lib/*" ' \
			'edu.stanford.nlp.naturalli.OpenIE {} -format ollie > {}'. \
	format(STANFORD_IE_FOLDER, JAVA_BIN_PATH, new_filename, out)

	if verbose:
		debug_print('Executing command = {}'.format(command), verbose)
		java_process = Popen(command, stdout=stderr, shell=True)
	else:
		java_process = Popen(command, stdout=stderr, stderr=open(os.devnull, 'w'), shell=True)
	java_process.wait()
	assert not java_process.returncode, 'ERROR: Call to stanford_ie exited with a non-zero code status.'

	with open(out, 'r') as output_file:
		results_str = output_file.readlines()
	os.remove(out)

	results = process_entity_relations(results_str, verbose)
	if generate_graphviz:
		generate_graphviz_graph(results, verbose)

	return results

args = argv[:]
arg_p = arg_parse().parse_args(args[1:])
filename = arg_p.filename
verbose = arg_p.verbose
generate_graphviz = arg_p.generate_graph
if filename is None:
	print('please provide a text file containing your input. Program will exit.')
	exit(1)
if verbose:
	debug_print('filename = {}'.format(filename), verbose)
global entities_relations
entities_relations = stanford_ie(filename, verbose, generate_graphviz)
global relations
	


pronouns = ['WP', 'PRP', '$WP', '$PRP','PRP$']
proper_nouns = ['NNP','NN']

#female = ['girl']
#female_pronoun = ['she','her']


#Requires mapping for both gender pronouns to replace pronouns with apt proper nouns
'''
for i in range(len(entities_relations)):
	a = nltk.pos_tag(nltk.word_tokenize(entities_relations[i][0]))	
	print (entities_relations[i][0],a[0][1])
	if a[0][1] in pronouns and entities_relations[i][0] not in female_pronoun:
		for j in range(i-1,-1,-1):
			print (nltk.pos_tag(nltk.word_tokenize(entities_relations[j][0]))[0][1], entities_relations[j][0])
			if nltk.pos_tag(nltk.word_tokenize(entities_relations[j][0]))[0][1] in proper_nouns:
				if entities_relations[i][0] not in female_pronoun:
					entities_relations[i][0] = entities_relations[j][0]
				print (entities_relations[i][0], entities_relations[j][0])
				break
	if a[0][1] in pronouns and entities_relations[i][0] in female_pronoun:   
		for j in range(i-1,-1,-1):
			for k in female:
				if k in entities_relations[j][0]:
					entities_relations[i][0] = entities_relations[j][0]
					break
					print (entities_relations[i][0], entities_relations[j][0])
'''
"""************
#Replaces pronoun with previous propernoun             
for i in range(len(entities_relations)):
	a = nltk.pos_tag(nltk.word_tokenize(entities_relations[i][0]))
	if entities_relations[i][0] == 'his friendship':
		print (a, a[0][0],a[0][1]	)
	#print (entities_relations[i][0],a[0][1])
	if a[0][1] in pronouns:     #**************don't predict the pronoun and proper noun to be in 0th index in both. find the index of the pronoun and propernoun
		for j in range(i-1,-1,-1):
			#print (nltk.pos_tag(nltk.word_tokenize(entities_relations[j][0]))[0][1], entities_relations[j][0])
			if nltk.pos_tag(nltk.word_tokenize(entities_relations[j][0]))[0][1] in proper_nouns:
				entities_relations[i][0] = entities_relations[i][0].replace(a[0][0],entities_relations[j][0])       
				#print (entities_relations[i][0], entities_relations[j][0])
				break
***********"""
'''
for i in entities_relations:	
	if i[0] in relations:	
		relations[i[0]].append(i[2])
	else:
		relations[i[0]] = [i[2]] 

#Open IE output
for i, v in relations.items():
	v = [j.decode('utf-8') for j in v]
	i = [i.decode('utf-8')]
'''

relations = entities_relations[:]
for i in relations:
	print (i)
