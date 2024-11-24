#Import all the required libraries
import re
import nltk
import argparse
from nltk.grammar import FeatureGrammar
from nltk.parse import FeatureEarleyChartParser



#Download all the required functionalities from nltk
nltk.download("punkt")
nltk.download("punkt_tab")

nltk.download('averaged_perceptron_tagger_eng')

nltk.download('maxent_ne_chunker')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')





#This function is used to read a text or a SGML/HTML file. The function uses regex to remove all the MARKUP Tags.
def read_file(file_path):
  content = ""

  with open(file_path,'r',encoding='latin-1') as file:
    content = file.read()

  #This line removes all the HTML content and returns the remaining plain text, then we split the sentences based on new line.  
  content = re.sub(r"<.*?>", "", content)
  content_list = re.split("\n",content)

  new_content_list = []

  #loop through the content and remove all the empty space lines and new line characters
  for x in content_list:
    if x!="" and x!="\n":
      new_content_list.append(x)

  content = ""

  #join the sentences with a new line character. We removed the new lines in the above loop to avoid the occurence of multiple contiguous empty lines.
  for sent in new_content_list:
      content += sent+"\n"
  
  #Return the entire content as plain text after the removal of all the HTML tags.
  return content






#This function tokenizes the complete text into a list of sentences.
def sentence_tokenize(paragraphs):
  sentences = []

  #We make use of the sent_tokenize function in NLTK for this purpose
  for para in paragraphs:
    sentences += nltk.sent_tokenize(para)
  return sentences

#A similar function to tokenize the sentences further into words.
def word_tokenize(sentence):
  return nltk.word_tokenize(sentence)





#This is the main pipeline from the earley parser 
def parser_pipeline(grammar_file_path,sentences_file_path):

    #Read the grammar from the file and turn it into a CFG object using the CFG python function. Then create a parser with that grammar
    # The parser we use is the earley chart parser  
    grammar = FeatureGrammar.fromstring(read_file(grammar_file_path))
    parser = FeatureEarleyChartParser(grammar)
  
    #Get the content of all the sentences in the file.
    text = read_file(sentences_file_path)

    #split the sentences and tokenize them
    paragraphs = re.split("\n",text)
    sentences = sentence_tokenize(paragraphs)   

    #a list to store all the sentences that are not parsed or producing errors.
    no_parse_sents = []
    parsed_sents = []
    parsed_trees = []    

    #loop through every sentence
    for sent in sentences:

        #remove the following punctuators from the sentences and convert the sentences to lower case as it is the form of our grammar
        sent = re.sub(r'[,;:<>{}?.()_=+|%\-\\\'\"]',"",sent.lower())
        sent = sent.replace("&quot","")     
        
        #split the sentences into words
        words = sent.split()
        is_parsed = False #Check for parsing

        #Now parse the words list using the sentence parser. If a parsing is found then print the sentence along with the parser.
        #Set the boolean to true. The break statment is used to stop the printing of all other possible parses for the sentences.
        #you may remove the statment to print all possible parsers.
        #Try catch block is used to avoid the errors which mostly arises due to the absence of terminals in the grammar.
        try:
            for tree in parser.parse(words): 
                is_parsed = True  
                parsed_sents.append(sent)
                parsed_trees.append(tree)
                print(sent)
                print(tree)
                print("")
                break
        except: #we append the sentences that are not parsed 
           no_parse_sents.append(sent)
           is_parsed = True
    
        if(not is_parsed):
          no_parse_sents.append(sent)

    if(len(parsed_sents)>0):
       parsed_sent = ""
       parsed_sents_and_trees = ""

       for i in range(0,len(parsed_sents)):
          parsed_sent+=parsed_sents[i]+"\n"
          parsed_sents_and_trees += parsed_sents[i]+"\n"+(str)(parsed_trees[i])+"\n\n"

       parsed_sent_path = sentences_file_path[0:sentences_file_path.rfind('/')]+"/Results/good.txt"
       sent_tree_path = sentences_file_path[0:sentences_file_path.rfind('/')]+"/Results/good-annotations.txt"

       # Write the sentences and parsers to the file
       with open(sent_tree_path, "w",encoding='latin-1') as file:
            file.write(parsed_sents_and_trees)

       # Write only the parsed sentences to the file
       with open(parsed_sent_path, "w",encoding='latin-1') as file:
            file.write(parsed_sent)



    if(len(no_parse_sents)>0):
       no_parsed_sent = ""

       for x in no_parse_sents:
          no_parsed_sent += x+"\n"
    
       print("The given grammar is insufficient to parse the following sentences")
       print(no_parsed_sent)

       no_parse_path = sentences_file_path[0:sentences_file_path.rfind('/')]+"/Results/False.txt"

       # Write only the non parsed sentences to the file
       with open(no_parse_path, "w",encoding='latin-1') as file:
            file.write(no_parsed_sent)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # Adding argument (file_path)
    parser.add_argument('--input', nargs='+', type=str)

    # Parse the arguments
    args = parser.parse_args()

    input_data = args.input
    input = []

    for i,string in enumerate(input_data):
       input.append(string)       
    
    # Call the main function with parsed arguments
    parser_pipeline(input[0],input[1])