#No Winnowing KEYWORDSUBJECT 70 use proc_part2_4.py
#No Winnowing 320, use proc_part2_2.py instead of proc_part2_4.py
#Rest all same


import os
files = os.listdir('trial_test_final/')

for inputfile in files:
	readfile = open('trial_test_final/'+inputfile,'r').read()
	writefile = open('important.txt','w')
	writefile.write(readfile)
	writefile.close()
	os.system('python nltk_tagger_rake_part2.py')
	os.system('python proc_part2_4.py -f sorter_3.txt')

	readagain0125 = open('summary_10.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.10/keywordsubject/'+inputfile.replace('Reference42','System1'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()
	
	readagain011 = open('summary_15.txt','r').read()
	writeagain011 = open('newest/original_summaries_0.15/keywordsubject/'+inputfile.replace('Reference42','System1'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_20.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.20/keywordsubject/'+inputfile.replace('Reference42','System1'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()

	readagain011 = open('summary_25.txt','r').read()
	writeagain011 = open('newest/original_summaries_0.25/keywordsubject/'+inputfile.replace('Reference42','System1'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_33.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.33/keywordsubject/'+inputfile.replace('Reference42','System1'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()
	
	readagain011 = open('summary_39.txt','r').read()
	writeagain011 = open('newest/original_summaries_0.39/keywordsubject/'+inputfile.replace('Reference42','System1'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_45.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.45/keywordsubject/'+inputfile.replace('Reference42','System1'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()
	
	print '\n\n' + str(files.index(inputfile)) + '\n\n'
