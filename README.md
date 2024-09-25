To install Phi3 on your computer using Ollama:
1. go to ollama.com/download/windows
2. click "Download for Windows (Preview)"
3. after download is complete, go to command prompt or VScode terminal and run the command "ollama"

   3a.if this does not work, try closing and reopening command prompt or VScode
4. to directly run in terminal in command prompt or VScode run the command "ollama run phi3"

    4a. to see full list of commands for ollama run the command "ollama help"
5. to be able to use in program (like project1.py in this repository) run the command "pip install ollama"

    5a. if this alone does not let you use "import ollama" run the command "ollama pull llama3.1" 
6. make sure "project1.py" and "questions.txt" are in the same folder
7. click the "play" (run) button in the top right corner of the VScode layout
8. "answers.txt" should appear on the left hand side among the other files

    8a. click on this file in order to see the final answers and also watch phi3 write the replies 
