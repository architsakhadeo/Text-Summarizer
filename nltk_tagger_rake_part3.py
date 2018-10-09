# -*- coding: utf-8 -*-
# encoding=utf8



'''
This code does preprocessing on the input text to remove corner cases which
cause trouble in the process of keyphrase extraction and then does the
extraction process using RAKE extraction method.
'''



import re
import operator
import nltk




#File containing text
#content1 = open('sorter_part2.txt','r').read()
content1 = open('important.txt','r').read()
contentforsplit = content1[:]
sorter = open('sorter_3.txt','w')

stoplistlines = open("stopwords1.txt",'r').readlines()
stoplist = []
for i in stoplistlines:
	stoplist.append(i.strip().lower())




#refining data to appropriate form
def preprocess(content1):

	'''
	Numbers like 1.34 are edge cases and the extractor will split the number
	into 1 and 34 if not handled properly. Hence it has been replaced by <dot>
	which is later replaced back to dot.
	
	Similarly for desginations like Mr., Mrs., Dr., are replaced to Mr, Mrs, Dr
	or initials like O. Schindler is replaced to O Schindler. 
	'''
	content = filter(None, re.sub('''Rs.''','''Rs''',content1))
	content = filter(None, re.sub('''Mr.''','''Mr''',content))
	content = filter(None, re.sub('''Mrs.''','''Mrs''',content))
	content = filter(None, re.sub('''Ms.''','''Ms''',content))
	content = filter(None, re.sub('''Dr.''','''Dr''',content))
	content = filter(None, re.sub('''([A-Z])\.''','''\\1''',content))
	content = filter(None, re.sub('''([0-9])\.''','''\\1<dot>''',content))
	content = filter(None, re.sub('''-and-''','''&''',content))
	
	
	'''
	Joining continuously occurring proper nouns into one proper noun separated
	by '-' to avoid unnecessary higher score to proper nouns.
	
	For example
	
	Oskar Schindler is replaced by Oskar-Schindler so the extractor considers it
	as one word and not as two separate words thus retaining the importance to
	both the proper nouns equally if they occur one after the other
	
	'''		
	token = nltk.word_tokenize(content.decode('utf-8'))
	
	pos = nltk.pos_tag(token) #pos tagger
	word_token = []
	tag_token = []
	for w,t in pos:
		word_token.append(w)
		tag_token.append(t)

	phraseList = []
	p = 0
	while p < len(tag_token):
		if tag_token[p] == 'NNP' or tag_token[p] == 'NNPS':   #Proper noun tags
			ph = word_token[p]
			j = p + 1
			if j >= len(tag_token):
				phraseList.append(ph)
				break
			flag = 0
			while j < len(tag_token):
				if tag_token[j] == 'NNP' or tag_token[j] == 'NNPS':
					ph += '-' + word_token[j]
					j += 1
					if j >= len(tag_token):	
						flag = 1		
				else:
					p = j
					phraseList.append(ph)
					break
			if flag == 1:
				phraseList.append(ph)
				break
		else:
			phraseList.append(word_token[p])
			p += 1


	
	
	'''
	phraseList contains merged proper nouns
	'''	
	phraseStr = ' '.join(phraseList)
	phraseStr = phraseStr.replace(' < dot > ', '<dot>')
	phraseStr = phraseStr.replace(' ,', ',')	
	phraseStr1 = phraseStr.replace(' ,', ',')	
	phraseStr1 = phraseStr1.replace('^',"'")
	#Made global since it is imported in proc_part2.py
	global read
	read = phraseStr1[:]
	read = read.encode('utf8').replace('-< dot >','<dot>')

	phraseStr1 = phraseStr1.replace('<dot>', '.') #for Open IE
	sent = nltk.sent_tokenize(content.decode('utf-8'))
	content11 = phraseStr1[:]
	sorter.write(content11.encode('utf8').replace('-< dot > ','<dot>'))
	content = phraseStr[:]



	
	#Removal of articles
	articles = [' the ',' a ', ' an ']
	for i in articles:
		content = content.replace(i,' ')
	
	
	
	
	#Removal of verbs which are not in stoplist
	'''
	If the keyphrase consists of "Indian aeroplane is best of its kind ; thus 
	gaining world ranking 3 in terms of safety" then it removes the
	verbs and replaces them with '|'
	
	Resultant statement will be "Indian aeroplane | best of its kind ; thus 
	| world ranking 3 in terms of safety"
	'''
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
	'''

	After the preprocessing step has been finished, the text is split on the basis
	of multiple symbols to get the shorter parts of sentences which can give us
	keyphrases

	Example: "Indian aeroplane | best of its kind ; thus | world ranking 3 in terms of safety"

	will be replaced to two sentences split on the ; and |

	Resultant will be "Indian aeroplane", "best of its kind", "thus", "world ranking 3 in terms of safety"

	'''
	contentList = filter(None, re.split('''[`~!@#$%&*_?=+/,.\\\\;|{}\(\)]''',content))
	return contentList



	
