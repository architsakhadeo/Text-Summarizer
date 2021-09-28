import os
files = os.listdir('trial_test/')

for inputfile in files:
	readfile = open('trial_test/'+inputfile,'r').read()
	writefile = open('important.txt','w')
	writefile.write(readfile)
	writefile.close()
	os.system('python nltk_tagger_rake.py')
	os.system('python proc.py -f sorter.txt')
	os.system('python nltk_tagger_rake_part2.py')
	os.system('python proc_part2_2.py -f sorter_3.txt')
	
	readagain011 = open('summary_15.txt','r').read()
	writeagain011 = open('original_summaries_0.15/'+inputfile.replace('Reference1','System3'),'w')
	writeagain011.write(readagain011)
	writeagain011.close()
	
	readagain0125 = open('summary_20.txt','r').read()
	writeagain0125 = open('original_summaries_0.20/'+inputfile.replace('Reference1','System3'),'w')
	writeagain0125.write(readagain0125)
	writeagain0125.close()

	
