# ATTENTION! 
# The following code may need to be run once before using this module.
# If needed, uncomment the code below, run a single time, and then comment out again.

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')


# ATTENTION! 
# The following code will save txt files in the form 'wiki-page-#.txt' to the current directory.

import random
import heapq
import requests
from string import punctuation
from bs4 import BeautifulSoup
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models import TfidfModel
from gensim.corpora import Dictionary

wiki_site = 'https://en.wikipedia.org'
wiki_index = '/wiki/Wikipedia:Contents/A–Z_index'
project_page = '/wiki/Special:AllPages/'
special_page = '/wiki/'
save_file = 'wiki-page'
num_urls = 10


# Search a user specified number of random Wikipedia pages for a user specified query.
def main():
    print("Search a user specified number of random Wikipedia pages for a user query:\n")
    num_pages = get_num_pages()
    page_links = source_wiki_pages(num_pages)
    wiki_pages = retrieve_wiki_pages(page_links)
    clean_save_text(wiki_pages)
    perform_search(*compile_corpus(num_pages))
    
    
# Requests a user specified number of Wikipedia pages to include in the search.
def get_num_pages():
    while True:
        try:
            num_pages = abs(int(input("Specify the number of Wikipedia pages to search: ").strip()))
            break
        except:
            print("* Your input must be a positive integer. *")
            
    return num_pages
            
            
# Sources the Wikipedia pages to be retrieved below.
def source_wiki_pages(num_pages):
    count = 0
    page_links = []
    print("\n* Please be patient. The Wikipedia pages retrieval may take a few minutes to complete. *")
    
    while True:
        try:
            sub_indices = get_wiki_link(num_pages, project_page, wiki_index)
            print("Sourcing Pages: ", end='')
            
            for sub_index in sub_indices:
                count += 1
                print(f"{count},", end='')
                page_link = get_wiki_link(1, special_page+sub_index[22:], sub_index)[0]
                page_links.append(page_link)
            break
        except:
            print("\n*** Experienced an error. Trying again. ***")
    print()
    
    return page_links


# Retrieves the sourced Wikipedia pages identified above.
def retrieve_wiki_pages(page_links):
    count = 0
    wiki_pages = {}
    print("Retrieving Pages: ", end='')
    
    for page_link in page_links:
        count += 1
        
        try:
            wiki_pages[f"{wiki_site}{page_link}"] = request_wiki_page(page_link)
            print(f"{count},", end='')
        except:
            print(f"\n**** An exception occurred. Skipping page {count}. ****")
    print()
    
    return wiki_pages


# Saves to disk the url and text from the Wikipedia pages retrieved above.
def clean_save_text(wiki_pages):
    count = 0
    print("Cleaning Text: ", end='')
    
    for page_url, page_text in wiki_pages.items():
        count += 1
        print(f"{count},", end='')
        cleaned_text = clean_text(page_text)
        save_to_file(count, page_url, cleaned_text)
        
        
# Tokenizes and cleans text discarding stopwords, punctuation, adjectives, etc.
def clean_text(text):
    cleaned_text = []
    tokens = word_tokenize(text)
    tokens = pos_tag(tokens)

    for token in tokens:
        if token[0].lower() not in stopwords.words('english'):
            if token[0] not in punctuation and token[0] not in ["''",'``','–',"'s","'t","'m","'d","'ve","'re","'ll",'•','·']:
                if token[0].lower().find('wiki') == -1 and token[1] not in ['JJ', 'JJR', 'JJS']:
                    cleaned_text.append(token[0].lower().replace("'", ''))
                            
    return cleaned_text


# Retrieves a Wikipedia index page and parses the content for appropriate links using BeautifulSoup
def get_wiki_link(num_pages, page_type, sub_page):
    wiki_links = []
    url = f"{wiki_site}{sub_page}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_links = soup.find(id="bodyContent").find_all("a")

    for _ in range(num_pages):
        random.shuffle(all_links)

        for link in all_links:
            if link['href'].find(page_type) == -1:
                continue
            break

        wiki_links.append(link['href'])

    return wiki_links


# Retrieves a Wikipedia page and parses the content for text using BeautifulSoup.
def request_wiki_page(wiki_link):
    url = f"{wiki_site}{wiki_link}"
    page_request = requests.get(url)
    page_text = BeautifulSoup(page_request.text, features='lxml').get_text()
    
    return page_text


# Saves a file in the form 'wiki-page#.txt' to the current directory including the url and text.
def save_to_file(num, page_url, wiki_text):
    file_name = f"{save_file}-{num}.txt"

    with open(file_name, 'w') as filehandle:
        filehandle.write(f"{page_url}\n")

        for text in wiki_text:
            try:
                filehandle.write(f"{text}\n")
            except:
                continue
                
                
# Opens a saved 'wiki-page#.txt' file from the current directory and returns the url and text.
def open_saved_file(num):
    wiki_text = []
    file_name = f"{save_file}-{num}.txt"
    
    with open(file_name, 'r') as filehandle:
        url = filehandle.readline().strip()
        line = filehandle.readline()

        while line:
            wiki_text.append(line)
            line = filehandle.readline().strip()

    return url, wiki_text


# The following performs a search within the saved radom Wikipedia pages for the terms provided by the user.
# Creates a model using gensim.TfidfModel and uses the model to vectorize the text.
# Stores the vector scores in a nested dict for each term in user query for each Wikipedia page.
# Sums all the vector scores for each Wikipedia page and places the total score in a priority queue.
# Pulls and displays up to 10 of the most relevent Wikepedia page links.
def compile_corpus(num_pages):
    urls = []
    data = []
    
    for num in range(num_pages):
        url, datum = open_saved_file(num+1)
        urls.append(url)
        data.append(datum)

    dictionary = Dictionary(data)
    unique_words = dictionary.token2id.keys()
    
    corpus = [dictionary.doc2bow(text) for text in data]
    model = TfidfModel(corpus)
    
    return dictionary, unique_words, corpus, model, urls
    
    
def perform_search(*args):
    url_scores = []
    corpus_scores = {}
    count = 1
    num = num_urls
    dictionary, unique_words, corpus, model, urls = args
    
    while True:
        try:
            query = input("\nProvide your search query here (submit 'q' to quit):\n\t")
            if query == 'q' or query == 'Q':
                return
            terms = clean_text(query)
            break
        except:
            print("\n** Something went wrong. Please try again. **")
    print()
    
    for i in range(len(corpus)):
        corpus_scores[urls[i]] = {}
        vector = model[corpus[i]]
        
        for term in terms:
            if term in unique_words:
                term_id = dictionary.token2id[term]
                corpus_scores[urls[i]].update({term: 0})
                
                for word_id, score in vector:
                    if word_id == term_id:
                        corpus_scores[urls[i]][term] = score
                        break
    
    for url, terms_scores in corpus_scores.items():
        total_score = 0
        
        for term, score in terms_scores.items():
            if score > 0:
                total_score += score
                    
        heapq.heappush(url_scores, (0-total_score, url))
        
    while len(url_scores) > 0 and num > 0:
        temp = heapq.heappop(url_scores)
        print(f"{count:>2}: {temp[1]}")
        count += 1
        num -= 1
        
    perform_search(*args)


if __name__ == '__main__':
    
    main()
    
