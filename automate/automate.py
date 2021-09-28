import os
directories = os.listdir('trial/')
for directory in directories:
	files = os.listdir('trial/'+directory+'/')
	for inputfile in files:
		readfile = open('trial/'+directory+'/'+inputfile,'r').read()
		writefile = open('important.txt','w')
		writefile.write(readfile)
		writefile.close()
		os.system('python nltk_tagger_rake.py')
		os.system('python proc.py -f sorter.txt')
		os.system('python nltk_tagger_rake_part2.py')
		os.system('python proc_part2_2.py -f sorter_3.txt')
		readagain = open('summary.txt','r').read()
		writeagain = open('summaries_trial/'+directory+'/'+inputfile,'w')
		writeagain.write(readagain)
		writeagain.close()
		print "\n\n\n----------------------------------------------------------------------"
		print "Done:       " + str(directories.index(directory)) + "-" + str(files.index(inputfile)) + "      " + str(directory) + "      " + str(inputfile)
		print "----------------------------------------------------------------------\n\n\n"	 
