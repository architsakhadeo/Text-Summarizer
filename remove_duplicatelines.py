import os,re
direcs = os.listdir('final_excess/')
for direc in direcs:
	subdirecs = os.listdir('final_excess/'+direc+'/')
	for subdirec in subdirecs:
		files = os.listdir('final_excess/'+direc+'/'+subdirec+'/')
		for ifile in files:
			'''
			reader = open('final_excess/'+direc+'/'+subdirec+'/'+ifile,'r').read()
			writer = open('final_excess/'+direc+'/'+subdirec+'/'+ifile,'w')
			wrote = re.sub(' +',' ',reader)
			writer.write(wrote)
			'''
			lines_seen = set() # holds lines already seen
			lines = open('final_excess/'+direc+'/'+subdirec+'/'+ifile, "r").readlines()
			outfile = open('final_excess/'+direc+'/'+subdirec+'/'+ifile, "w")
			for line in lines:
				if line not in lines_seen: # not a duplicate
					outfile.write(line)
					lines_seen.add(line)
			outfile.close()
