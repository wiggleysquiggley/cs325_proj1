### About this project
This program was written to scrape a website and parse through the content using Beautiful Soup in order to isolate the comments left on an item on a website (in this case eBay). It takes the parsed webpage and sorts through the content to find where all the feedback for this item specific item is. It then goes through all the pages of customer feedback and writes all of the comments in an output file.

### To download Beautiful Soup
1. open Command Prompt or an environment in VSCode
2. run the following commands
>pip install beautifulsoup4

>pip install bs4

>pip install lxml
3. make sure "requests" is installed by running the following command:
>pip install beautifulsoup4 requests

### To run Beautiful Soup
1. make sure you import needed libraries
>import requests

>from bs4 import BeautifulSoup
2. use "requests" in order to get the content
>response = requests.get(url)
3. make the soup
>soup = BeautifulSoup(response.content, "html.parser")
4. various commands can be used to go through the soup
    - for full list of commands go to [Beautiful Soup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### To run project2.py
1. make sure **project2.py** and **urls.txt** are in the same folder
2. click run and the files will pop up as the comments are scrapped and they're written to their assgined file
3. to use your own urls
   - put all urls in **urls.txt**, with one url per line
   - find the first half of your url when it fetches the next page of feedback, since it only retrieves the relative path, not the full path
   - replace 'https://www.ebay.com/fdbk/mweb_profile' on line 48 with the first half of the link you have chosen