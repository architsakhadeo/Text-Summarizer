# -*- coding: utf-8 -*-
# encoding=utf8
import re
import operator
import nltk

#File containing text
content1 = open('schindler.txt','r').read()
contentforsplit = content1[:]
print "\n\n\n\n\n\n"
sorter = open('sorter.txt','w')

stoplistlines = open("stopwords1.txt",'r').readlines()
stoplist = []
for i in stoplistlines:
	stoplist.append(i.strip().lower())

def preprocess(content1):
	#refining data to appropriate form
	content = filter(None, re.sub('''Rs.''','''Rs''',content1))
	content = filter(None, re.sub('''Mr.''','''Mr''',content))
	content = filter(None, re.sub('''Mrs.''','''Mrs''',content))
	content = filter(None, re.sub('''Ms.''','''Ms''',content))
	content = filter(None, re.sub('''Dr.''','''Dr''',content))
	content = filter(None, re.sub('''([A-Z])\.''','''\\1''',content))
	content = filter(None, re.sub('''([0-9])\.''','''\\1<dot>''',content))
	content = filter(None, re.sub('''-and-''','''&''',content))
	
	
	
	#Joining continuously occurring proper nouns into one proper noun separated by '-' to avoid unnecessary higher score to proper nouns.	
	token = nltk.word_tokenize(content.decode('utf-8'))
	
	pos = nltk.pos_tag(token) #pos tagger
	ii = []
	vv = []
	for p,v in pos:
		ii.append(p)
		vv.append(v)

	phraseList = []
	p = 0
	while p < len(vv):
		if vv[p] == 'NNP' or vv[p] == 'NNPS':
			ph = ii[p]
			j = p + 1
			if j >= len(vv):
				phraseList.append(ph)
				break
			flag = 0
			while j < len(vv):
				if vv[j] == 'NNP' or vv[j] == 'NNPS':
					ph += '-' + ii[j]
					j += 1
					if j >= len(vv):	
						flag = 1		
				else:
					p = j
					phraseList.append(ph)
					break
			if flag == 1:
				phraseList.append(ph)
				break
		else:
			phraseList.append(ii[p])
			p += 1
	
	phraseStr = ' '.join(phraseList)
	phraseStr = phraseStr.replace(' < dot > ', '<dot>')

	phraseStr = phraseStr.replace(' ,', ',')	
	phraseStr1 = phraseStr.replace('<dot>', '.') #for Open IE
	phraseStr1 = phraseStr1.replace(' ,', ',')	
	phraseStr1 = phraseStr1.replace('^',"'")
	sent = nltk.sent_tokenize(content.decode('utf-8'))
	
	
	content11 = phraseStr1[:]
	
	sorter.write(content11.encode('utf8'))
	
	
	content = phraseStr[:]
	
	
	sym = [' the ',' a ', ' an ']
	for i in sym:
		content = content.replace(i,' ')
	
	#Removal of verbs which are not in stoplist

	verb = ['VB','VBD','VBG','VBN','VBZ','VBP']
	verbs = []

	for t in sent:	
		token = nltk.word_tokenize(t)
		pos = nltk.pos_tag(token)
		for i,v in pos:
			if v in verb:
				if i not in stoplist:
					verbs.append(i)

	for i in verbs:
		content = filter(None, re.sub(' ' +str(i.encode('utf8') + ' '),''' | ''',content))
	
	return content

#text split on the basis of following characters
def contentSplit(content):
	contentList = filter(None, re.split('''[`~!@#$%&*_?=+/,.\\\\;|{}\(\)]''',content))
	return contentList
	
#Finding candidate keywords	
def processPhrases(contentList):
	candidateKeywords = []
	
	for i in contentList:
		phraseStr = (i.replace('\t','').replace('\n','').strip())

		phraseList = phraseStr.split()
		
		
		for k in phraseList:	
			if k.lower() in stoplist:
				phraseList[phraseList.index(k)] = '|'

		phraseStr = ' '.join(phraseList)
		a = phraseStr.split('|')
		for o in a:
			candidateKeywords.append(o)
	candidateKeywords = [x.strip() for x in candidateKeywords if x] 
	candidateKeywords = filter(None, candidateKeywords)
	return candidateKeywords

