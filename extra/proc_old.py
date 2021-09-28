from mained import relations
import nltk
import operator
from nltk_tagger_rake import new_sort_list, content_no_dot
from mained import generate_graphviz_graph
import os
import sys
import re
sys.setrecursionlimit(50000)
from nltk_tagger_rake import word_frequency, word_degree
stoplistlines = open("stopwords1.txt",'r').readlines()
stoplist = []
for i in stoplistlines:
	stoplist.append(i.strip().lower())


def intersection(string1,string2):
	#list1 = string1.split()
	#list2 = string2.split()	
	list1 = filter(None, re.split('''[-' ]''',string1))
	list2 = filter(None, re.split('''[-' ]''',string2))
	count = 0
	count1 = 0
	count2 = 0
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
			count1 += 1
	for r in range(len(max_list)):
		if max_list[r] in min_list:
			count2 += 1
	count = max(count1,count2)
	return count

"""
def intersection(string1,string2):
	#list1 = string1.split()
	#list2 = string2.split()	
	list1 = filter(None, re.split('''[-' ]''',string1))
	list2 = filter(None, re.split('''[-' ]''',string2))
	count = 0
	count1 = 0
	count2 = 0
	#if len(list1) <= len(list2):
	#	min_list = list1
	#	max_list = list2
	#else:
	#	min_list = list2
	#	max_list = list1
	for i in range(len(list1)):
		list1[i] = list1[i].lower()
	for i in range(len(list2)):
		list2[i] = list2[i].lower()
	for w in range(len(list1)):
		for q in range(len(list2)):	
			if list1[w] in list2[q]:
				count1 += 1
	for w in range(len(list2)):
		for q in range(len(list1)):
			if list2[w] in list1[q]:
				count2 += 1
	count = max(count1,count2)
	return count
"""


pronouns = ['WP', 'PRP', '$WP', '$PRP']
proper_nouns = ['NNP','NN']
for i in range(len(relations)):
	a = nltk.pos_tag(nltk.word_tokenize(relations[i][0]))	
	#print (entities_relations[i][0],a[0][1])
	if a[0][1] in pronouns: #**************don't predict the pronoun and proper noun to be in 0th index in both. find the index of the pronoun and propernoun. Put this above before merging first components -> Osker-Schindler and Schindler frienship. Check for the proper noun above. Move this above later. 
		for j in range(i-1,-1,-1):
			#print (nltk.pos_tag(nltk.word_tokenize(entities_relations[j][0]))[0][1], entities_relations[j][0])
			if nltk.pos_tag(nltk.word_tokenize(relations[j][0]))[0][1] in proper_nouns:
				relations[i][0] = relations[i][0].replace(a[0][0],relations[j][0])
				#print (entities_relations[i][0], entities_relations[j][0])
				break


#removing verbs from first components and merges them if they are same after removal of verbs
verb = ['VB','VBD','VBG','VBN','VBZ','VBP']
proper_noun = ['NNP','NNPS']
for i in relations:
	p = nltk.word_tokenize(i[0])
	p = nltk.pos_tag(p)
	str1 = []
	for j,k in p:
		if k not in verb or j.lower() not in stoplist:
			str1.append(j)
	str1 = ' '.join(str1)
	i[0] = str1.decode('utf-8')

for i in relations:
	p = nltk.word_tokenize(i[2])
	p = nltk.pos_tag(p)
	str1 = []
	for j,k in p:
		if k not in verb or j.lower() not in stoplist:
			str1.append(j)
	str1 = ' '.join(str1)
	i[2] = str1.replace(" '","'").decode('utf-8')	

	

print "\n\n\n\n\n\n\n",new_sort_list,'\n\n\n\n\n\n\n'




print "------------------------------------------------------------------------------------------------------------------------------------------"
print relations

print "------------------------------------------------------------------"
print "Relations"
print "------------------------------------------------------------------"
'''
common_relations = []
for i in relations:
	for j,k in new_sort_list:
		if i[0].encode('utf8') in j.encode('utf8') and i not in common_relations:
			common_relations.append(i)
		if j.encode('utf8') in i[0].encode('utf8') and i not in common_relations:
			common_relations.append(i)
'''

common_relations = []
for i in relations:
	for j,k in new_sort_list:
		if intersection(i[0].encode('utf8'),j.encode('utf8')) >= 1 and i not in common_relations:
			common_relations.append(i)

for i in common_relations:
	print i	

def substrings(s):
    for i in range(len(s)):
        for j in range(i, len(s)):
            yield s[i:j+1]

def intersect(s1, s2):
    return set(substrings(s1)) & set(substrings(s2))


