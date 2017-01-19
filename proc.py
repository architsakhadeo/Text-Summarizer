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


	'''
	if y != '':
		if y not in f:
			f[y] = [t.decode('utf-8') for t in v]
			
		else:
			for e in v:	
				f[y].append(e.decode('utf-8'))
	'''
print "------------------------------------------------------------------------------------------------------------------------------------------"
print relations
'''
relations1 = {}
#removing verbs from third components 
for i,v in f.items():
	i = i.decode('utf-8').replace(" '", "'")
	l = []
	for p in v:
		p = p.split()
		for q in p:
			if q.lower() in stoplist:
				p[p.index(q)] = ';'
		p = ' '.join(p)
		p = p.split(';')
		for t in p:
			if t.strip() != '' and t.strip() not in l:
				l.append(t.strip())
	v = l[:]	
	v = [j.encode('utf-8') for j in v]  
	relations1[i] = v




newer_sort_list = {}

for i,v in new_sort_list:
	i = i
	newer_sort_list[i] = v

'''	
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

new = []
for i in range(len(common_relations)):
	three = []
	for j in range(len(common_relations)):
		if common_relations[i][0] == common_relations[j][0] and common_relations[i][1] == common_relations[j][1]:
			three.append(common_relations[j][2])
	print "Three is " + str(three)
	three1 = three[:]
	for k in range(len(three)):
		z = three[k].split(' ')
		print "Split is " + str(z)
		for r in range(len(three)):
			print "Error1"
			if k != r:
				count = 0
				for a in z:
					print "Error2"
					if a in three[r]:
						print "Error3"
						count += 1
				if count == len(z):
					print "Error4"
					if three[k] in three1:
						print "Error5"
						three1.remove(three[k])
						print "Error6"
	
						
	for q in three1:
		sub = []
		sub.append(common_relations[i][0])
		sub.append(common_relations[i][1])
		sub.append(q)
		if sub not in new:	
			new.append(sub)
#requires input in decode form
newer = []
for i in range(len(new)):
	two = []
	for j in range(len(new)):
		if new[i][0] == new[j][0] and new[i][2] == new[j][2]:
			two.append(new[j][1])
	print "Two is " + str(two)
	two1 = two[:]
	for k in range(len(two)):
		z = two[k].split(' ')
		print "Split is " + str(z)
		for r in range(len(two)):
			print "Error1"
			if k != r:
				count = 0
				for a in z:
					print "Error2"
					if a in two[r]:
						print "Error3"
						count += 1
				if count == len(z):
					print "Error4"
					if two[k] in two1:
						print "Error5"
						two1.remove(two[k])
						print "Error6"
	
						
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
	'''for j in range(len(common_relations)):
		if common_relations[i][0] == common_relations[j][0] and common_relations[i][1] == common_relations[j][1]:
			counter += 1
			if i!=j:	
				if common_relations[i][2] in common_relations[j][2]:
					count = 0
					break
				if common_relations[i][2] not in common_relations[j][2]:
					count = 1
	if count == 1:
		new.append(common_relations[i])
	if counter == 1:
		new.append(common_relations[i])
	if count == 0:
		continue
	'''
	

	
generate_graphviz_graph(newer,verbose=True)
os.system('mv /tmp/openie/out.png ./')
'''
#common to RAKE and OpenIE
a = {}
for i,v in relations1.items():
	for j,k in newer_sort_list.items():
		if i in j and i not in a and v != []:
			a[i] = [t.replace(" '","'") for t in v]
		if j in i and i not in a and v != []:
			a[i] = [t.replace(" '","'") for t in v]
			
#merging third components belonging to same relation if there are substrings
for i,v in a.items():
	p = v[:]
	for q in range(len(v)):
		t = v[q].split()
		for r in range(len(v)):
			if q != r:
				count = 0
				for z in t:
					if z in v[r]:
						count += 1
				if count == len(t):
					if v[q] in p:
						p.remove(v[q])
	a[i] = p

#sorting in decreasing order of number of third components
z = sorted(a,key=lambda k: len(a[k]),reverse=True)
for i in z:
	print i, " -> ",
	print a[i][0],
	for k in range(1,len(a[i])):
		print ',',a[i][k],
	print


'''
