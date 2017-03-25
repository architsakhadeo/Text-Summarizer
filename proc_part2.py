'''
[subject,verb,object] -> element
for component in element 
'''

from mained import relations
import nltk
import operator
from nltk_tagger_rake_part2 import new_sort_list, content_no_dot
from mained import generate_graphviz_graph
import os
import sys
import re
from nltk_tagger_rake_part2 import word_frequency, word_degree

#Stopwords list
stoplistlines = open("stopwords1.txt",'r').readlines()
stoplist = []
for i in stoplistlines:
	stoplist.append(i.strip().lower())


##for i in relations:
	#print i
#Function to find the total overlap between two strings
def intersection(string1,string2):
	'''
	It outputs the total number of words common to both strings

	Oskar's and Oskar-Schindler would output 0 as no word is present in the other one,
	hence we split on "'" and "-" and spaces and then check for intersections
	'''
	list1 = filter(None, re.split('''[-' ]''',string1)) #List1 = String1 split into words
	list2 = filter(None, re.split('''[-' ]''',string2)) #List2 = String2 split into words
	count = 0
	count_min = 0
	count_max = 0
	if len(list1) <= len(list2):
		min_list = list1
		max_list = list2
	else:
		min_list = list2
		max_list = list1
	for i in range(len(min_list)):
		min_list[i] = min_list[i].lower()
	for i in range(len(max_list)):
		max_list[i] = max_list[i].lower()
	for w in range(len(min_list)):
		if min_list[w] in max_list:
			count_min += 1
	for r in range(len(max_list)):
		if max_list[r] in min_list:
			count_max += 1
	count = max(count_min,count_max)
	return count


#Removes the verbs from the components
'''
Noun + Verb -> Noun
'''
def remove_verbs_merge(component):
	verb = ['VB','VBD','VBG','VBN','VBZ','VBP']
	proper_noun = ['NNP','NNPS']
	component_tokens = nltk.word_tokenize(component)
	component_tagged = nltk.pos_tag(component_tokens)
	string_component = []
	for word,tag in component_tagged:
		if tag not in verb or word.lower() not in stoplist:
			string_component.append(word)
	string_component = ' '.join(string_component)
	return string_component

#Combines multiple similar components with one different output index component
'''
input_list -> OpenIE output before processing
output_list -> OpenIE output after processing
index1, index2 -> indices which have similar words
output_index -> remaining component 

Here, if components at index1 and index2 are mostly same(very high overlap),
and if the component at output_index is similar to other components at the same
position(output_index), then it merges them into one component.
'''
def combine_components(input_list,output_list,index1,index2,output_index):                   
	for i in range(len(input_list)):
		'''
		'part' list includes the list of third components for which there are similar first and second components
		Redundant elements within this list are removed.
		'''
		part = []
		for j in range(len(input_list)):	
			if input_list[i][index1] in input_list[j][index1] or input_list[j][index1] in input_list[i][index1]: 
				if input_list[i][index2] in input_list[j][index2] or input_list[j][index2] in input_list[i][index2]:
					part.append(input_list[j][output_index])
		part1 = part[:]
		for k in range(len(part)):
			z = part[k].split(' ')
			for r in range(len(part)):
				if k != r:
					count = 0
					for a in z:
						if a in part[r]:
							count += 1
					if count == len(z):
						if part[k] in part1:
							part1.remove(part[k])
	
	
		'''
		This combines the processed elements to give a list of non redundant elements
		'''
		for q in part1:
			sub = []
			sub.append(input_list[i][index1])
			if index2 == 1:
				sub.append(input_list[i][index2])
				sub.append(q)
			if index2 == 2:
				sub.append(q)
				sub.append(input_list[i][index2])
			if sub not in output_list:	
				output_list.append(sub)
	return output_list


