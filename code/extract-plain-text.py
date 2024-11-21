#Import all the required libraries
import re
import nltk
import argparse

#Download all the required functionalities from nltk
nltk.download("punkt")
nltk.download("punkt_tab")

nltk.download('averaged_perceptron_tagger_eng')

nltk.download('maxent_ne_chunker')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')

#This function is used to read a text or a SGML/HTML file. The function uses regex to remove all the MARKUP Tags.
def extract_text(file_path_arg):
  #Get the file path
  file_path = file_path_arg.input
  
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
  
  new_file_path = file_path[0:file_path.rfind('.')]+"-plain text.txt"

  # Write the string to the file
  with open(new_file_path, "w",encoding='latin-1') as file:
    file.write(content)

  #Return the entire content as plain text after the removal of all the HTML tags.
  print(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # Adding argument (file_path)
    parser.add_argument('--input', type=str)

    # Parse the arguments
    args = parser.parse_args()
    
    # Call the main function with parsed arguments
    extract_text(args)