for i in range(len(common_relations)):
	'''p = nltk.word_tokenize(relations[i][0])           ####Check for proper noun and then replace
	p = nltk.pos_tag(p)
	for j,k in p:
		if j in proper_noun:
			for z in range(len(relations)):
				if i != z and k in relations[z][0] and len(relations[z][0]) > len(relations[i][0]):
					relations[i][0] = relations[z][0] '''
	for z in range(len(common_relations)):
		if i != z: 
			if intersection(common_relations[i][0].lower(),common_relations[z][0].lower()) >= 1:
				aa = common_relations[i][0].split()
				bb = common_relations[z][0].split()
				#maxima = max(intersect(common_relations[i][0].lower(), common_relations[z][0].lower()), key=len)
				flag = 0
				for p in aa:
					for q in bb:
						if p in q or q in p:
							
							if len(p) >= len(q):
								maxima1 = p
								minima1 = q
								flag = 1
								break
							else:
								maxima1 = q
								minima1 = p
								flag = 1
								break
					if flag == 1:
						break
		
				if maxima1 not in common_relations[i][0]:
					common_relations[i][0] = common_relations[i][0].replace(minima1,maxima1)  ###########do not replace the whole thing. Replace only the places which match 
#combining third components if there are substrings

for i in common_relations:
	print i

new = []
for i in range(len(common_relations)):
	three = []
	for j in range(len(common_relations)):
		if common_relations[i][0] in common_relations[j][0] or common_relations[j][0] in common_relations[i][0]: 
			if common_relations[i][1] in common_relations[j][1] or common_relations[j][1] in common_relations[i][1]:
				three.append(common_relations[j][2])
	three1 = three[:]
	for k in range(len(three)):
		z = three[k].split(' ')
		for r in range(len(three)):
			if k != r:
				count = 0
				for a in z:
					if a in three[r]:
						count += 1
				if count == len(z):
					if three[k] in three1:
						three1.remove(three[k])
	
						
	for q in three1:
		sub = []
		sub.append(common_relations[i][0])
		sub.append(common_relations[i][1])
		sub.append(q)
		if sub not in new:	
			new.append(sub)



#requires input in decode form
#combining second components if there are substrings

print "\n\n\n\New is ", new

newer = []
for i in range(len(new)):
	two = []
	for j in range(len(new)):
		if new[i][0] in new[j][0] or new[j][0] in new[i][0]:
			if new[i][2] in new[j][2] or new[j][2] in new[i][2]:
				two.append(new[j][1])
	two1 = two[:]
	for k in range(len(two)):
		z = two[k].split(' ')
		for r in range(len(two)):
			if k != r:
				count = 0
				for a in z:
					if a in two[r]:
						count += 1
				if count == len(z):
					if two[k] in two1:
						two1.remove(two[k])
	
						
	for q in two1:
		sub = []
		sub.append(new[i][0].encode('utf8'))
		sub.append(q.encode('utf8'))										#graph requires input in encode form
		sub.append(new[i][2].encode('utf8'))
		if sub not in newer:	
			newer.append(sub)





newer = []
flag = [0 for i in range(len(new))]
for i in range(len(new)):
	two = []
	for j in range(len(new)):
		if new[i][0] in new[j][0] or new[j][0] in new[i][0]:
			if new[i][2] in new[j][2] or new[j][2] in new[i][2]:  
				two.append(new[j][1])                                   #select first element
	two1 = two[:]
	for k in range(len(two)):
		z = two[k].split(' ')
		for r in range(len(two)):
			if k != r:
				count = 0
				for a in z:
					if a in two[r]:
						count += 1
				if count == len(z):
					if two[k] in two1:
						two1.remove(two[k])
	
						
	for q in two1:
		sub = []
		sub.append(new[i][0].encode('utf8'))
		sub.append(q.encode('utf8'))										#graph requires input in encode form
		sub.append(new[i][2].encode('utf8'))
		if sub not in newer:	
			newer.append(sub)

print "\n\n\n\Newer is ", newer

newer1 = []
flag = [0 for i in range(len(newer))]
for i in range(len(newer)):
	for j in range(len(newer)):
		if intersection(newer[i][1],newer[i][2]) >= 1:
			flag[i] = 1
			break	
		if flag[i] == 0 and i != j:
			if newer[i][0] in newer[j][0] or newer[j][0] in newer[i][0]:
				if newer[i][2] in newer[j][2] or newer[j][2] in newer[i][2]:
					flag[j] = 1
	if flag[i] == 0:
		newer1.append(newer[i])
		
