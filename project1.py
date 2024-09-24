#Kaitlyn Kelble - 800743046
#project 1 .py file

import ollama

with open("questions.txt" , "r") as f:
    lines = f.readlines()

for line in lines:
    result = ollama.chat(
        model = 'llama3.1',
        messages = [{'role': 'user', 'content': line}],
        stream = True,
    )

    for chunk in result:
        with open("answers.txt", "a") as f_a:
            f_a.write(chunk['message']['content'])

    with open("answers.txt", "a") as f_a:
        f_a.write("\n\n")

f.close()
f_a.close()