#Finding candidate keywords
def processPhrases(contentList):
	'''

	stopwords like 'of' and 'its' won't be present now as we replace them by |

	"Indian aeroplane", "best of its kind", "thus", "world ranking 3 in terms of safety"

	will become

	"Indian aeroplane", "best", "kind", "thus", "world ranking 3", "terms", "safety"
	'''	
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

	'''
	Calculates the frequency of the words in the document.
	Frequency of the word is the number of times it appears in the document.

	Calculates the degree of the words.
	Degree of a word is the number of keyphrases present along with a specific keyphrase in a sentence.
	We add this for all the sentences to get the degree of the word.
	Thus degree is the total number of keyphrase related to a particular keyphrase.

	For -> "Indian aeroplane", "best", "kind", "world ranking 3", "terms", "safety"

	Frequency of each keyphrase is the total number of times they occur in the document
	Degree of each keyphrase in this sentence is 6 including themselves. We add individual degrees
	for each sentence to get the final degree.

	This final degree for each word is divided by the frequency of the world to find the score
	against a particular keyphrase. The more score, the higher will the keyphrase appear statistically
	in the list.

	'''
	global word_frequency
	global word_degree
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
	
	##printing keyphrases in decreasing order of word scores
	print "NLTK POS TAGGER"
	new_sort_list = {}
	for i,v in sort_list:
		new_sort_list[i.replace('^',"'").replace('<dot>','.').strip()] = v
	#	#print i.replace('^',"'").replace('<dot>','.').strip(), ' - ', v
	##print '----------------------------------------------------------------'
	
	new_sort_list = sorted(new_sort_list.items(),key=operator.itemgetter(1),reverse=True)
	
	new_sort_dict = {}
	for i,v in new_sort_list:
		new_sort_dict[i] = v


	
	
	#separating on the basis of paragraphs
	splitcontent = contentforsplit.split('\n')
	freq = [[] for i in range(len(splitcontent))]     #contains keyphrases in one para
	
	for i,v in new_sort_list:
		
		for j in splitcontent:
			if i in j.decode('utf-8'):
				freq[splitcontent.index(j)].append(i)

	another_freq = []
	another_score = []
	for i in range(len(freq)):
		for j in range(50):                          #for 25 keyphrases in each paragraph
			if j < len(freq[i]):
				another_freq.append(freq[i][j])
				another_score.append(new_sort_dict[freq[i][j]])
	dictor = dict(zip(another_freq,another_score))

	
	new_sort_dictor = sorted(dictor.items(),key=operator.itemgetter(1),reverse=True)
					
	return new_sort_dictor
	'''
	return new_sort_list
	'''



	
#dealing with characters which cause in poor results
articles0 = ['“','”','"']
for i in articles0:
	content1 = content1.replace(i,'')
content1 = content1.replace("'",'^')
content1 = content1.replace("’",'^')		 	 
articles = ['—','[',']']
for o in articles:
	content1 = content1.replace(o,' ')

articles1 = ['. The ', '. A ', '. An ']
for o in articles1:
	content1 = content1.replace(o,'. ')





def main():
	#Does preprocessing on the input text
	content = preprocess(content1)


	
	#Splits processed input text on multiple symbols 
	contentList = contentSplit(content)


	
	#Creates a list of keyphrases from the available text 
	candidateKeywords = processPhrases(contentList)


	
	#calculates word scores of each keyphrase
	global new_sort_list
	new_sort_list = word_score(candidateKeywords)


	#Print keyphrases in descending order
	for i,v in new_sort_list:
		i = i.strip()
		print i, v

	print '\n\n\n\n\n\n\n\n\n\n\n\n'
main()


import math

print '\n\n\n\n\n\n\HEY\n\n\n\n'
scores = []
sorter.close()
read = open('sorter_3.txt','r').read().split(' . ')
print read
for i in read:
	score = 0
	words = i.split(' ')
	for j in words:
		if j in word_frequency:	
			score += (word_degree[j.lower()]*1.0)/word_frequency[j.lower()]
			print score, j
	scores.append(score)
print scores
indexed = [i for i in range(len(scores))]
sent_dict = dict(zip(indexed,scores))
sent_sorted = sorted(sent_dict.items(),key=operator.itemgetter(1),reverse=True)




sent_sorted_top_10 = dict(sent_sorted[:int(math.ceil(len(read)*0.1))])	
#Sorts these top 1/3rd obtained sentences in increasing order of their appearance in the input text 
inorder_sent_sorted_top_10 = sorted(sent_sorted_top_10.items(),key=operator.itemgetter(0),reverse=False)


