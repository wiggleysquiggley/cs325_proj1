#Ksitlyn Kelble - 800743046
#CS325 - Sec 002

#import needed libraries
import requests
from bs4 import BeautifulSoup

#open and read file with urls
with open('urls.txt', 'r') as f:
    lines = f.readlines()

#goes through each url one at a time
for line in lines:
    #fetches the webpage 
    response = requests.get(line)

    #parses the page content
    soup = BeautifulSoup(response.content, "html.parser")

    #gets name of item from item page
    filename = soup.find('span', class_='ux-textspans ux-textspans--BOLD').string

    #finds where section for seller feedback is
    seller_fdbk = soup.find('a', class_='fdbk-detail-list__tabbed-btn fake-btn fake-btn--large fake-btn--secondary')

    #gets the link for the page that includes all seller feedback for item
    url = seller_fdbk['href']
    response = requests.get(url)

    #parsea the page content
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
                f_c.write('\n\n')

        #finds the link for the next page
        next_page = this_tab.find('a', class_='pagination__next icon-link')
        #checks if None and assign page to 0 as needed to stop loop
        if next_page == None:
            next_page = 0

#close file for housekeeping purposes
f.close()