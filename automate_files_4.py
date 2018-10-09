#Only SUBJECTS

import os
files = os.listdir('trial_test_final/')

for inputfile in files:
	readfile = open('trial_test_final/'+inputfile,'r').read()
	writefile = open('important.txt','w')
	writefile.write(readfile)
	writefile.close()
	os.system('python nltk_tagger_rake_part6.py')
	os.system('python proc_part2_3.py -f sorter_6.txt')

	readagain0125 = open('summary_101.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.10/subjects/'+inputfile.replace('Reference42','System4'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()
	
	readagain011 = open('summary_151.txt','r').read()
	writeagain011 = open('newest/original_summaries_0.15/subjects/'+inputfile.replace('Reference42','System4'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_201.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.20/subjects/'+inputfile.replace('Reference42','System4'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()

	readagain011 = open('summary_251.txt','r').read()
	writeagain011 = open('newest/original_summaries_0.25/subjects/'+inputfile.replace('Reference42','System4'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_331.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.33/subjects/'+inputfile.replace('Reference42','System4'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()
	
	readagain011 = open('summary_391.txt','r').read()
	writeagain011 = open('newest/original_summaries_0.39/subjects/'+inputfile.replace('Reference42','System4'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_451.txt','r').read()
	writeagain0125 = open('newest/original_summaries_0.45/subjects/'+inputfile.replace('Reference42','System4'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()
	
	print '\n\n' + str(files.index(inputfile)) + '\n\n'
