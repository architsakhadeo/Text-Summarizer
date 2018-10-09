#MYCODE - WINNOWING

import os
files = os.listdir('trial_test_final/')
for inputfile in files:
	readfile = open('trial_test_final/'+inputfile,'r').read()
	writefile = open('important.txt','w')
	writefile.write(readfile)
	writefile.close()
	os.system('python nltk_tagger_rake.py')
	os.system('python proc.py -f sorter.txt')
	os.system('python nltk_tagger_rake_part2.py')
	os.system('python proc_part2_2.py -f sorter_3.txt')

	readagain0125 = open('summary_10.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.10/mycode/'+inputfile.replace('Reference42','System2'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()
	
	readagain011 = open('summary_15.txt','r').read()
	writeagain011 = open('newest/original_summaries_0.15/mycode/'+inputfile.replace('Reference42','System2'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_20.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.20/mycode/'+inputfile.replace('Reference42','System2'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()

	readagain011 = open('summary_25.txt','r').read()
	writeagain011 = open('newest/original_summaries_0.25/mycode/'+inputfile.replace('Reference42','System2'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_33.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.33/mycode/'+inputfile.replace('Reference42','System2'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()
	
	readagain011 = open('summary_39.txt','r').read()
	writeagain011 = open('newest/original_summaries_0.39/mycode/'+inputfile.replace('Reference42','System2'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_45.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.45/mycode/'+inputfile.replace('Reference42','System2'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()		
	
	print '\n\n' + str(files.index(inputfile)) + '\n\n'
