import re
def intersection(string1,string2):
	#list1 = string1.split()
	#list2 = string2.split()	
	list1 = list(filter(None, re.split('''[-' ]''',string1)))
	list2 = list(filter(None, re.split('''[-' ]''',string2)))
	
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
	print(count1, count2, count)
	
	
intersection('Amazon executive Jeffrey-P-Bezos','Amazon chief executive Jeffrey-P-Bezos')
