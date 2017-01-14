from mained import relations
import nltk
import operator
from nltk_tagger_rake import new_sort_list


stoplistlines = open("stopwords1.txt",'r').readlines()
stoplist = []
for i in stoplistlines:
	stoplist.append(i.strip().lower())


#removing verbs from first components and merges them if they are same after removal of verbs
verb = ['VB','VBD','VBG','VBN','VBZ','VBP']
f = {}
for i,v in relations.items():
	p = nltk.word_tokenize(i)
	p = nltk.pos_tag(p)
	str1 = []
	for j,k in p:
		if k not in verb:
			str1.append(j)
	str1 = ' '.join(str1)
	y = i.replace(i,str1)
	if y != '':
		if y not in f:
			f[y] = [t.decode('utf-8') for t in v]
			
		else:
			for e in v:	
				f[y].append(e.decode('utf-8'))


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

	
print "------------------------------------------------------------------"
print "Relations"
print "------------------------------------------------------------------"

#common to RAKE and OpenIE
a = {}
for i,v in relations1.items():
	for j,k in newer_sort_list.items():
		if i in j and i not in a and v != []:
			a[i] = v
		if j in i and i not in a and v != []:
			a[i] = v
			
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



