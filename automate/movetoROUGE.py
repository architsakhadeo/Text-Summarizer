import os
trial = open('mapping_trial_names.txt','r').read().split('\n')
rouge = open('mapping_rouge_names.txt','r').read().split('\n')

for i in range(len(trial)):
	if trial[i] != '':
		os.system('mv summaries_trial/'+trial[i] + ' ' + 'summaries_trial/'+trial[i].split('/')[0]+'/'+rouge[i]+'_System3')

directories = os.listdir('summaries_trial/')
for directory in directories:
	os.system('cp -rf summaries_trial/'+directory+'/*' + ' ~/Desktop/ROUGE-Java/test-summarization/system/')
	
for i in range(len(trial)):
	if trial[i] != '':	
		os.system('mv summaries_trial/'+trial[i].split('/')[0]+'/'+rouge[i]+'_System3' + ' ' + 'summaries_trial/'+trial[i]+'_System3')
