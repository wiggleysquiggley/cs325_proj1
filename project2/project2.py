import requests
from bs4 import BeautifulSoup

# Fetch the webpage seller feedback
url = "https://www.ebay.com/fdbk/mweb_profile?fdbkType=FeedbackReceivedAsSeller&item_id=125799442762&username=kitchenaid&filter=feedback_page%3ARECEIVED_AS_SELLER&q=125799442762&sort=RELEVANCE"
response = requests.get(url)

# Parse the page content
soup = BeautifulSoup(response.content, "html.parser")

# Extract and print the title
title = soup.title.string
print("Page Title:", title)

all_tab = soup.find('div', class_='tabs__content')
this_tab = all_tab.find('div', class_='tabs__panel')

next_page = this_tab.find('a', class_='pagination__next icon-link')

#print('https://www.ebay.com/fdbk/mweb_profile' + next_page['href'])


while next_page != 0:
    next_url = 'https://www.ebay.com/fdbk/mweb_profile' + next_page['href']
    response  = requests.get(next_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    all_tab = soup.find('div', class_='tabs__content')
    this_tab = all_tab.find('div', class_='tabs__panel')

    comments = this_tab.find_all('div', class_='fdbk-container__details__comment')
    for c in comments:
        print(c.get_text())
        print('\n')

    next_page = this_tab.find('a', class_='pagination__next icon-link')
    if next_page == None:
        next_page = 0