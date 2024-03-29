The project uses Python wrappers on Stanford's Open IE from https://github.com/philipperemy/Stanford-OpenIE-Python and NLTK.

Dependencies: You may be required to download some corpora and the built-in pos-tagger (maxent_treebank_pos_tagger) from nltk.download(). Download all data from nltk if it doesn't work.

## Tools used

1) Regular Expression
 
2) NLTK data set (models, corpus)
 
3) NLTK POS tagger
 
4) Stanford’s OpenIE implementation in Python which also provides the facility to
   use graphviz to generate graph
 
5) networkx to generate graph


## Running the code

  
 1) Change the variable `input_content` to input file name (input.txt) in the `stage1_nowinnowing.py`
   
 2) `python stage1_nowinnowing.py` -> gives keyphrases
 
 3) `python proc_ranker.py -f outputs/output_file.txt` -> gives relation between objects and subject(common to keyphrases)
 
 4) Check for the `out.png` image for graphical representation provided by Open IE
  
or Just run `script.sh`

 1) Change the variable `input_content` to input file name (input.txt) in the `stage1_nowinnowing.py`
  
 2) `bash script.sh`


## Detailed description of the code

The code executes in the following stages:

1) RAKE (Rapid Automatic Keyword Extraction) was used to extract keywords.

2) The scoring of the keyphrases was done based on the their word frequencies and
   word degrees with the score given by => score = (word_degree) / (word_frequency)

3) Many edge cases caused errors in the output. Some of them are as follows:
    i) Splitting on fullstops, causes decimal numbers to be split
    ii) Similarly for designations like Mr., Mrs., Ms., Dr., etc
    iii) For inititals like A. the sentence further includes the rest of the name,
         hence we should not split on the full stop here

4) For proper nouns, we put together consecutively occuring proper nouns so that
   they are considered as one and not as two different keywords.(Eg. Name Surname)

5) OpenIE is used to give the subject – action – object mapping for each sentence.

6) From the keyphrases extracted, we find the common ones which belong to the RAKE’s
   output and OpenIE’s subject output and work further only on the sentences which
   have the keywords as subjects.

7) Then pronouns are replaced by proper nouns(if present) which occur immediately
   in the next sentence to get better output.

8) Proper nouns are replaced by proper nouns consisting them
   (Name and Name-Surname if present both are considered as Name-Surname)
   to avoid redundancy and avoid sharing of importance.

`After this, all sorts of post processing is done on the output of OpenIE output
to remove redundancy and get only the required output. These steps are necessary as
OpenIE gives very redundant subject – action – verb combinations.`

9) We then form adjacency matrix of all the nodes(subject and object in the processed
   OpenIE output), to get connectivity of each node. It is a directed graph.

10) We then sort the nodes in descending order of connectivity and pick up the
    top 3 nodes.

11) Now the winnowing process is done wherein we select the sentences including
    at least one of these top 3 nodes.

12) We treat this collection of sentences as our new input text and do all the
    above steps till step 9.

13) We then assign scores to each of the sentences based on the presence of the
    nodes with the score being equivalent to the sum of the connectivity of each
    node present.

14) We then select the top 1/3 rd of these sentences and print them on the basis
    of their occurence in the original text.

15) This forms our summary for the original input.

16) Two types of graphs are plotted. One using graphviz and other networkx.


## Thus in short,

1) Preprocessing is done on input text to get required form of text to be passed
   as an input to the keyword extractor.

2) RAKE extractor used.

3) Scoring and selecting top keyphrases.

4) OpenIE extractor used on input text to get subject – action – object
   in each sentence.

5) Common subjects between OpenIE output and RAKE output are selected.

6) Post-processing on this common output of OpenIE to get better form of graphs
   by removing all sorts of redundancies.

7) Finding connectivity of each node of the graph and applying the
   winnowing process to get reduced text.

8) Applying the above extraction process again on the reduced text.

9) Scoring and selecting top few sentences containing these nodes and displaying
   them in the order of their appearence in the original text gives us the summary.

10) Graphs are displayed.


## Summary

Thus based on a purely statistical approach, we first obtained the top keyphrases,
and then using a logical approach of getting an intersection between RAKE and OpenIE
output we restricted the sentences to be processed. Then a more reliable approach
was used to find the connectivity of nodes. The nodes now obtained by finding the
connectivity are more reliable than the initially obtained keyphrases from just RAKE.
Thus, from purely numerical, limited, and not totally reliable statistics we converged
towards a more reliable and logical approach to find important words in the  text.
This was further used to find sentences which consisted of these important words to
form the summary.


Procedure explained as a figure:

<img src="https://github.com/architsakhadeo/Text-Summarizer/blob/master/procedure.png?raw=true" width="500">
