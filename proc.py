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

#Function to find the total overlap between two strings
def intersection(string1,string2):
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
def remove_verbs_merge(component):
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
'''
def combine_components(input_list,output_list,index1,index2,output_index):                   
	for i in range(len(input_list)):
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
pronouns = ['WP', 'PRP', '$WP', '$PRP']
proper_nouns = ['NNP','NN']
for i in range(len(relations)):
	component_tagged = nltk.pos_tag(nltk.word_tokenize(relations[i][0]))	
	if component_tagged[0][1] in pronouns: #**************don't predict the pronoun and proper noun to be in 0th index in both. find the index of the pronoun and propernoun. Put this above before merging first components -> Osker-Schindler and Schindler friendship. Check for the proper noun above. Move this above later. 
		for j in range(i-1,-1,-1):
			if nltk.pos_tag(nltk.word_tokenize(relations[j][0]))[0][1] in proper_nouns:
				relations[i][0] = relations[i][0].replace(component_tagged[0][0],relations[j][0])
				break



verb = ['VB','VBD','VBG','VBN','VBZ','VBP']
proper_noun = ['NNP','NNPS']

for i in relations:
	#removing verbs from first components and merges them if they are same after removal of verbs
	str_component_one = remove_verbs_merge(i[0])
	i[0] = str_component_one.replace(" '","'").decode('utf-8')
	#removing verbs from first components and merges them if they are same after removal of verbs
	str_component_three = remove_verbs_merge(i[2])
	i[2] = str_component_three.replace(" '","'").decode('utf-8')
		

#Finds overlap between the subjects found from OpenIE and the keywords obtained from keyword extraction phase
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
				comp_1_i = common_relations[i][0].split()
				comp_1_z = common_relations[z][0].split()
				flag = 0
				for comp_1_i_word in comp_1_i:
					for comp_1_z_word in comp_1_z:
						if comp_1_i_word in comp_1_z_word or comp_1_z_word in comp_1_i_word:
							
							if len(comp_1_i_word) >= len(comp_1_z_word):
								maxima1 = comp_1_i_word
								minima1 = comp_1_z_word
								flag = 1
								break
							else:
								maxima1 = comp_1_z_word
								minima1 = comp_1_i_word
								flag = 1
								break
					if flag == 1:
						break
		
				if maxima1 not in common_relations[i][0]:
					common_relations[i][0] = common_relations[i][0].replace(minima1,maxima1)


#Combining third components if there are substrings in components. It checks if 1st and 2nd components are similar, then it merges third components for the same
list_of_elements = []
list_of_elements = combine_components(common_relations,list_of_elements,0,1,2)


#requires input in decode form
#Combining second components if there are substrings in components. It checks if 1st and 3rd components are similar, then it merges third components for the same
list_of_elements_1 = []
list_of_elements_1 = combine_components(list_of_elements,list_of_elements_1,0,2,1)

for i in list_of_elements_1:
	i[0] = i[0].encode('utf8')
	i[1] = i[1].encode('utf8')
	i[2] = i[2].encode('utf8')

#Excludes element which has redundant components which have 2nd and third component almost similar.
list_of_elements_2 = []
flag = [0 for i in range(len(list_of_elements_1))]
for i in range(len(list_of_elements_1)):
	for j in range(len(list_of_elements_1)):
		if intersection(list_of_elements_1[i][1],list_of_elements_1[i][2]) >= 1:
			flag[i] = 1
			break	
	if flag[i] == 0:
		list_of_elements_2.append(list_of_elements_1[i])
		


#Removes redudant elements for which element1 != element2 but element1[0]+element1[1]+element1[2] == element2[0]+element2[1]+element2[2]
list_of_elements_3 = list_of_elements_2[:]
for i in range(len(list_of_elements_2)):
	two_three = list_of_elements_2[i][1] + ' ' + list_of_elements_2[i][2]
	two_three_split = two_three.split()
	for j in range(len(list_of_elements_2)):
		if list_of_elements_2[i] != list_of_elements_2[j] and list_of_elements_2[i][0] == list_of_elements_2[j][0]:
			string_trial = list_of_elements_2[j][1] + ' ' + list_of_elements_2[j][2]
			string_trial_split = string_trial.split()
			counting = 0
			for k in range(len(two_three_split)):
				 if two_three_split[k] in string_trial_split:
				 	counting += 1
			if counting == len(two_three_split):
				list_of_elements_3.remove(list_of_elements_2[i])
				break
			
#Adjacency matrix. To find out the degree of connections for each node	
list_matrix = []
for i in list_of_elements_3:
	if i[0] not in list_matrix:
		list_matrix.append(i[0])
	if i[2] not in list_matrix:
		list_matrix.append(i[2])
		
matrix = [[0 for i in list_matrix] for j in list_matrix]

for i in list_of_elements_3:
	matrix[list_matrix.index(i[0])][list_matrix.index(i[2])] = 1 


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

for i in list_of_elements_3:
	if i[0] == '' or i[1] == '' or i[2] == '':
		list_of_elements_3.remove(i)
	print i
	
generate_graphviz_graph(list_of_elements_3,verbose=True)

#generate_graphviz_graph(list_of_elements_3,verbose=True)

os.system('mv /tmp/openie/out.png ./')


#Content written in sorter.txt. Imported from nltk_tagger_rake.py. Selects top 1/3rd statements which occur first in order of appearance. Scores for each sentence are calculated on the basis of presence of top nodes. Sum of these degrees of nodes is equivalent to score of sentence
content_no_dot = content_no_dot.split('.')
scored_sent = [0 for i in range(len(content_no_dot))]
#Calculates scores for each sentences
for i in range(len(content_no_dot)):
	print '*********',content_no_dot[i],'*********'
	if content_no_dot[i].lower() not in stoplist:	
		for k in range(len(keys)):
			if intersection(content_no_dot[i],keys[k]) >= 1:
				scored_sent[i] += values[k]
				print '------------',content_no_dot[i], keys[k], intersection(content_no_dot[i],keys[k]), values[k]

for i in range(len(content_no_dot)):	
	print content_no_dot[i], scored_sent[i], '\n'

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
if len(content_no_dot)/4 >= 20:	
	sent_sorted_20 = dict(sent_sorted[:20])
else:
	sent_sorted_20 = dict(sent_sorted[:int(len(content_no_dot)/3.5)])
#Sorts these top 1/3rd obtained sentences in increasing order of their appearance in the input text 
inorder_sent_sorted_20 = sorted(sent_sorted_20.items(),key=operator.itemgetter(0),reverse=False)

for index,score in inorder_sent_sorted_20:
	#print score, '--->', content_no_dot[index],'\n'
	print content_no_dot[index].strip().replace('<dot>','.') + '.'

