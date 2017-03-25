'''
[subject,verb,object] -> element
for component in element 
'''
from copy import deepcopy
from mained import relations
import nltk
import operator
from nltk_tagger_rake import new_sort_list, content_no_dot
from mained import generate_graphviz_graph
import os
import sys
import re
from nltk_tagger_rake import word_frequency, word_degree




#Stopwords list
stoplistlines = open("stopwords1.txt",'r').readlines()
stoplist = []
for i in stoplistlines:
	stoplist.append(i.strip().lower())


complete_text = content_no_dot[:]
complete_text_list = complete_text.split('.')

relations_pronouns = deepcopy(relations)



	
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



#Compares components at multiple indices to merge them into one thus decreasing the redundancy
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




#Since the input to further task is required in encoded utf8 form
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


'''
imp_nodes contains the top 3 most connected words.

We use these nodes to winnow further the input text to the text
which only includes the sentences containing these words or
related/referring pronouns.
'''
imp_nodes = keys[-3:] 

flagged_sentences = [0 for i in range(len(relations_pronouns))]
reduced_text_list = []



#Checks for sentences with pronouns replaced by imp_nodes also
'''
Identifies the elements in which the pronouns were replaced by one of the
words in imp_nodes. Marks the flag against them.

flag_sentences = flags against the elements in relations_pronouns
'''
for i in common_relations_rc_3:
	tagflag = 0
	for j in imp_nodes:
		if intersection(j,i[0]) >= 1 or intersection(j,i[1]) >= 1 or intersection(j,i[2]) >= 1:
			for k in relations_pronouns:
				if flagged_sentences[relations_pronouns.index(k)] == 0:	
					if k[1] in i[1] or i[1] in k[1]:
						if k[2] in i[2] or i[2] in k[2]:	
							flagged_sentences[relations_pronouns.index(k)] = 1
							tagflag = 1
							break
						
					
			if tagflag == 1:
				break
		
	
#for i in relations_pronouns:
	#print i, flagged_sentences[relations_pronouns.index(i)]




#Checks only for sentences with the imp_nodes
'''
Simply checks and marks the flag of the sentence if it contains any of
the imp_nodes words
'''
flagged_all = [0 for i in range(len(complete_text_list))]
for i in complete_text_list:
	count = 0
	for j in imp_nodes:
		if intersection(j,i):
			count += 1
	if count != 0:
		flagged_all[complete_text_list.index(i)] = 1

'''
For pronouns which are replaced by one of the imp_nodes earlier in the stage,
it identifies which sentence they belonged to and marks the flag of that
sentence.
'''
k = 0
for i in complete_text_list:
	if flagged_all[complete_text_list.index(i)] == 1:
		continue
	for j in range(k,len(flagged_sentences)):
		if flagged_sentences[j] == 1:
			if relations_pronouns[j][0] in i and relations_pronouns[j][1] in i and relations_pronouns[j][2] in i:
				 flagged_all[complete_text_list.index(i)] = 1
				 k = j
				 break

reduced_text = ''
for i in range(len(flagged_all)):
	if flagged_all[i] == 1:
		reduced_text += complete_text_list[i].strip() + '. '


'''
This text now includes only the important sentences containing the words in imp_nodes
or the sentences with pronouns which were replaced by one of the words in imp_nodes.
 
Writes to sorter_part2.txt which will be used as an input to the text summarizer program again.
'''
new_text = open('sorter_part2.txt','w+')


'''
This text does not contain paragraphs and hence we cannot extract 3-5 number
of keyphrases per paragraph in the next step. We instead take a large number
of keyphrases around 25 in this sole paragraph.
'''
#without paragraphs. All sentences lie in one para here
new_text.write(reduced_text.replace('<dot>','.'))