#Replaces pronouns by previously encountered Proper Nouns
'''

If pronouns are present in the first components as subjects, it replaces it with
the immediately obtained proper noun in the next encountered first component
containing a proper noun. 

'''
pronouns = ['WP', 'PRP', '$WP', '$PRP']
proper_nouns = ['NNP','NN']
for i in range(len(relations)):
	component_tagged = nltk.pos_tag(nltk.word_tokenize(relations[i][0]))	
	if component_tagged[0][1] in pronouns: #**************don't predict the pronoun and proper noun to be in 0th index in both. find the index of the pronoun and propernoun. Put this above before merging first components -> Osker-Schindler and Schindler friendship. Check for the proper noun above. Move this above later. 
		for j in range(i-1,-1,-1):
			if nltk.pos_tag(nltk.word_tokenize(relations[j][0]))[0][1] in proper_nouns:
				relations[i][0] = relations[i][0].replace(component_tagged[0][0],relations[j][0])
				break





#--------------------------------------------------------------------------------------------
#Code to remove verbs and merge has been removed but is located on Github
#in previous commits and is not required.
#--------------------------------------------------------------------------------------------





#Since the input to further task is required in decoded utf8 form
for i in relations:
	i[0] = i[0].decode('utf-8')
	i[1] = i[1].decode('utf-8')
	i[2] = i[2].decode('utf-8')	




#Finds overlap between the subjects found from OpenIE and the keywords obtained from keyword extraction phase
'''
OpenIE output              Keywords  
                                      
a -> b                     a,d  
a -> c
c -> d
d -> e
f -> g


Output is only overlap of first component of OpenIE output and Keywords

a -> b
a -> c
d -> e

'''
common_relations = []
for i in relations:
	for j,k in new_sort_list:
		if intersection(i[0].encode('utf8'),j.encode('utf8')) >= 1 and i not in common_relations:
			common_relations.append(i)


#Replaces words like Schindler with Oskar-Schindler. Basically reduces redundancy by having just Oskar-Schindler instead of Oskar, Schindler, Oskar-Schindler separately.

for i in range(len(common_relations)):
	for z in range(len(common_relations)):
		if i != z: 
			if intersection(common_relations[i][0].lower(),common_relations[z][0].lower()) >= 1:
				component_1_i = common_relations[i][0].split() #component_1_i - 1st component in common_relations[i] i.e. element of first loop
				component_1_z = common_relations[z][0].split() #component_1_z - 1st component in common_relations[j] i.e. element of second loop
				flag = 0
				for component_1_i_word in component_1_i:
					for component_1_z_word in component_1_z:
						if component_1_i_word in component_1_z_word or component_1_z_word in component_1_i_word:
							
							if len(component_1_i_word) >= len(component_1_z_word):
								maxima1 = component_1_i_word
								minima1 = component_1_z_word
								flag = 1
								break
							else:
								maxima1 = component_1_z_word
								minima1 = component_1_i_word
								flag = 1
								break
					if flag == 1:
						break
				if flag == 1:
					if maxima1 not in common_relations[i][0]:
						common_relations[i][0] = common_relations[i][0].replace(minima1,maxima1)


#Combining third components if there are substrings in components. It checks if 1st and 2nd components are similar, then it merges third components for the same

'''
common_relations_rc -> rc is redundancy check. After every redundancy removal, new variable assigned.
'''

common_relations_rc = []
common_relations_rc = combine_components(common_relations,common_relations_rc,0,1,2)


#requires input in decode form
#Combining second components if there are substrings in components. It checks if 1st and 3rd components are similar, then it merges third components for the same
common_relations_rc_1 = []
common_relations_rc_1 = combine_components(common_relations_rc,common_relations_rc_1,0,2,1)

			

#common_relations_rc_1 = newer[:]

for i in common_relations_rc_1:
	i[0] = i[0].encode('utf8')
	i[1] = i[1].encode('utf8')
	i[2] = i[2].encode('utf8')



'''
For the same first and third component, it selects only one element


Oskar-Schindler, saved multiple, Jews
Oskar-Schindler, saved, Jews
Oskar-Schindler, helped, Jews

It selects only one of them
'''


