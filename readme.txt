The six PIL has the extracted sentences file from the six main pil leaflets and the PIL folder has the rest of them. 
The Grammar folder contains two files. The terminal_grammar.txt has the terminal part of the grammar and the final_grammar_with_ner.txt is the file containing both the terminal and the non terminal part constituting the final feature grammar of our project.

The Entity Data folder contains all the text documents for drugs, chemicals and organization containing the words list to be passed as terminals to the feature grammar.

The results folder contains the final output.
-> good.txt - the sentences from the six main PIL leaflets that are successfully parsed by the grammar.
-> good-annotations.txt - the sentences from the six main PIL leaflets that are successfully parsed by the grammar along with their annotations.
-> false.txt - the sentences from the six main PIL leaflets that are not parsed by the grammar.

-> NER.txt - the file with all the NER values (drugs, chemicals and organizations) found by the grammar along with the sentences.
-> NER_with_annotations.txt - the file with all the NER values (drugs, chemicals and organizations) found by the grammar along with the sentences and the tree annotations.

The sentences.txt file contains the sentences extracted from the six leaflets. The sample sentences file contains the sentences that were manually added to check the validity of the feature grammar. 

-> good_sample.txt - all the sentences which are grammatically correct with respect to person and number agreement.
-> false_sample.txt - all the sentences which are grammatically wrong with respect to person and number agreement.


CODE
 The NLA_project.ipynb file was just used for the ease of running parts of a code and debugging. It doesn't contain the final refined code of the project.

The extract-plain-text.py is the file used in project one to extract the text from the sgml files with HTML annotations.

The feature-early-parser.py is the file with that takes the path to the grammar file and the sentences file as input and returns the final output with three files good, false and good-annotations. To run the file go to the location of the file in the command prompt and enter the following

python feature-earley-parser.py --input "../Grammar/final_grammar_with_ner.txt" "../sentences.txt"

The path to the grammar file and the sentences file can be changed according to the need.

Similarly the NER.py file contains the code that detects the Named entities in the sentences and then returns the NER_with_annotations file. To run the file do the following

python NER.py --input "../Grammar/final_grammar_with_ner.txt" "../sentences.txt"
