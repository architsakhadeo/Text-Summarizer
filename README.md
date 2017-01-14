The project uses Python wrappers on Stanford's Open IE from https://github.com/philipperemy/Stanford-OpenIE-Python and NLTK.

Dependencies: You may be required to download some corpora and the built in pos tagger(maxent_treebank_pos_tagger) from nltk.download(). Download all if it doesn't work.

Running the code
  
  1) Change the variable "content1" to input file name in the nltk_tagger_rake.py 
  
  2) python nltk_tagger_rake.py -> gives keyphrases
  
  3) python proc.py -f sorter.txt -> gives relation between objects and subject(common to keyphrases)
  
  
  