newer1 = []
flag = [0 for i in range(len(common_relations_rc_1))]
for i in range(len(common_relations_rc_1)):
	for j in range(len(common_relations_rc_1)):
		'''
		#Excludes element which has redundant components which have 2nd and third component almost similar.
		'''
		if intersection(common_relations_rc_1[i][1],common_relations_rc_1[i][2]) >= 2:
			flag[i] = 1
			break	
		if flag[i] == 0 and i != j:
			if common_relations_rc_1[i][0] in common_relations_rc_1[j][0] or common_relations_rc_1[j][0] in common_relations_rc_1[i][0]:
				if common_relations_rc_1[i][2] in common_relations_rc_1[j][2] or common_relations_rc_1[j][2] in common_relations_rc_1[i][2]:
					flag[j] = 1
	if flag[i] == 0:
		newer1.append(common_relations_rc_1[i])
	
common_relations_rc_1 = newer1[:]




###############################################################################
'''
EXCESS CODE. DONT REUSE.

#Excludes element which has redundant components which have 2nd and third component almost similar.
common_relations_rc_2 = []
flag = [0 for i in range(len(common_relations_rc_1))]
for i in range(len(common_relations_rc_1)):
	for j in range(len(common_relations_rc_1)):
		if intersection(common_relations_rc_1[i][1],common_relations_rc_1[i][2]) >= 1:
			flag[i] = 1
			break	
	if flag[i] == 0:
		common_relations_rc_2.append(common_relations_rc_1[i])


#common_relations_rc_3 = common_relations_rc_2[:] instead of the next line		
'''
###############################################################################




'''
Removes redudant elements for which 
element1[0] == element2[0]
element1 != element2 
but element1[0]+element1[1]+element1[2] == element2[0]+element2[1]+element2[2]

Removes one of them
'''
common_relations_rc_2 = common_relations_rc_1[:] #Remove this line if the above commented code is used
common_relations_rc_3 = common_relations_rc_2[:]
for i in range(len(common_relations_rc_2)):
	two_three = common_relations_rc_2[i][1] + ' ' + common_relations_rc_2[i][2] #two_three is component two and three appended as a string
	two_three_split = two_three.split()
	for j in range(len(common_relations_rc_2)):
		if common_relations_rc_2[i] != common_relations_rc_2[j] and common_relations_rc_2[i][0] == common_relations_rc_2[j][0]:
			string_trial = common_relations_rc_2[j][1] + ' ' + common_relations_rc_2[j][2]
			string_trial_split = string_trial.split()
			counting = 0
			for k in range(len(two_three_split)):
				 if two_three_split[k] in string_trial_split:
				 	counting += 1
			if counting == len(two_three_split):
				common_relations_rc_3.remove(common_relations_rc_2[i])
				break
			
#Adjacency matrix. To find out the degree of connections for each node
'''
This creates an adjacency matrix and with 
Matrix[A][B] = 1 only if A -> B (A is connected to B).

It should be like a directed graph. A -> B does not imply B -> A necessarily.

Now we find out the total number of connections a node has with other nodes,
which have connections further with more nodes. Thus, all the recursive connections,
a node has have to be calculated for each node.

A -> B
A -> C
B -> D
B -> E
D -> F
G -> I

Here, A is directly connected to B and C and indirectly connected to
D, E and F

Thus A has 5 connections
'''		
list_matrix = []
for i in common_relations_rc_3:
	if i[0] not in list_matrix:
		list_matrix.append(i[0])
	if i[2] not in list_matrix:
		list_matrix.append(i[2])
		
matrix = [[0 for i in list_matrix] for j in list_matrix]

for i in common_relations_rc_3:
	matrix[list_matrix.index(i[0])][list_matrix.index(i[2])] = 1 