print '\n\n\n\n\n\nSummary is\n\n\n'
strstrstr_10 = ""
for index,score in inorder_sent_sorted_top_10:
	strstrstr_10 += str(read[index].strip().replace('<dot>','.')) + '.\n'
	print read[index].strip().replace('<dot>','.') + '.'

filer_10 = open('summary_10.txt','w')
filer_10.write(strstrstr_10)






sent_sorted_top_25 = dict(sent_sorted[:int(math.ceil(len(read)*0.25))])	
#Sorts these top 1/3rd obtained sentences in increasing order of their appearance in the input text 
inorder_sent_sorted_top_25 = sorted(sent_sorted_top_25.items(),key=operator.itemgetter(0),reverse=False)


print '\n\n\n\n\n\nSummary is\n\n\n'
strstrstr_25 = ""
for index,score in inorder_sent_sorted_top_25:
	strstrstr_25 += str(read[index].strip().replace('<dot>','.')) + '.\n'
	print read[index].strip().replace('<dot>','.') + '.'

filer_25 = open('summary_25.txt','w')
filer_25.write(strstrstr_25)









sent_sorted_top_33 = dict(sent_sorted[:int(math.ceil(len(read)*0.33))])	
#Sorts these top 1/3rd obtained sentences in increasing order of their appearance in the input text 
inorder_sent_sorted_top_33 = sorted(sent_sorted_top_33.items(),key=operator.itemgetter(0),reverse=False)


print '\n\n\n\n\n\nSummary is\n\n\n'
strstrstr_33 = ""
for index,score in inorder_sent_sorted_top_33:
	strstrstr_33 += str(read[index].strip().replace('<dot>','.')) + '.\n'
	print read[index].strip().replace('<dot>','.') + '.'

filer_33 = open('summary_33.txt','w')
filer_33.write(strstrstr_33)



sent_sorted_top_39 = dict(sent_sorted[:int(math.ceil(len(read)*0.39))])	
#Sorts these top 1/3rd obtained sentences in increasing order of their appearance in the input text 
inorder_sent_sorted_top_39 = sorted(sent_sorted_top_39.items(),key=operator.itemgetter(0),reverse=False)


print '\n\n\n\n\n\nSummary is\n\n\n'
strstrstr_39 = ""
for index,score in inorder_sent_sorted_top_39:
	strstrstr_39 += str(read[index].strip().replace('<dot>','.')) + '.\n'
	print read[index].strip().replace('<dot>','.') + '.'

filer_39 = open('summary_39.txt','w')
filer_39.write(strstrstr_39)



sent_sorted_top_45 = dict(sent_sorted[:int(math.ceil(len(read)*0.45))])	
#Sorts these top 1/3rd obtained sentences in increasing order of their appearance in the input text 
inorder_sent_sorted_top_45 = sorted(sent_sorted_top_45.items(),key=operator.itemgetter(0),reverse=False)


print '\n\n\n\n\n\nSummary is\n\n\n'
strstrstr_45 = ""
for index,score in inorder_sent_sorted_top_45:
	strstrstr_45 += str(read[index].strip().replace('<dot>','.')) + '.\n'
	print read[index].strip().replace('<dot>','.') + '.'

filer_45 = open('summary_45.txt','w')
filer_45.write(strstrstr_45)


sent_sorted_top_15 = dict(sent_sorted[:int(math.ceil(len(read)*0.15))])	
#Sorts these top 1/3rd obtained sentences in increasing order of their appearance in the input text 
inorder_sent_sorted_top_15 = sorted(sent_sorted_top_15.items(),key=operator.itemgetter(0),reverse=False)


print '\n\n\n\n\n\nSummary is\n\n\n'
strstrstr_15 = ""
for index,score in inorder_sent_sorted_top_15:
	strstrstr_15 += str(read[index].strip().replace('<dot>','.')) + '.\n'
	print read[index].strip().replace('<dot>','.') + '.'

filer_15 = open('summary_15.txt','w')
filer_15.write(strstrstr_15)


sent_sorted_top_20 = dict(sent_sorted[:int(math.ceil(len(read)*0.20))])	
#Sorts these top 1/3rd obtained sentences in increasing order of their appearance in the input text 
inorder_sent_sorted_top_20 = sorted(sent_sorted_top_20.items(),key=operator.itemgetter(0),reverse=False)


print '\n\n\n\n\n\nSummary is\n\n\n'
strstrstr_20 = ""
for index,score in inorder_sent_sorted_top_20:
	strstrstr_20 += str(read[index].strip().replace('<dot>','.')) + '.\n'
	print read[index].strip().replace('<dot>','.') + '.'

filer_20 = open('summary_20.txt','w')
filer_20.write(strstrstr_20)



