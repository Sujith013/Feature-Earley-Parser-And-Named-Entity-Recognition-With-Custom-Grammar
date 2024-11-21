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







# Function to extract entities of a specific non-terminal (e.g., drug)
def extract_entities(tree, Named_Entity):
    entities = []

    # If the tree is a terminal, there's nothing to do
    if isinstance(tree, str):
        return entities
    
    # If it's a non-terminal and matches the target, collect its leaves
    for x in tree.label().keys():
        if tree.label().get(x) == Named_Entity:
            return tree.leaves()

    # Otherwise, recursively search the subtrees
    for subtree in tree:
        entities.extend(extract_entities(subtree, Named_Entity))

    return entities




#
def NER_pipeline(file_path,grammar_path):

  grammar_string = ""

  with open(grammar_path,'r',encoding='latin-1') as file:
      grammar_string = file.read()

  grammar = FeatureGrammar.fromstring(grammar_string)
  parser = FeatureEarleyChartParser(grammar)
  
  text = read_file(file_path)

  paragraphs = re.split("\n",text)
  sentences = sentence_tokenize(paragraphs)

  ner_output = ""
  f = 0
  j = 0
  
  for sent in sentences:
      f = 0
      sent = re.sub(r'[,;:<>{}?.()_=+|%°\-\\\'\"]',"",sent.lower())
      sent = sent.replace("&quot","")
      words = sent.split()

      trees = parser.parse(words)
      final_named_entities = []
      
      print(j)
      
      if trees != None:
        for i, tree in enumerate(trees):
            named_entities = extract_entities(tree, "chemical")
            
            if(len(named_entities)>len(final_named_entities)):
              final_named_entities = list(tuple(named_entities))

      if(len(final_named_entities)!=0):
          print(f"Named entities (Chemical): {final_named_entities}")
          ner_output += sent+"\n"
          ner_output += "Named entities (Chemical): ["+" ".join(final_named_entities)+"]\n"
          f = 1

      trees = parser.parse(words)
      final_named_entities = []
      
      if trees != None:
        for i, tree in enumerate(trees):
            named_entities = extract_entities(tree, "drug")
            
            if(len(named_entities)>len(final_named_entities)):
              final_named_entities = list(tuple(named_entities))

      if(len(final_named_entities)!=0):
          print(f"Named entities (Drugs): {final_named_entities}")
          if f==0:
             ner_output += sent+"\n"
          ner_output += "Named entities (drugs): ["+" ".join(final_named_entities)+"]\n"
          f = 1
      
      trees = parser.parse(words)
      final_named_entities = []
      
      if trees != None:
        for i, tree in enumerate(trees):
            named_entities = extract_entities(tree, "org")
            
            if(len(named_entities)>len(final_named_entities)):
              final_named_entities = list(tuple(named_entities))
      
      if(len(final_named_entities)!=0):
          print(f"Named entities (org): {final_named_entities}")
          if f==0:
             ner_output += sent+"\n"
          ner_output += "Named entities (org): ["+" ".join(final_named_entities)+"]\n"
      
      j += 1
  
  with open("../Results/NER.txt", "w",encoding='latin-1') as file:
          file.write(ner_output)








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
    NER_pipeline(input[0],input[1])