'''
count is the list of connections of all nodes
listmatrix is the list of all nodes
'''
count = [1 for i in list_matrix]  #Stores degree of connection 
for i in range(len(matrix)):
	major = []
	for j in range(len(matrix[i])):
		if matrix[i][j] == 1:
			major.append(j)
	if major == []:
		continue
	z = 0
	while True:
		for k in range(len(matrix)):	
			if matrix[major[z]][k] == 1 and k not in major:
				major.append(k)
		if z == len(major) - 1:
			break
		z += 1
	count[i] += len(major)



combo = dict(zip(list_matrix,count))
list_of_elements_combo = sorted(combo.items(),key=operator.itemgetter(1),reverse=False) #ascending
keys = [i[0] for i in list_of_elements_combo]
values = [i[1] for i in list_of_elements_combo]

for i in common_relations_rc_3:
	if i[0] == '' or i[1] == '' or i[2] == '':
		common_relations_rc_3.remove(i)

'''
This generates graph by graphviz with the elements from common_relations_rc_3
such that

                  ACTION
SUBJECT -------------------------> OBJECT


'''	
generate_graphviz_graph(common_relations_rc_3,verbose=True)

#generate_graphviz_graph(common_relations_rc_3,verbose=True)

os.system('mv /tmp/openie/out.png ./')


'''
Content written in sorter.txt. Imported from nltk_tagger_rake.py. Selects top 1/3rd statements which occur first in order of appearance. Scores for each sentence are calculated on the basis of presence of top nodes. Sum of these degrees of nodes is equivalent to score of sentence
'''
content_no_dot = content_no_dot.split('.')
scored_sent = [0 for i in range(len(content_no_dot))]



#Calculates scores for each sentences
'''
Score of a sentence = Sum(Number of connections for each node present in it)
'''
for i in range(len(content_no_dot)):
	if content_no_dot[i].lower() not in stoplist:	
		for k in range(len(keys)):
			if intersection(content_no_dot[i],keys[k]) >= 1:
				scored_sent[i] += values[k]


for i in content_no_dot:
	j = i.strip()
	if j == '':
		content_no_dot.remove(i)

index_sent = [i for i in range(len(content_no_dot))]	
sent_dict = dict(zip(index_sent,scored_sent))



#Sorts sentences based on decreasing order of scores
sent_sorted = sorted(sent_dict.items(),key=operator.itemgetter(1),reverse=True)



#Selects top 1/3rd sentences
#sent_sorted_20 = dict(sent_sorted[:len(content_no_dot)/3])
if len(content_no_dot)/3.5 >= 20:	
	sent_sorted_top = dict(sent_sorted[:20])
else:
	sent_sorted_top = dict(sent_sorted[:int(len(content_no_dot)/3.5)])
	
	

#Sorts these top 1/3rd obtained sentences in increasing order of their appearance in the input text 
inorder_sent_sorted_top = sorted(sent_sorted_top.items(),key=operator.itemgetter(0),reverse=False)


print '\n\n\n\n\n\nSummary is\n\n\n'
for index,score in inorder_sent_sorted_top:
	print content_no_dot[index].strip().replace('<dot> ','.') + '.'


for i in common_relations_rc_3:
	for j in range(len(i)):
		i[j] = i[j].decode('utf-8')
		

#To draw graph by networkx
import networkx as nx
import matplotlib.pyplot as plt



def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)

    # show graph
    plt.show()

#graph = [(0, 1), (1, 5), (1, 7), (4, 5), (4, 8), (1, 6), (3, 7), (5, 9),
#         (2, 4), (0, 4), (2, 5), (3, 6), (8, 9)]

graph = []

for i in common_relations_rc_3:
	graph.append((i[0],i[2]))


labels = []
for i in common_relations_rc_3:
	labels.append(i[1])

# you may name your edge labels
#labels = map(chr, range(65, 65+len(graph)))
draw_graph(graph, labels)

# if edge labels is not specified, numeric labels (0, 1, 2...) will be used
#draw_graph(graph)