print "\n\n\n\Newer1 is ", newer1
newest = newer1[:]
for i in range(len(newer1)):
	two_three = newer1[i][1] + ' ' + newer1[i][2]
	two_three_split = two_three.split()
	for j in range(len(newer1)):
		if newer1[i] != newer1[j] and newer1[i][0] == newer1[j][0]:
			string_trial = newer1[j][1] + ' ' + newer1[j][2]
			string_trial_split = string_trial.split()
			counting = 0
			for k in range(len(two_three_split)):
				 if two_three_split[k] in string_trial_split:
				 	counting += 1
			if counting == len(two_three_split):
				newest.remove(newer1[i])
				break
			
for i in newest:
	print i



print "--------------------------------------------------------------------------------------------------------------------------------------------------"
print "**************************************************************************************************************************************************"

	
list_matrix = []
for i in newest:
	if i[0] not in list_matrix:
		list_matrix.append(i[0])
	if i[2] not in list_matrix:
		list_matrix.append(i[2])
		
matrix = [[0 for i in list_matrix] for j in list_matrix]

for i in newest:
	matrix[list_matrix.index(i[0])][list_matrix.index(i[2])] = 1 



'''
def recur(a_list,a_index):
	for j in range(len(a_list)):
		if a_list[j] == 1:
			a_split = list_matrix[j].split()
			counting = 0
			for k in a_split:
				if k != 'Nazi-Party':
					counting += (word_degree[k.lower()]/word_frequency[k.lower()]*1.0)
			count[a_index] += counting
			recur(matrix[j],j)

'''
'''
count = [1 for i in list_matrix]
def recur(a_list,a_index):                         #exceeds recursion depth for linux so use iterative model
	recount += 1
	print recount
	for j in range(len(a_list)):
		if a_list[j] == 1:
			count[a_index] += 1
			recur(matrix[j],j)

for i in range(len(matrix)):
	recur(matrix[i],i)
	print list_matrix[i], count[i]
'''

count = [1 for i in list_matrix]
for i in range(len(matrix)):
	#print '********'
	#print "i is ", i 
	major = []
	for j in range(len(matrix[i])):
		if matrix[i][j] == 1:
			major.append(j)
	if major == []:
		continue
	z = 0
	while True:
		#print '        z is ', z
		for k in range(len(matrix)):	
			#print '                k is ', k
			if matrix[major[z]][k] == 1 and k not in major:
				major.append(k)
		if z == len(major) - 1:
			break
		z += 1
	count[i] += len(major)

combo = dict(zip(list_matrix,count))
new_combo = sorted(combo.items(),key=operator.itemgetter(1),reverse=False) #ascending
keys = [i[0] for i in new_combo]
values = [i[1] for i in new_combo]

key_value = {}
for i in range(len(values)):
	if values[i] not in key_value:
		key_value[values[i]] = [keys[i]]
	else:
		key_value[values[i]].append(keys[i])	
total = 0

for i in count:
	total += i

final_total = total
remove = []
"""
import random
print "Total is ",total
print "Final total is ",final_total
while total/(final_total*1.0) >= 0.9:
	minimum = min(key_value)
	if key_value[minimum] != []:
		p = random.randint(0,len(key_value[minimum])-1)
	else:
		del key_value[minimum]
		continue
	total -= values[keys.index(key_value[minimum][p])]
	if total/(final_total*1.0) < 0.9:
		break
	remove.append(keys[keys.index(key_value[minimum][p])])
	for k,v in key_value.items():
		if k == minimum:
			print keys[keys.index(key_value[minimum][p])]
			v.remove(keys[keys.index(key_value[minimum][p])])
			#print key_value
	print "Total inside is ", total
	print "Ratio is ", total/(final_total*1.0), '\n\n'
"""
newer_list = []
for i in newest:
	if i[0] not in remove:
		if i[2] not in remove:
			newer_list.append(i)

print "\n**********************REMOVED**********************\n"
for i in remove:
	print i

print remove


for i in newer_list:
	if i[0] == '' or i[1] == '' or i[2] == '':
		newer_list.remove(i)
	print i
	
generate_graphviz_graph(newer_list,verbose=True)
#generate_graphviz_graph(newest,verbose=True)

os.system('mv /tmp/openie/out.png ./')



content_no_dot = content_no_dot.split('.')
scored_sent = [0 for i in range(len(content_no_dot))]
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
sent_sorted = sorted(sent_dict.items(),key=operator.itemgetter(1),reverse=True)
#for i,v in sent_sorted:
#	print v, '--->', content_no_dot[i],'\n'

#sent_sorted_20 = dict(sent_sorted[:20])
sent_sorted_20 = dict(sent_sorted[:len(content_no_dot)/3])
inorder_sent_sorted_20 = sorted(sent_sorted_20.items(),key=operator.itemgetter(0),reverse=False)

for i,v in inorder_sent_sorted_20:
	print v, '--->', content_no_dot[i],'\n'

###############Check new_sort_list and play with no of keywords extracted per para. Refine this	

