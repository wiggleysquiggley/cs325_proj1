#Kaitlyn Kelble - 800743046
#project 3 .py file

#import ollama in order to use phi3
import ollama

#import beautifulsoup in order to use soup
import requests
from bs4 import BeautifulSoup

#import matplotlib, numpy, and textwrap libraries for graph
import matplotlib.pyplot as plt
import numpy as np
import textwrap

#class for scrapping website
class Scraper:
    def __init__(self, urls_file):
        #assigns file name for urls and calls get_urls()
        self.urls_file = urls_file
        self.urls = self.get_urls()

    def get_urls(self):
        #opens and reads file containing urls and assigns to lines
        with open(self.urls_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return lines
    
    def fetch_comments(self, url):
        #fetches the webpage 
        response = requests.get(url)

        #parses the page content
        soup = BeautifulSoup(response.content, "html.parser")

        #gets name of item from item page
        filename = soup.find('span', class_='ux-textspans ux-textspans--BOLD').string

        #finds where section for seller feedback is
        seller_fdbk = soup.find('a', class_='fdbk-detail-list__tabbed-btn fake-btn fake-btn--large fake-btn--secondary')

        #gets the link for the page that includes all seller feedback for item
        url = seller_fdbk['href']
        response = requests.get(url)

        #parses the page content
        soup = BeautifulSoup(response.content, "html.parser")

        #finds div where comments are stored
        all_tab = soup.find('div', class_='tabs__content')
        #goes to next div in order to specify comments for this item specifically
        this_tab = all_tab.find('div', class_='tabs__panel')

        #finds where the link for the next page
        next_page = this_tab.find('a', class_='pagination__next icon-link')

        #checks tp make sure next_page was fetche properly
        if next_page == None:
            next_page = 0

        #goes through this loop while there is a next page of comments
        while next_page != 0:
            #generates full link for next page, fetches the webpage, and parses it
            next_url = 'https://www.ebay.com/fdbk/mweb_profile' + next_page['href']
            response  = requests.get(next_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            #finds where comments are stored and specifies use of this item comments
            all_tab = soup.find('div', class_='tabs__content')
            this_tab = all_tab.find('div', class_='tabs__panel')

            #finds each inidiviual comment and writes it to file
            comments = this_tab.find_all('div', class_='fdbk-container__details__comment')
            for c in comments:
                with open(filename, 'a', encoding='utf-8') as f_c:
                    f_c.write(c.get_text())
                    f_c.write('\n')

            #finds the link for the next page
            next_page = this_tab.find('a', class_='pagination__next icon-link')
            #checks if None and assign page to 0 as needed to stop loop
            if next_page == None:
                next_page = 0

        #open file containing the comments using the read only option
        with open(filename , "r", encoding='utf-8') as f:
            #assign each individual line (comment) as an item in a list called lines
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        return filename, lines

#class for analyzing the sentiment of comments    
class Analyzer:
    def analyze_comments(self, line, filename):
        #API for ollama to analyze the sentiment of line
        result = ollama.chat(
            model = 'phi3',                                     #using model phi3
            messages = [{'role': 'user', 'content': f'Using only one word, classify the sentiment of this review as positive, negative, or neutral: "{line}"'}],     #declaring role as user with content of a single line
            stream = True,                                      #lets response be printed while being generated
            options = {
                "num_predict": 3,       #allows three tokens to be output
                "temperature": 0        #gives it zero personality (no creativity)
            }
        )
        
        full_result = ''
        #for each chunk in result it adds to full_result, generating the full response
        for chunk in result:
            full_result += chunk['message']['content']

        #modifies result to strip white space and make all lowercase for easier assessment
        stripped_result = full_result.strip().lower()

        #write stripped results to file
        with open(filename + "_output.txt", "a", encoding='utf-8') as f_a:
            f_a.write(stripped_result + "\n")

        return stripped_result
        
    def count_sentiments(self, comments, filename):
        #initialize counts to zero
        pos_count = 0
        neg_count = 0
        neutral_count = 0

        #goes through each comment that was passed through
        for comment in comments:
            #calls analyze_comments to get the analysis of the comment
            sentiment = self.analyze_comments(comment, filename)
            if "positive" in sentiment:
                pos_count += 1
            elif "negative" in sentiment:
                neg_count += 1
            elif "neutral" in sentiment:
                neutral_count += 1

        #takes filename and total counts of positive, negative, and neutral and adds to its respective list
        categories.append(filename)
        pos_values.append(pos_count)
        neg_values.append(neg_count)
        neutral_values.append(neutral_count)

#class for creating a bar graph for the total sentiments of each type for each product
class Graph:
    def plot(self, categories, pos_values, neg_values, neutral_values):
        #position for each bar
        x = np.arange(len(categories))

        #makes it so the title of each device are elligible since they're very long
        wrapped_labels = [textwrap.fill(label, width=25) for label in categories]

        #plot bars for positive, negative, and neutral counts for each product
        plt.bar(x - 0.2, pos_values, width=0.2, label='Positive', color='cornflowerblue')
        plt.bar(x      , neg_values, width=0.2, label='Negative', color='tomato')
        plt.bar(x + 0.2, neutral_values, width=0.2, label='Neutral', color='gold')

        #add labels and title
        plt.xlabel('Devices')
        plt.ylabel('Number of Sentiments')
        plt.title('Sentiments for Devices')
        plt.xticks(x, wrapped_labels, fontsize=8)   #for each device specifically, fontsize 8 so titles fit on screen
        plt.legend(title = 'Sentiment Types')

    #function to specifically print the bar graph
    def print_plot(self):
        plt.show()

if __name__ == "__main__":
    #creating instances for each class
    scraper = Scraper('urls.txt')
    analyzer = Analyzer()
    graph = Graph()
    #initializing the lists
    categories, pos_values, neg_values, neutral_values = [], [], [], []

    #going through each url in url file
    for url in scraper.urls:
        #fetching the comments
        filename, comments = scraper.fetch_comments(url)
        #counting the sentiments for the comments
        analyzer.count_sentiments(comments, filename)

    #creating graph and showing said graph
    graph.plot(categories, pos_values, neg_values, neutral_values)
    graph.print_plot()