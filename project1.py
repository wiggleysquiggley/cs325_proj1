#Kaitlyn Kelble - 800743046
#project 1 .py file

#import ollama in order to use phi3
import ollama

#open file containing the questions using the read only option
with open("questions.txt" , "r") as f:
    #assign each individual line (question) as an item in a list called lines
    lines = f.readlines()

#looping through the list called lines and for each individual line, sending to phi3 and recording the response
for line in lines:
    #API for ollama
    result = ollama.chat(
        model = 'phi3',                                     #using model phi3
        messages = [{'role': 'user', 'content': line}],     #declaring role as user with content of a single line
        stream = True,                                      #lets response be printed while being generated
    )
    
    #for each chunk in result it appends the generated response chunk to the answers.txt file
    for chunk in result:
        with open("answers.txt", "a") as f_a:
            f_a.write(chunk['message']['content'])

    #appends two newlines to file between the answers of each question in order to visually separate them
    with open("answers.txt", "a") as f_a:
        f_a.write("\n\n")

#close both files for housekeeping purposes
f.close()
f_a.close()