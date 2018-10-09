import os
docs = os.listdir('duc2001_docs/')
for doc in docs:

	print '\n\n***********' + str(docs.index(doc)) + '***********\n\n'
	print '\n\n***********' + doc + '***********\n\n'
	'''
	file_size = int(os.stat('duc2001_docs/'+doc).st_size)
	size_10 = (int(os.stat('final_excess/excess_0.10/mycode/'+doc.replace('_Reference2','_System230')).st_size)+int(os.stat('final_excess/excess_0.10/nowinnowing/'+doc.replace('_Reference2','_System2320')).st_size)+int(os.stat('final_excess/excess_0.10/keywordsubject/'+doc.replace('_Reference2','_System270')).st_size))/3.0
	size_15 = (int(os.stat('final_excess/excess_0.15/mycode/'+doc.replace('_Reference2','_System230')).st_size)+int(os.stat('final_excess/excess_0.15/nowinnowing/'+doc.replace('_Reference2','_System2320')).st_size)+int(os.stat('final_excess/excess_0.15/keywordsubject/'+doc.replace('_Reference2','_System270')).st_size))/3.0
	size_20 = (int(os.stat('final_excess/excess_0.20/mycode/'+doc.replace('_Reference2','_System230')).st_size)+int(os.stat('final_excess/excess_0.20/nowinnowing/'+doc.replace('_Reference2','_System2320')).st_size)+int(os.stat('final_excess/excess_0.20/keywordsubject/'+doc.replace('_Reference2','_System270')).st_size))/3.0
	size_25 =(int(os.stat('final_excess/excess_0.25/mycode/'+doc.replace('_Reference2','_System230')).st_size)+int(os.stat('final_excess/excess_0.25/nowinnowing/'+doc.replace('_Reference2','_System2320')).st_size)+int(os.stat('final_excess/excess_0.25/keywordsubject/'+doc.replace('_Reference2','_System270')).st_size))/3.0
	size_33 = (int(os.stat('final_excess/excess_0.33/mycode/'+doc.replace('_Reference2','_System230')).st_size)+int(os.stat('final_excess/excess_0.33/nowinnowing/'+doc.replace('_Reference2','_System2320')).st_size)+int(os.stat('final_excess/excess_0.33/keywordsubject/'+doc.replace('_Reference2','_System270')).st_size))/3.0
	size_39 = (int(os.stat('final_excess/excess_0.39/mycode/'+doc.replace('_Reference2','_System230')).st_size)+int(os.stat('final_excess/excess_0.39/nowinnowing/'+doc.replace('_Reference2','_System2320')).st_size)+int(os.stat('final_excess/excess_0.39/keywordsubject/'+doc.replace('_Reference2','_System270')).st_size))/3.0
	size_45 = (int(os.stat('final_excess/excess_0.46/mycode/'+doc.replace('_Reference2','_System230')).st_size)+int(os.stat('final_excess/excess_0.46/nowinnowing/'+doc.replace('_Reference2','_System2320')).st_size)+int(os.stat('final_excess/excess_0.46/keywordsubject/'+doc.replace('_Reference2','_System270')).st_size))/3.0
	
	percent_10 = int(round(100.0*size_10/file_size))
	percent_15 = int(round(100.0*size_15/file_size))
	percent_20 = int(round(100.0*size_20/file_size))
	percent_25 = int(round(100.0*size_25/file_size))
	percent_33 = int(round(100.0*size_33/file_size))
	percent_39 = int(round(100.0*size_39/file_size))
	percent_45 = int(round(100.0*size_45/file_size))
	'''
	
	file_size = len(open('duc2001_docs/'+doc,'r').readlines())
	size_10 = (len(open('final_excess/excess_0.10/mycode/'+doc.replace('_Reference2','_System230'),'r').readlines())+len(open('final_excess/excess_0.10/nowinnowing/'+doc.replace('_Reference2','_System2320'),'r').readlines())+len(open('final_excess/excess_0.10/keywordsubject/'+doc.replace('_Reference2','_System270'),'r').readlines()))/3.0
	size_15 = (len(open('final_excess/excess_0.15/mycode/'+doc.replace('_Reference2','_System230'),'r').readlines())+len(open('final_excess/excess_0.15/nowinnowing/'+doc.replace('_Reference2','_System2320'),'r').readlines())+len(open('final_excess/excess_0.15/keywordsubject/'+doc.replace('_Reference2','_System270'),'r').readlines()))/3.0
	size_20 = (len(open('final_excess/excess_0.20/mycode/'+doc.replace('_Reference2','_System230'),'r').readlines())+len(open('final_excess/excess_0.20/nowinnowing/'+doc.replace('_Reference2','_System2320'),'r').readlines())+len(open('final_excess/excess_0.20/keywordsubject/'+doc.replace('_Reference2','_System270'),'r').readlines()))/3.0
	size_25 = (len(open('final_excess/excess_0.25/mycode/'+doc.replace('_Reference2','_System230'),'r').readlines())+len(open('final_excess/excess_0.25/nowinnowing/'+doc.replace('_Reference2','_System2320'),'r').readlines())+len(open('final_excess/excess_0.25/keywordsubject/'+doc.replace('_Reference2','_System270'),'r').readlines()))/3.0
	size_33 = (len(open('final_excess/excess_0.33/mycode/'+doc.replace('_Reference2','_System230'),'r').readlines())+len(open('final_excess/excess_0.33/nowinnowing/'+doc.replace('_Reference2','_System2320'),'r').readlines())+len(open('final_excess/excess_0.33/keywordsubject/'+doc.replace('_Reference2','_System270'),'r').readlines()))/3.0
	size_39 = (len(open('final_excess/excess_0.39/mycode/'+doc.replace('_Reference2','_System230'),'r').readlines())+len(open('final_excess/excess_0.39/nowinnowing/'+doc.replace('_Reference2','_System2320'),'r').readlines())+len(open('final_excess/excess_0.39/keywordsubject/'+doc.replace('_Reference2','_System270'),'r').readlines()))/3.0
	size_45 = (len(open('final_excess/excess_0.46/mycode/'+doc.replace('_Reference2','_System230'),'r').readlines())+len(open('final_excess/excess_0.46/nowinnowing/'+doc.replace('_Reference2','_System2320'),'r').readlines())+len(open('final_excess/excess_0.46/keywordsubject/'+doc.replace('_Reference2','_System270'),'r').readlines()))/3.0
	

	percent_10 = int(round(100.0*size_10/file_size))
	percent_15 = int(round(100.0*size_15/file_size))
	percent_20 = int(round(100.0*size_20/file_size))
	percent_25 = int(round(100.0*size_25/file_size))
	percent_33 = int(round(100.0*size_33/file_size))
	percent_39 = int(round(100.0*size_39/file_size))
	percent_45 = int(round(100.0*size_45/file_size))	
	
	
	
	os.system('sumy luhn --length='+str(percent_10)+'% --file=duc2001_docs/'+doc + ' > 10/luhn/'+doc.replace('Reference2','System21'))
	print '10_luhn'
	os.system('sumy luhn --length='+str(percent_15)+'% --file=duc2001_docs/'+doc + ' > 15/luhn/'+doc.replace('Reference2','System21'))
	print '15_luhn'
	os.system('sumy luhn --length='+str(percent_20)+'% --file=duc2001_docs/'+doc + ' > 20/luhn/'+doc.replace('Reference2','System21'))
	print '20_luhn'
	os.system('sumy luhn --length='+str(percent_25)+'% --file=duc2001_docs/'+doc + ' > 25/luhn/'+doc.replace('Reference2','System21'))
	print '25_luhn'
	os.system('sumy luhn --length='+str(percent_33)+'% --file=duc2001_docs/'+doc + ' > 33/luhn/'+doc.replace('Reference2','System21'))
	print '33_luhn'
	os.system('sumy luhn --length='+str(percent_39)+'% --file=duc2001_docs/'+doc + ' > 39/luhn/'+doc.replace('Reference2','System21'))
	print '39_luhn'
	os.system('sumy luhn --length='+str(percent_45)+'% --file=duc2001_docs/'+doc + ' > 45/luhn/'+doc.replace('Reference2','System21'))
	print '45_luhn'
		
	os.system('sumy edmundson --length='+str(percent_10)+'% --file=duc2001_docs/'+doc + ' > 10/edmundson/'+doc.replace('Reference2','System22'))
	print '10_edmundson'	
	os.system('sumy edmundson --length='+str(percent_15)+'% --file=duc2001_docs/'+doc + ' > 15/edmundson/'+doc.replace('Reference2','System22'))
	print '15_edmundson'
	os.system('sumy edmundson --length='+str(percent_20)+'% --file=duc2001_docs/'+doc + ' > 20/edmundson/'+doc.replace('Reference2','System22'))
	print '20_edmundson'
	os.system('sumy edmundson --length='+str(percent_25)+'% --file=duc2001_docs/'+doc + ' > 25/edmundson/'+doc.replace('Reference2','System22'))
	print '25_edmundson'
	os.system('sumy edmundson --length='+str(percent_33)+'% --file=duc2001_docs/'+doc + ' > 33/edmundson/'+doc.replace('Reference2','System22'))
	print '33_edmundson'
	os.system('sumy edmundson --length='+str(percent_39)+'% --file=duc2001_docs/'+doc + ' > 39/edmundson/'+doc.replace('Reference2','System22'))
	print '39_edmundson'
	os.system('sumy edmundson --length='+str(percent_45)+'% --file=duc2001_docs/'+doc + ' > 45/edmundson/'+doc.replace('Reference2','System22'))
	print '45_edmundson'
	
	os.system('sumy lsa --length='+str(percent_10)+'% --file=duc2001_docs/'+doc + ' > 10/lsa/'+doc.replace('Reference2','System23'))
	print '10_lsa'
	os.system('sumy lsa --length='+str(percent_15)+'% --file=duc2001_docs/'+doc + ' > 15/lsa/'+doc.replace('Reference2','System23'))
	print '15_lsa'
	os.system('sumy lsa --length='+str(percent_20)+'% --file=duc2001_docs/'+doc + ' > 20/lsa/'+doc.replace('Reference2','System23'))
	print '20_lsa'
	os.system('sumy lsa --length='+str(percent_25)+'% --file=duc2001_docs/'+doc + ' > 25/lsa/'+doc.replace('Reference2','System23'))
	print '25_lsa'
	os.system('sumy lsa --length='+str(percent_33)+'% --file=duc2001_docs/'+doc + ' > 33/lsa/'+doc.replace('Reference2','System23'))
	print '33_lsa'
	os.system('sumy lsa --length='+str(percent_39)+'% --file=duc2001_docs/'+doc + ' > 39/lsa/'+doc.replace('Reference2','System23'))
	print '39_lsa'
	os.system('sumy lsa --length='+str(percent_45)+'% --file=duc2001_docs/'+doc + ' > 45/lsa/'+doc.replace('Reference2','System23'))
	print '45_lsa'
		
	os.system('sumy text-rank --length='+str(percent_10)+'% --file=duc2001_docs/'+doc + ' > 10/text-rank/'+doc.replace('Reference2','System24'))
	print '10_text-rank'
	os.system('sumy text-rank --length='+str(percent_15)+'% --file=duc2001_docs/'+doc + ' > 15/text-rank/'+doc.replace('Reference2','System24'))
	print '15_text-rank'
	os.system('sumy text-rank --length='+str(percent_20)+'% --file=duc2001_docs/'+doc + ' > 20/text-rank/'+doc.replace('Reference2','System24'))
	print '20_text-rank'
	os.system('sumy text-rank --length='+str(percent_25)+'% --file=duc2001_docs/'+doc + ' > 25/text-rank/'+doc.replace('Reference2','System24'))
	print '25_text-rank'
	os.system('sumy text-rank --length='+str(percent_33)+'% --file=duc2001_docs/'+doc + ' > 33/text-rank/'+doc.replace('Reference2','System24'))
	print '33_text-rank'
	os.system('sumy text-rank --length='+str(percent_39)+'% --file=duc2001_docs/'+doc + ' > 39/text-rank/'+doc.replace('Reference2','System24'))
	print '39_text-rank'
	os.system('sumy text-rank --length='+str(percent_45)+'% --file=duc2001_docs/'+doc + ' > 45/text-rank/'+doc.replace('Reference2','System24'))
	print '45_text-rank'	

	os.system('sumy lex-rank --length='+str(percent_10)+'% --file=duc2001_docs/'+doc + ' > 10/lex-rank/'+doc.replace('Reference2','System25'))
	print '10_lex-rank'
	os.system('sumy lex-rank --length='+str(percent_15)+'% --file=duc2001_docs/'+doc + ' > 15/lex-rank/'+doc.replace('Reference2','System25'))
	print '15_lex-rank'
	os.system('sumy lex-rank --length='+str(percent_20)+'% --file=duc2001_docs/'+doc + ' > 20/lex-rank/'+doc.replace('Reference2','System25'))
	print '20_lex-rank'
	os.system('sumy lex-rank --length='+str(percent_25)+'% --file=duc2001_docs/'+doc + ' > 25/lex-rank/'+doc.replace('Reference2','System25'))
	print '25_lex-rank'
	os.system('sumy lex-rank --length='+str(percent_33)+'% --file=duc2001_docs/'+doc + ' > 33/lex-rank/'+doc.replace('Reference2','System25'))
	print '33_lex-rank'
	os.system('sumy lex-rank --length='+str(percent_39)+'% --file=duc2001_docs/'+doc + ' > 39/lex-rank/'+doc.replace('Reference2','System25'))
	print '39_lex-rank'
	os.system('sumy lex-rank --length='+str(percent_45)+'% --file=duc2001_docs/'+doc + ' > 45/lex-rank/'+doc.replace('Reference2','System25'))
	print '45_lex-rank'
	
