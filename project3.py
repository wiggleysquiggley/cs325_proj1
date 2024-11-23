#Kaitlyn Kelble - 800743046
#project 3 .py file

#import ollama in order to use phi3
import ollama

#import beautifulsoup in order to use soup
import requests
from bs4 import BeautifulSoup

#import matplotlib libraries for graph
import matplotlib.pyplot as plt
import numpy as np

import textwrap

class Scraper:
    def __init__(self, urls_file):
        self.urls_file = urls_file
        self.urls = self.get_urls()

    def get_urls(self):
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
    
class Analyzer:
    def analyze_comments(self, line, filename):
        #API for ollama
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
        #for each chunk in result it appends the generated response chunk to the filename_output.txt file
        for chunk in result:
            full_result += chunk['message']['content']

        stripped_result = full_result.strip().lower()

        with open(filename + "_output.txt", "a", encoding='utf-8') as f_a:
            f_a.write(stripped_result + "\n")

        return stripped_result

        
    def count_sentiments(self, comments, filename):
        pos_count = 0
        neg_count = 0
        neutral_count = 0

        for comment in comments:
            sentiment = self.analyze_comments(comment, filename)
            if "positive" in sentiment:
                pos_count += 1
            elif "negative" in sentiment:
                neg_count += 1
            elif "neutral" in sentiment:
                neutral_count += 1

        with open("total_results.txt", "a", encoding='utf-8') as f_r:
            f_r.write(f"{filename}: pos: {pos_count} neg: {neg_count} neutral: {neutral_count}\n")

        categories.append(filename)
        pos_values.append(pos_count)
        neg_values.append(neg_count)
        neutral_values.append(neutral_count)

class Graph:
    def plot(self, categories, pos_values, neg_values, neutral_values):
        # Position for each bar
        x = np.arange(len(categories))

        wrapped_labels = [textwrap.fill(label, width=25) for label in categories]

        # Plot bars
        plt.bar(x - 0.2, pos_values, width=0.2, label='Positive', color='cornflowerblue')
        plt.bar(x      , neg_values, width=0.2, label='Negative', color='tomato')
        plt.bar(x + 0.2, neutral_values, width=0.2, label='Neutral', color='gold')

        # Add labels and title
        plt.xlabel('Devices')
        plt.ylabel('Number of Sentiments')
        plt.title('Sentiments for Devices')
        plt.xticks(x, wrapped_labels, fontsize=8)  # Set x-axis labels
        plt.legend(title = 'Sentiment Types')

    def print_plot(self):
        plt.show()

if __name__ == "__main__":
    scraper = Scraper('urls.txt')
    analyzer = Analyzer()
    graph = Graph()
    categories, pos_values, neg_values, neutral_values = [], [], [], []

    for url in scraper.urls:
        filename, comments = scraper.fetch_comments(url)
        analyzer.count_sentiments(comments, filename)

    graph.plot(categories, pos_values, neg_values, neutral_values)
    graph.print_plot()