#calculating word score
def word_score(candidateKeywords):
	word_frequency = {}
	word_degree = {}
	for i in candidateKeywords:
		for j in i.split():
			if j.lower() in word_frequency:
				word_frequency[j.lower()] += 1
				word_degree[j.lower()] += len(i.split())
			else:
				word_frequency[j.lower()] = 1
				word_degree[j.lower()] = len(i.split())    

	summed = {}
	for i in candidateKeywords:
		phrased = ""
		sumof = 0
		for j in i.split():
			phrased += " "
			phrased += j
			sumof += (word_degree[j.lower()])/(word_frequency[j.lower()] * 1.0)   #phrase wise score

		summed[phrased.strip()] = sumof

	sort_list = sorted(summed.items(),key=operator.itemgetter(1),reverse=True)
	
	content = filter(None, re.sub('''Rs.''','''Rs''',content1))
	content = filter(None, re.sub('''Mr.''','''Mr''',content))
	content = filter(None, re.sub('''Mrs.''','''Mrs''',content))
	content = filter(None, re.sub('''Ms.''','''Ms''',content))
	content = filter(None, re.sub('''Dr.''','''Dr''',content))
	content = filter(None, re.sub('''([A-Z])\.''','''\\1''',content))
	content = filter(None, re.sub('''([0-9])\.''','''\\1<dot>''',content))
	content = filter(None, re.sub('''-and-''','''&''',content))
	
	con = filter(None, re.split('''[.]''',content))
	
	for i in range(len(con)):
		con[i] = con[i].replace('\t','').replace('\n','').strip()
	length = [0 for i in range(len(con))]
	dash = []
	
	#Printing keyphrases in decreasing order of word scores
	print "NLTK POS TAGGER"
	new_sort_list = {}
	for i,v in sort_list:
		new_sort_list[i.replace('^',"'").replace('<dot>','.').strip()] = v
	#	print i.replace('^',"'").replace('<dot>','.').strip(), ' - ', v
	#print '----------------------------------------------------------------'
	
	new_sort_list = sorted(new_sort_list.items(),key=operator.itemgetter(1),reverse=True)
	new_sort_dict = {}
	for i,v in new_sort_list:
		new_sort_dict[i] = v
	
	#separating on the basis of paragraphs
	splitcontent = contentforsplit.split('\n')
	freq = [[] for i in range(len(splitcontent))]
	
	for i,v in new_sort_list:
		
		for j in splitcontent:
			if i in j.decode('utf-8'):
				freq[splitcontent.index(j)].append(i)
	#print freq
	another_freq = []
	another_score = []
	for i in range(len(freq)):
		for j in range(3):                          #for 3 keyphrases in each paragraph
			if j < len(freq[i]):
				another_freq.append(freq[i][j])
				another_score.append(new_sort_dict[freq[i][j]])
	dictor = dict(zip(another_freq,another_score))

	
	new_sort_dictor = sorted(dictor.items(),key=operator.itemgetter(1),reverse=True)
					
	return new_sort_dictor


#dealing with characters which cause in poor results
sym0 = ['“','”','"']
for i in sym0:
	content1 = content1.replace(i,'')
content1 = content1.replace("'",'^')
content1 = content1.replace("’",'^')		 	 
sym = ['—','[',']']
for o in sym:
	content1 = content1.replace(o,' ')

sym1 = ['. The ', '. A ', '. An']
for o in sym1:
	content1 = content1.replace(o,'. ')

content = preprocess(content1)
contentList = contentSplit(content)
candidateKeywords = processPhrases(contentList)
new_sort_list = word_score(candidateKeywords)


for i,v in new_sort_list:
	i = i.strip()
	print i, v
	
