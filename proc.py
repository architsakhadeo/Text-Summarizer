from mained import relations
import nltk
import operator
from nltk_tagger_rake import new_sort_list
from mained import generate_graphviz_graph
import os
stoplistlines = open("stopwords1.txt",'r').readlines()
stoplist = []
for i in stoplistlines:
	stoplist.append(i.strip().lower())


#removing verbs from first components and merges them if they are same after removal of verbs
verb = ['VB','VBD','VBG','VBN','VBZ','VBP']

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


print "------------------------------------------------------------------------------------------------------------------------------------------"
print relations

print "------------------------------------------------------------------"
print "Relations"
print "------------------------------------------------------------------"
common_relations = []
for i in relations:
	for j,k in new_sort_list:
		if i[0].encode('utf8') in j.encode('utf8') and i not in common_relations:
			common_relations.append(i)
		if j.encode('utf8') in i[0].encode('utf8') and i not in common_relations:
			common_relations.append(i)

for i in common_relations:		
	print i


#combining third components if there are substrings
new = []
for i in range(len(common_relations)):
	three = []
	for j in range(len(common_relations)):
		if common_relations[i][0] == common_relations[j][0] and common_relations[i][1] == common_relations[j][1]:
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
newer = []
for i in range(len(new)):
	two = []
	for j in range(len(new)):
		if new[i][0] == new[j][0] and new[i][2] == new[j][2]:
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




print "--------------------------------------------------------------------------------------------------------------------------------------------------"
print "**************************************************************************************************************************************************"
for i in newer:
	print i
	

	
generate_graphviz_graph(newer,verbose=True)
os.system('mv /tmp/openie/out.png ./')

