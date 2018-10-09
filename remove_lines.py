import os, re
directories = os.listdir('trial/')
for directory in directories:
	files = os.listdir('trial/'+directory+'/')
	for inputfile in files:
		readfile = open('trial/'+directory+'/'+inputfile,'r').read()
		a = re.findall(r'\w+\n',readfile)
		print a
		for i in a:
			readfile = readfile.replace(i,i.strip()+' ')
		writefile = open('trial/'+directory+'/'+inputfile,'w')
		writefile.write(readfile)

